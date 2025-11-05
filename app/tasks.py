"""
Celery tasks for background processing
"""
from celery import Celery
from flask import current_app
from flask_mail import Message
from app.models import db, User, Research
import os

# Initialize Celery
celery = Celery(__name__)


def init_celery(app):
    """Initialize Celery with Flask app context"""
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


@celery.task(name='app.tasks.send_email')
def send_email_task(subject, recipient, body, html=None):
    """Send email asynchronously"""
    try:
        from flask_mail import Mail
        mail = Mail(current_app)

        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=body,
            html=html
        )
        mail.send(msg)
        return {'status': 'success', 'recipient': recipient}
    except Exception as e:
        current_app.logger.error(f'Failed to send email: {str(e)}')
        return {'status': 'error', 'error': str(e)}


@celery.task(name='app.tasks.send_comment_notification')
def send_comment_notification(research_id, comment_id):
    """Send notification to research author when someone comments"""
    from app.models import Research, Comment

    try:
        research = Research.query.get(research_id)
        comment = Comment.query.get(comment_id)

        if not research or not comment:
            return {'status': 'error', 'message': 'Research or comment not found'}

        # Don't notify if author commented on own research
        if research.user_id == comment.user_id:
            return {'status': 'skipped', 'reason': 'Self-comment'}

        author = research.user
        if not author.email_notifications:
            return {'status': 'skipped', 'reason': 'Notifications disabled'}

        subject = f'New comment on your research: {research.title}'
        body = f'''
Hello {author.full_name},

{comment.user.full_name} commented on your research "{research.title}":

"{comment.content}"

Rating: {'⭐' * comment.rating if comment.rating else 'No rating'}

View your research: {current_app.config['SERVER_NAME']}/research/{research.id}

Best regards,
Research Management System
        '''

        send_email_task.delay(subject, author.email, body)
        return {'status': 'sent', 'recipient': author.email}

    except Exception as e:
        current_app.logger.error(f'Failed to send comment notification: {str(e)}')
        return {'status': 'error', 'error': str(e)}


@celery.task(name='app.tasks.cleanup_old_files')
def cleanup_old_files():
    """Clean up orphaned upload files"""
    try:
        upload_dir = current_app.config['UPLOAD_FOLDER']

        # Get all file paths from database
        db_files = set()
        for research in Research.query.all():
            if research.file_path:
                db_files.add(os.path.basename(research.file_path))

        # Check files in upload directory
        deleted_count = 0
        for filename in os.listdir(upload_dir):
            if filename not in db_files and not filename.startswith('.'):
                file_path = os.path.join(upload_dir, filename)
                os.remove(file_path)
                deleted_count += 1

        return {'status': 'success', 'deleted_count': deleted_count}

    except Exception as e:
        current_app.logger.error(f'Failed to cleanup files: {str(e)}')
        return {'status': 'error', 'error': str(e)}


@celery.task(name='app.tasks.generate_weekly_digest')
def generate_weekly_digest():
    """Generate weekly digest email for users"""
    from datetime import datetime, timedelta

    try:
        week_ago = datetime.utcnow() - timedelta(days=7)

        # Get new researches from past week
        new_researches = Research.query.filter(
            Research.created_at >= week_ago
        ).order_by(Research.created_at.desc()).limit(10).all()

        if not new_researches:
            return {'status': 'skipped', 'reason': 'No new researches'}

        # Send to users who opted in
        users = User.query.filter_by(email_notifications=True).all()
        sent_count = 0

        for user in users:
            subject = 'Weekly Research Digest'
            body = f'''
Hello {user.full_name},

Here are the latest researches from the past week:

'''
            for research in new_researches:
                body += f'- {research.title} by {research.authors}\n'

            body += f'''

Visit the site to read more: {current_app.config.get('SERVER_NAME', '')}

Best regards,
Research Management System
            '''

            send_email_task.delay(subject, user.email, body)
            sent_count += 1

        return {'status': 'success', 'emails_sent': sent_count}

    except Exception as e:
        current_app.logger.error(f'Failed to generate weekly digest: {str(e)}')
        return {'status': 'error', 'error': str(e)}


# Periodic tasks configuration
celery.conf.beat_schedule = {
    'cleanup-files-weekly': {
        'task': 'app.tasks.cleanup_old_files',
        'schedule': 604800.0,  # Weekly (in seconds)
    },
    'weekly-digest': {
        'task': 'app.tasks.generate_weekly_digest',
        'schedule': 604800.0,  # Weekly
    },
}

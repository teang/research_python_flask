#!/usr/bin/env python
"""
Database backup script
"""
import os
import subprocess
from datetime import datetime
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def backup_postgres(db_url, output_dir):
    """Backup PostgreSQL database"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(output_dir, f'db_backup_{timestamp}.sql')

    try:
        # Parse database URL
        # Format: postgresql://user:pass@host:port/dbname
        logger.info(f'Starting backup to {backup_file}')

        cmd = f'pg_dump {db_url} > {backup_file}'
        subprocess.run(cmd, shell=True, check=True)

        logger.info(f'✓ Backup completed: {backup_file}')

        # Compress backup
        logger.info('Compressing backup...')
        subprocess.run(f'gzip {backup_file}', shell=True, check=True)
        logger.info(f'✓ Compressed: {backup_file}.gz')

        return f'{backup_file}.gz'

    except subprocess.CalledProcessError as e:
        logger.error(f'✗ Backup failed: {str(e)}')
        return None


def cleanup_old_backups(output_dir, keep_days=30):
    """Remove backups older than specified days"""
    import time

    cutoff = time.time() - (keep_days * 86400)
    removed = 0

    for filename in os.listdir(output_dir):
        if filename.startswith('db_backup_') and filename.endswith('.gz'):
            filepath = os.path.join(output_dir, filename)
            if os.path.getmtime(filepath) < cutoff:
                os.remove(filepath)
                removed += 1
                logger.info(f'Removed old backup: {filename}')

    logger.info(f'Cleaned up {removed} old backups')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup database')
    parser.add_argument('--db-url', help='Database URL',
                       default=os.getenv('DATABASE_URL'))
    parser.add_argument('--output-dir', help='Output directory',
                       default='backups')
    parser.add_argument('--keep-days', type=int, default=30,
                       help='Days to keep backups')

    args = parser.parse_args()

    if not args.db_url:
        logger.error('Database URL not specified')
        exit(1)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Perform backup
    backup_file = backup_postgres(args.db_url, args.output_dir)

    if backup_file:
        # Cleanup old backups
        cleanup_old_backups(args.output_dir, args.keep_days)
        logger.info('Backup process completed successfully')
    else:
        logger.error('Backup process failed')
        exit(1)

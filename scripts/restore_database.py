#!/usr/bin/env python
"""
Database restore script
"""
import os
import subprocess
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def restore_postgres(db_url, backup_file):
    """Restore PostgreSQL database from backup"""
    try:
        logger.info(f'Starting restore from {backup_file}')

        # Decompress if needed
        if backup_file.endswith('.gz'):
            logger.info('Decompressing backup...')
            subprocess.run(f'gunzip -k {backup_file}', shell=True, check=True)
            backup_file = backup_file[:-3]  # Remove .gz extension

        # Restore database
        cmd = f'psql {db_url} < {backup_file}'
        subprocess.run(cmd, shell=True, check=True)

        logger.info('✓ Database restored successfully')

        # Clean up decompressed file
        if os.path.exists(backup_file) and backup_file.endswith('.sql'):
            os.remove(backup_file)

        return True

    except subprocess.CalledProcessError as e:
        logger.error(f'✗ Restore failed: {str(e)}')
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restore database from backup')
    parser.add_argument('backup_file', help='Backup file to restore')
    parser.add_argument('--db-url', help='Database URL',
                       default=os.getenv('DATABASE_URL'))

    args = parser.parse_args()

    if not args.db_url:
        logger.error('Database URL not specified')
        exit(1)

    if not os.path.exists(args.backup_file):
        logger.error(f'Backup file not found: {args.backup_file}')
        exit(1)

    # Confirm before restore
    response = input(f'⚠️  This will restore database from {args.backup_file}. Continue? (yes/no): ')
    if response.lower() != 'yes':
        logger.info('Restore cancelled')
        exit(0)

    # Perform restore
    if restore_postgres(args.db_url, args.backup_file):
        logger.info('Restore process completed successfully')
    else:
        logger.error('Restore process failed')
        exit(1)

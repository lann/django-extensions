__author__ = 'erik'

"""
 Command for restoring a database
"""

import os, time
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Backup database. Only Mysql and Postgresql engines are implemented"

    def handle(self, *args, **options):
        from django.db import connection
        from ... import settings

        infile = os.path.join(settings.BACKUP_LOCATION, "%s.sql" %(settings.BACKUP_BASENAME))

        if not settings.RESTORE_ENABLED:
            print 'restore not enabled, set settings.EXTENSIONS_RESTORE_ENABLED=True to enable'
        elif 'mysql' in settings.DB_ENGINE:
            print 'Doing Mysql restore of database %s from %s' % (settings.DB_NAME, infile)
            self.do_mysql_restore(infile)
        elif 'postgres' in settings.DB_ENGINE:
            print 'Doing Postgresql restore of database %s from %s' % (settings.DB_NAME, infile)
            self.do_postgresql_restore(infile)
        else:
            print 'Backup in %s engine not implemented' % settings.DB_ENGINE

    def do_mysql_restore(self, infile):
        from ... import settings
        args = []
        if settings.DB_USER:
            args += ["--user=%s" % settings.DB_USER]
        if settings.DB_PASSWD:
            args += ["--password=%s" % settings.DB_PASSWD]
        if settings.DB_HOST:
            args += ["--host=%s" % settings.DB_HOST]
        if settings.DB_PORT:
            args += ["--port=%s" % settings.DB_PORT]
        args += [settings.DB_NAME]

        os.system('mysql %s < %s' % (' '.join(args), infile))

    def do_postgresql_restore(self, infile):
        from ... import settings
        args = []
        if settings.DB_USER:
            args += ["--username=%s" % settings.DB_USER]
        if settings.DB_HOST:
            args += ["--host=%s" % settings.DB_HOST]
        if settings.DB_PORT:
            args += ["--port=%s" % settings.DB_PORT]
        if settings.DB_NAME:
            args += [settings.DB_NAME]
        os.system('PGPASSWORD=%s psql -c "drop schema public cascade; create schema public;" %s' % (settings.DB_PASSWD, ' '.join(args)))
        os.system('PGPASSWORD=%s psql %s < %s' % (settings.DB_PASSWD, ' '.join(args), infile))

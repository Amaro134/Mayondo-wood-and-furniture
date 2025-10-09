from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Clean up expired or corrupted sessions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=0,
            help='Remove sessions older than specified days (default: only expired)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Remove all sessions (forces logout for all users)',
        )

    def handle(self, *args, **options):
        if options['all']:
            # Delete all sessions
            count = Session.objects.count()
            Session.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted all {count} sessions')
            )
        elif options['days'] > 0:
            # Delete sessions older than specified days
            cutoff_date = timezone.now() - timedelta(days=options['days'])
            old_sessions = Session.objects.filter(expire_date__lt=cutoff_date)
            count = old_sessions.count()
            old_sessions.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {count} sessions older than {options["days"]} days'
                )
            )
        else:
            # Delete only expired sessions (default behavior)
            expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
            count = expired_sessions.count()
            expired_sessions.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} expired sessions')
            )
        
        # Show remaining session count
        remaining = Session.objects.count()
        self.stdout.write(f'Remaining active sessions: {remaining}')
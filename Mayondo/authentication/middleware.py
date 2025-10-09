import logging
from django.contrib.sessions.exceptions import SuspiciousSession
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore

logger = logging.getLogger('authentication')

class SessionErrorHandlingMiddleware:
    """
    Middleware to handle session corruption errors gracefully
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except (SuspiciousSession, ValueError, TypeError) as e:
            # Log the session error
            logger.warning(f'Session error detected: {str(e)}')
            
            # Clear the corrupted session
            try:
                request.session.flush()
                logger.info('Corrupted session cleared successfully')
            except Exception as clear_error:
                logger.error(f'Failed to clear corrupted session: {str(clear_error)}')
            
            # Add a user-friendly message
            messages.warning(request, 'Your session was corrupted and has been reset. Please log in again.')
            
            # Redirect to login page
            return HttpResponseRedirect(reverse('authentication:login'))
    
    def process_exception(self, request, exception):
        """
        Handle session-related exceptions during request processing
        """
        if isinstance(exception, (SuspiciousSession, ValueError, TypeError)):
            if 'session' in str(exception).lower():
                logger.warning(f'Session exception caught: {str(exception)}')
                
                try:
                    request.session.flush()
                    logger.info('Session flushed due to exception')
                except Exception as e:
                    logger.error(f'Failed to flush session on exception: {str(e)}')
                
                messages.warning(request, 'Session error occurred. Please log in again.')
                return HttpResponseRedirect(reverse('authentication:login'))
        
        return None
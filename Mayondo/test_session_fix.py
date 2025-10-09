#!/usr/bin/env python
"""
Quick test script to verify session configuration fixes
Run this script after setting up the virtual environment and applying migrations
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mayondo.settings')
django.setup()

from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory
from django.contrib.auth import get_user_model

def test_session_configuration():
    """Test session configuration settings"""
    print("=== Session Configuration Test ===")
    
    # Test session engine
    print(f"Session Engine: {settings.SESSION_ENGINE}")
    
    # Test session settings
    print(f"Session Cookie Age: {settings.SESSION_COOKIE_AGE} seconds")
    print(f"Session Cookie Name: {settings.SESSION_COOKIE_NAME}")
    print(f"Session Save Every Request: {settings.SESSION_SAVE_EVERY_REQUEST}")
    print(f"Session Serializer: {settings.SESSION_SERIALIZER}")
    
    return True

def test_session_creation():
    """Test creating and manipulating sessions"""
    print("\n=== Session Creation Test ===")
    
    try:
        # Create a new session
        session = SessionStore()
        session['test_key'] = 'test_value'
        session.save()
        
        print(f"Session created with key: {session.session_key}")
        
        # Retrieve the session
        retrieved_session = SessionStore(session_key=session.session_key)
        test_value = retrieved_session.get('test_key')
        
        if test_value == 'test_value':
            print("✓ Session creation and retrieval successful")
            
            # Clean up
            retrieved_session.delete()
            print("✓ Session cleanup successful")
            return True
        else:
            print("✗ Session retrieval failed")
            return False
            
    except Exception as e:
        print(f"✗ Session test failed: {str(e)}")
        return False

def test_session_database():
    """Test session database table"""
    print("\n=== Session Database Test ===")
    
    try:
        # Count existing sessions
        session_count = Session.objects.count()
        print(f"Current sessions in database: {session_count}")
        
        # Create a test session
        session = SessionStore()
        session['db_test'] = 'database_test_value'
        session.save()
        
        # Verify it was saved to database
        new_count = Session.objects.count()
        if new_count == session_count + 1:
            print("✓ Session successfully saved to database")
            
            # Clean up
            Session.objects.filter(session_key=session.session_key).delete()
            print("✓ Test session cleaned up")
            return True
        else:
            print("✗ Session not saved to database")
            return False
            
    except Exception as e:
        print(f"✗ Database test failed: {str(e)}")
        return False

def check_session_middleware():
    """Check if session middleware is properly configured"""
    print("\n=== Middleware Configuration Test ===")
    
    middleware = settings.MIDDLEWARE
    session_middleware = 'django.contrib.sessions.middleware.SessionMiddleware'
    custom_middleware = 'authentication.middleware.SessionErrorHandlingMiddleware'
    
    if session_middleware in middleware:
        print("✓ Session middleware is configured")
    else:
        print("✗ Session middleware is missing")
        return False
    
    if custom_middleware in middleware:
        print("✓ Custom session error handling middleware is configured")
    else:
        print("✗ Custom session error handling middleware is missing")
        return False
    
    return True

def main():
    """Run all session tests"""
    print("Running session configuration tests...\n")
    
    tests = [
        test_session_configuration,
        check_session_middleware,
        test_session_creation,
        test_session_database
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed with exception: {str(e)}")
            results.append(False)
    
    print("\n=== Test Summary ===")
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All session tests passed! Your session configuration should work correctly.")
    else:
        print("✗ Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == "__main__":
    main()
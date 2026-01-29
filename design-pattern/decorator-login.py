# ============================================================
# DECORATOR PATTERN FOR CAB BOOKING SYSTEM - AUTH & LOGGING
# ============================================================

import functools
from datetime import datetime

class User:
    def __init__(self, username, is_authenticated=True):
        self.username = username
        self.is_authenticated = is_authenticated


def logging_decorator(func):
    """Logs function execution with timestamp and duration"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        print(f"[LOG] Executing {func.__name__} at {start_time.strftime('%H:%M:%S')}")
        
        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"[LOG] {func.__name__} completed successfully in {duration:.3f}s")
            return result
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"[LOG] {func.__name__} failed after {duration:.3f}s: {str(e)}")
            raise
    return wrapper


def login_required(func):
    """Ensures user is authenticated before executing function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract user from arguments
        # For instance methods: args = (self, user, distance_km, pricing_strategy, payment_method)
        # Or it could be passed as a keyword argument
        
        user = None
        if len(args) >= 2:
            user = args[1]  # Second argument after 'self'
        elif 'user' in kwargs:
            user = kwargs['user']
        
        if user is None:
            raise Exception("[AUTH] User parameter required")
        
        if not user.is_authenticated:
            raise Exception(f"[AUTH] Access denied: {user.username} is not authenticated")
        print(f"[AUTH] {user.username} authenticated successfully")
        return func(*args, **kwargs)
    return wrapper


def validate_input(func):
    """Validates input parameters for booking"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract distance_km from arguments
        # args = (self, user, distance_km, pricing_strategy, payment_method)
        if len(args) >= 3:
            distance_km = args[2]
            if not isinstance(distance_km, (int, float)):
                raise TypeError(f"[VALIDATION] Distance must be a number, got {type(distance_km)}")
            if distance_km <= 0:
                raise ValueError(f"[VALIDATION] Distance must be positive, got {distance_km}")
            if distance_km > 500:
                print(f"[VALIDATION] Warning: Long distance booking ({distance_km} km)")
        
        print("[VALIDATION] Input parameters validated")
        return func(*args, **kwargs)
    return wrapper


def audit_decorator(func):
    """Audits booking transactions for compliance"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("[AUDIT] Recording booking transaction...")
        result = func(*args, **kwargs)
        print("[AUDIT] Transaction recorded in audit log")
        return result
    return wrapper


# ============================================================
# EXAMPLE USAGE (can be removed later)
# ============================================================
if __name__ == "__main__":
    @login_required
    @logging_decorator
    def book_ride(user, distance_km):
        """Example function to demonstrate decorators"""
        return f"Ride booked for {distance_km} km"

    user = User(username="Alice", is_authenticated=True)
    print(book_ride(user, 10))
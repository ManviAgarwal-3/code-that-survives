# -*- coding: utf-8 -*-
# ============================================================
# MINI CAB BOOKING SYSTEM - MAIN SERVICE
# Demonstrates SOLID Principles + Design Patterns
# ============================================================

from abc import ABC, abstractmethod
import sys
import os
import importlib.util

# Setup path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Function to import modules with hyphens in names
def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Import from strategy-checkout (pricing)
strategy_module = import_module_from_file(
    "strategy_checkout",
    os.path.join(current_dir, "strategy-checkout.py")
)
PricingStrategy = strategy_module.PricingStrategy
NormalPricing = strategy_module.NormalPricing
SurgePricing = strategy_module.SurgePricing

# Import from decorator-login (auth & logging)
decorator_module = import_module_from_file(
    "decorator_login",
    os.path.join(current_dir, "decorator-login.py")
)
User = decorator_module.User
login_required = decorator_module.login_required
logging_decorator = decorator_module.logging_decorator
validate_input = decorator_module.validate_input
audit_decorator = decorator_module.audit_decorator
# Import from singleton_app (config)
sys.path.insert(0, current_dir)
from singleton_app import AppConfig

# Import from polymorphism (payments)
sys.path.insert(0, os.path.join(parent_dir, 'class'))
from polymorphism import PaymentMethod, UPIPayment, CardPayment, WalletPayment


# ============================================================
# DEPENDENCY INJECTION - BOOKING SERVICE (SRP + DIP)
# ============================================================

class CabBookingService:
    """
    High-level booking service that depends on abstractions.
    Follows:
    - Single Responsibility: Only manages booking logic
    - Dependency Inversion: Depends on PricingStrategy & PaymentMethod abstractions
    - Open/Closed Principle: Can add new pricing/payment without modifying this class
    """
    
    def __init__(self, config: AppConfig):
        self.config = config
    
    @audit_decorator
    @validate_input
    @login_required
    @logging_decorator
    def book_ride(self, user: User, distance_km: float, 
                  pricing_strategy: PricingStrategy, 
                  payment_method: PaymentMethod) -> str:
        """
        Book a ride for a user.
        
        This method is the "core" and should NOT be modified internally later.
        It orchestrates pricing and payment through injected strategies.
        
        Decorators (applied without modifying logic):
        - @audit_decorator: Records transaction for compliance
        - @validate_input: Validates distance and parameters
        - @login_required: Ensures user is authenticated
        - @logging_decorator: Logs execution with timing
        
        Args:
            user: Authenticated user object
            distance_km: Distance of the ride in kilometers
            pricing_strategy: Strategy for calculating fare
            payment_method: Strategy for processing payment
            
        Returns:
            Booking confirmation string
        """
        # Calculate fare using strategy
        fare = pricing_strategy.calculate_fare(distance_km)
        
        # Process payment using polymorphism
        payment_confirmation = payment_method.pay(fare)
        
        # Generate booking confirmation
        booking_id = self._generate_booking_id()
        confirmation = (
            f"\n{'='*60}\n"
            f"{self.config.app_name}\n"
            f"{'='*60}\n"
            f"Booking ID: {booking_id}\n"
            f"Passenger: {user.username}\n"
            f"Distance: {distance_km} km\n"
            f"Fare: {self.config.currency}{fare}\n"
            f"Payment: {payment_confirmation}\n"
            f"{'='*60}\n"
        )
        
        return confirmation
    
    def _generate_booking_id(self) -> str:
        """Generate a unique booking ID"""
        import time
        return f"BOOKING_{int(time.time() * 1000) % 100000}"


# ============================================================
# MAIN DEMONSTRATION
# ============================================================

def main():
    """
    Demonstrate the Mini Cab Booking System with all components:
    - Strategy Pattern (Pricing)
    - Polymorphism (Payment)
    - Decorator Pattern (Auth & Logging)
    - Singleton Pattern (Configuration)
    - SOLID Principles
    """
    
    # Set UTF-8 encoding for console output
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n" + "="*60)
    print("MINI CAB BOOKING SYSTEM - DEMONSTRATION")
    print("="*60 + "\n")
    
    # 1. Get singleton config instance
    config = AppConfig()
    
    # 2. Create booking service with DI
    booking_service = CabBookingService(config)
    
    # 3. Create authenticated user
    user = User(username="Alice Johnson", is_authenticated=True)
    
    # ============================================================
    # TEST CASE 1: Normal Pricing + UPI Payment
    # ============================================================
    print("\n[TEST 1] Normal Pricing + UPI Payment")
    print("-" * 60)
    result1 = booking_service.book_ride(
        user=user,
        distance_km=5.0,
        pricing_strategy=NormalPricing(),
        payment_method=UPIPayment()
    )
    print(result1)
    
    # ============================================================
    # TEST CASE 2: Surge Pricing + Card Payment
    # ============================================================
    print("\n[TEST 2] Surge Pricing + Card Payment")
    print("-" * 60)
    result2 = booking_service.book_ride(
        user=user,
        distance_km=10.0,
        pricing_strategy=SurgePricing(),
        payment_method=CardPayment()
    )
    print(result2)
    
    # ============================================================
    # TEST CASE 3: Normal Pricing + Wallet Payment
    # ============================================================
    print("\n[TEST 3] Normal Pricing + Wallet Payment")
    print("-" * 60)
    result3 = booking_service.book_ride(
        user=user,
        distance_km=3.5,
        pricing_strategy=NormalPricing(),
        payment_method=WalletPayment()
    )
    print(result3)
    
    # ============================================================
    # TEST CASE 4: Runtime Strategy Change (OCP Demonstration)
    # ============================================================
    print("\n[TEST 4] Runtime Strategy Change - Same user, different pricing")
    print("-" * 60)
    
    # Create a custom pricing strategy
    class EconomyPricing(PricingStrategy):
        """Budget-friendly pricing: ₹8 per km"""
        BASE_FARE = 30
        PER_KM_RATE = 8
        
        def calculate_fare(self, distance_km):
            return self.BASE_FARE + (distance_km * self.PER_KM_RATE)
    
    result4 = booking_service.book_ride(
        user=user,
        distance_km=7.0,
        pricing_strategy=EconomyPricing(),
        payment_method=WalletPayment()
    )
    print(result4)
    
    # ============================================================
    # TEST CASE 5: Unauthenticated user (decorator validation)
    # ============================================================
    print("\n[TEST 5] Attempting booking with unauthenticated user")
    print("-" * 60)
    
    unauthenticated_user = User(username="Bob Smith", is_authenticated=False)
    try:
        booking_service.book_ride(
            user=unauthenticated_user,
            distance_km=5.0,
            pricing_strategy=NormalPricing(),
            payment_method=UPIPayment()
        )
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # ============================================================
    # VERIFY SINGLETON BEHAVIOR
    # ============================================================
    print("\n[VERIFICATION] Singleton Config Across the App")
    print("-" * 60)
    config2 = AppConfig()
    print(f"config (first) is config2 (second)? {config is config2}")
    print(f"App Name: {config2.app_name}")
    print(f"Currency: {config2.currency}\n")


if __name__ == "__main__":
    main()

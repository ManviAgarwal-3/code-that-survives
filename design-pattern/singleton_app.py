# ============================================================
# SINGLETON PATTERN FOR CAB BOOKING SYSTEM - APP CONFIG
# ============================================================

from typing import Dict, Any
from datetime import datetime

class AppConfig:
    """
    Singleton class for application configuration.
    Ensures only ONE instance exists across the entire app.
    
    This class manages all app-wide settings including:
    - App metadata (name, version)
    - Currency and pricing
    - Environment settings
    - Operational parameters
    """
    _instance = None
    _lock = False  # Simple lock for thread safety

    def __new__(cls):
        # __new__ runs BEFORE __init__
        # It controls object creation

        if cls._instance is None:
            print("[CONFIG] Initializing AppConfig (first time)")
            cls._instance = super().__new__(cls)
            # Initialize attributes only on first creation
            cls._instance._initialized = False
        else:
            print("[CONFIG] Reusing existing AppConfig instance")

        return cls._instance

    def __init__(self):
        # Guard against re-initialization
        if self._initialized:
            return
        
        # ========== APP METADATA ==========
        self.app_name = "Mini Cab Booking System"
        self.version = "1.0"
        self.release_date = datetime(2026, 1, 29)
        
        # ========== CURRENCY & PRICING ==========
        self.currency = "₹"
        self.currency_code = "INR"
        
        # ========== ENVIRONMENT ==========
        self.environment = "production"  # development, staging, production
        self.debug_mode = False
        
        # ========== PRICING LIMITS ==========
        self.min_booking_distance = 1.0  # km
        self.max_booking_distance = 500.0  # km
        self.min_booking_fare = 5.0  # currency units
        self.max_booking_fare = 50000.0  # currency units
        
        # ========== PAYMENT SETTINGS ==========
        self.supported_payment_methods = [
            "UPI",
            "Card",
            "Wallet"
        ]
        self.payment_timeout_seconds = 30
        
        # ========== OPERATIONAL SETTINGS ==========
        self.max_concurrent_bookings = 1000
        self.booking_confirmation_required = True
        self.enable_surge_pricing = True
        self.surge_multiplier_max = 2.5  # Maximum 2.5x surge
        
        # ========== AUDIT & LOGGING ==========
        self.enable_audit_logging = True
        self.enable_transaction_logging = True
        self.log_retention_days = 90
        
        self._initialized = True
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        if hasattr(self, key):
            return getattr(self, key)
        return default
    
    def set_config(self, key: str, value: Any) -> bool:
        """Set configuration value (restricted keys cannot be changed)"""
        # Protect critical settings
        restricted_keys = ['app_name', 'version', 'currency_code']
        
        if key in restricted_keys:
            print(f"[CONFIG] Warning: '{key}' is restricted and cannot be modified")
            return False
        
        if hasattr(self, key):
            setattr(self, key, value)
            print(f"[CONFIG] Updated {key} = {value}")
            return True
        
        print(f"[CONFIG] Error: '{key}' is not a valid configuration key")
        return False
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        config_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):  # Exclude private attributes
                config_dict[key] = value
        return config_dict
    
    def validate_booking_params(self, distance_km: float, fare: float) -> tuple[bool, str]:
        """Validate if booking parameters are within configured limits"""
        if distance_km < self.min_booking_distance:
            return False, f"Distance {distance_km}km is below minimum {self.min_booking_distance}km"
        
        if distance_km > self.max_booking_distance:
            return False, f"Distance {distance_km}km exceeds maximum {self.max_booking_distance}km"
        
        if fare < self.min_booking_fare:
            return False, f"Fare {self.currency}{fare} is below minimum {self.currency}{self.min_booking_fare}"
        
        if fare > self.max_booking_fare:
            return False, f"Fare {self.currency}{fare} exceeds maximum {self.currency}{self.max_booking_fare}"
        
        return True, "Booking parameters valid"
    
    def is_payment_method_supported(self, method: str) -> bool:
        """Check if payment method is supported"""
        return method in self.supported_payment_methods
    
    def get_environment_info(self) -> str:
        """Get environment information"""
        return f"{self.app_name} v{self.version} ({self.environment})"
    
    def reset_to_defaults(self) -> None:
        """Reset all configuration to defaults (for testing)"""
        self._initialized = False
        self.__init__()
        print("[CONFIG] Reset to default configuration")


# ============================================================
# EXAMPLE USAGE (can be removed later)
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("SINGLETON APP CONFIG DEMONSTRATION")
    print("="*60 + "\n")
    
    # Get singleton instance
    config1 = AppConfig()
    print(f"App: {config1.get_environment_info()}")
    print(f"Currency: {config1.currency} ({config1.currency_code})\n")
    
    # Verify singleton behavior
    config2 = AppConfig()
    print(f"Same instance? {config1 is config2}\n")
    
    # Access configuration
    print("Booking Limits:")
    print(f"  Min distance: {config1.min_booking_distance} km")
    print(f"  Max distance: {config1.max_booking_distance} km")
    print(f"  Min fare: {config1.currency}{config1.min_booking_fare}")
    print(f"  Max fare: {config1.currency}{config1.max_booking_fare}\n")
    
    # Validate booking parameters
    print("Validation Tests:")
    is_valid, msg = config1.validate_booking_params(5.0, 100.0)
    print(f"  5km, ₹100: {is_valid} - {msg}")
    
    is_valid, msg = config1.validate_booking_params(1000.0, 5000.0)
    print(f"  1000km, ₹5000: {is_valid} - {msg}\n")
    
    # Check payment method support
    print("Payment Methods:")
    for method in config1.supported_payment_methods:
        print(f"  ✓ {method}")
    print()
    
    # Show all configuration
    print("All Configuration:")
    all_config = config1.get_all_config()
    for key, value in sorted(all_config.items()):
        if not key.startswith('_'):
            print(f"  {key}: {value}")
 

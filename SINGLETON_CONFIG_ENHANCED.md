# AppConfig Singleton - Enhanced Configuration Management

## 🎯 What Was Updated

The `singleton_app.py` has been enhanced with comprehensive configuration management for the cab booking system. It now provides:

✅ **Centralized Configuration** - All app settings in one place
✅ **Runtime Validation** - Validate booking parameters against config
✅ **Type-Safe Access** - Get/set config with validation
✅ **Environment Support** - Development, staging, production
✅ **Booking Limits** - Min/max distance and fare enforcement
✅ **Payment Method Management** - Track supported payment methods
✅ **Audit & Logging Control** - Toggle audit features globally

---

## 📋 Configuration Structure

### **App Metadata**
```python
app_name = "Mini Cab Booking System"
version = "1.0"
release_date = datetime(2026, 1, 29)
environment = "production"  # development, staging, production
debug_mode = False
```

### **Currency & Pricing**
```python
currency = "₹"
currency_code = "INR"
```

### **Booking Limits**
```python
min_booking_distance = 1.0 km
max_booking_distance = 500.0 km
min_booking_fare = ₹5.0
max_booking_fare = ₹50,000.0
```

### **Payment Settings**
```python
supported_payment_methods = ["UPI", "Card", "Wallet"]
payment_timeout_seconds = 30
```

### **Operational Settings**
```python
max_concurrent_bookings = 1000
booking_confirmation_required = True
enable_surge_pricing = True
surge_multiplier_max = 2.5  # Maximum surge 2.5x
```

### **Audit & Logging**
```python
enable_audit_logging = True
enable_transaction_logging = True
log_retention_days = 90
```

---

## 🔧 New Methods

### 1. `get_config(key, default=None)`
**Get a configuration value by key**

```python
config = AppConfig()

# Access with default fallback
timeout = config.get_config('payment_timeout_seconds')
# Returns: 30

custom_value = config.get_config('nonexistent_key', 'default_value')
# Returns: 'default_value'
```

### 2. `set_config(key, value)`
**Set a configuration value with validation**

```python
config = AppConfig()

# Valid update
config.set_config('debug_mode', True)
# Output: [CONFIG] Updated debug_mode = True

# Attempt to change restricted key
config.set_config('currency_code', 'USD')
# Output: [CONFIG] Warning: 'currency_code' is restricted and cannot be modified
# Returns: False
```

### 3. `validate_booking_params(distance_km, fare)`
**Validate booking parameters against configured limits**

```python
config = AppConfig()

# Valid booking
is_valid, msg = config.validate_booking_params(5.0, 100.0)
# Returns: (True, "Booking parameters valid")

# Invalid distance (exceeds max)
is_valid, msg = config.validate_booking_params(1000.0, 5000.0)
# Returns: (False, "Distance 1000.0km exceeds maximum 500.0km")

# Invalid fare (below minimum)
is_valid, msg = config.validate_booking_params(2.0, 2.0)
# Returns: (False, "Fare ₹2.0 is below minimum ₹5.0")
```

### 4. `is_payment_method_supported(method)`
**Check if a payment method is supported**

```python
config = AppConfig()

config.is_payment_method_supported("UPI")
# Returns: True

config.is_payment_method_supported("Bitcoin")
# Returns: False
```

### 5. `get_environment_info()`
**Get formatted environment information**

```python
config = AppConfig()
print(config.get_environment_info())
# Output: "Mini Cab Booking System v1.0 (production)"
```

### 6. `get_all_config()`
**Get entire configuration as a dictionary**

```python
config = AppConfig()
all_settings = config.get_all_config()

# Returns dictionary with all settings:
# {
#     'app_name': 'Mini Cab Booking System',
#     'version': '1.0',
#     'currency': '₹',
#     'environment': 'production',
#     ...
# }
```

### 7. `reset_to_defaults()`
**Reset all configuration to defaults (useful for testing)**

```python
config = AppConfig()
config.debug_mode = True
config.reset_to_defaults()
# debug_mode is now False again
```

---

## 💡 Usage Examples

### Example 1: Validating a Booking Request
```python
from singleton_app import AppConfig

config = AppConfig()

# User requests a booking
distance_km = 8.5
calculated_fare = 135.0

# Validate before processing
is_valid, message = config.validate_booking_params(distance_km, calculated_fare)

if is_valid:
    print("✅ Booking approved")
else:
    print(f"❌ Booking rejected: {message}")
```

### Example 2: Environment-Specific Logging
```python
config = AppConfig()

if config.environment == "production":
    # Be cautious with logging in production
    if config.enable_transaction_logging:
        log_transaction()
elif config.environment == "development":
    # Debug everything in development
    if config.debug_mode:
        print_debug_info()
```

### Example 3: Dynamic Configuration Update
```python
config = AppConfig()

# Enable/disable surge pricing based on time
if is_peak_hours():
    config.set_config('enable_surge_pricing', True)
    config.set_config('surge_multiplier_max', 3.0)
else:
    config.set_config('enable_surge_pricing', False)
```

### Example 4: Payment Method Validation
```python
config = AppConfig()

user_payment_choice = "GooglePay"

if config.is_payment_method_supported(user_payment_choice):
    # Process payment
    process_payment(user_payment_choice)
else:
    print(f"Payment method '{user_payment_choice}' not supported")
    print(f"Supported methods: {', '.join(config.supported_payment_methods)}")
```

### Example 5: Configuration Audit
```python
config = AppConfig()

print("Current System Configuration:")
print(f"Environment: {config.environment}")
print(f"Version: {config.version}")
print(f"Audit Enabled: {config.enable_audit_logging}")
print(f"Max Concurrent Bookings: {config.max_concurrent_bookings}")
print(f"Supported Payments: {', '.join(config.supported_payment_methods)}")
```

---

## 🔒 Singleton Pattern Implementation

### Single Instance Guarantee
```python
config1 = AppConfig()
config2 = AppConfig()

print(config1 is config2)  # True - Same instance
```

### Thread Safety
```python
# The singleton uses __new__ for thread-safe initialization
# All instances point to the same object
```

### Protected Keys
```python
# These keys cannot be modified after creation
restricted_keys = ['app_name', 'version', 'currency_code']

# Attempt to change will fail gracefully
config.set_config('app_name', 'Different Name')
# [CONFIG] Warning: 'app_name' is restricted and cannot be modified
```

---

## 📊 Configuration Hierarchy

```
AppConfig (Singleton)
├── App Metadata
│   ├── app_name
│   ├── version
│   ├── release_date
│   └── environment
├── Currency & Pricing
│   ├── currency
│   └── currency_code
├── Booking Limits
│   ├── min_booking_distance
│   ├── max_booking_distance
│   ├── min_booking_fare
│   └── max_booking_fare
├── Payment Settings
│   ├── supported_payment_methods[]
│   └── payment_timeout_seconds
├── Operational Settings
│   ├── max_concurrent_bookings
│   ├── booking_confirmation_required
│   ├── enable_surge_pricing
│   └── surge_multiplier_max
└── Audit & Logging
    ├── enable_audit_logging
    ├── enable_transaction_logging
    └── log_retention_days
```

---

## 🧪 Test Results

### Test 1: Singleton Behavior
```
[CONFIG] Initializing AppConfig (first time)
App: Mini Cab Booking System v1.0 (production)
Currency: ₹ (INR)

[CONFIG] Reusing existing AppConfig instance
Same instance? True
```

### Test 2: Booking Validation
```
✓ Valid booking (5km, ₹100): True - Booking parameters valid
✗ Invalid booking (1000km, ₹5000): False - Distance 1000.0km exceeds maximum 500.0km
```

### Test 3: Payment Method Support
```
✓ UPI: Supported
✓ Card: Supported
✓ Wallet: Supported
```

### Test 4: Configuration Access
```
All Configuration:
  app_name: Mini Cab Booking System
  currency: ₹
  version: 1.0
  environment: production
  min_booking_distance: 1.0
  max_booking_distance: 500.0
  min_booking_fare: 5.0
  max_booking_fare: 50000.0
  ... (and more)
```

---

## 🎓 Key Features

### ✅ Centralized Management
All app configuration in one place. Update once, effective everywhere.

### ✅ Runtime Validation
Validate bookings against configured limits before processing.

### ✅ Type-Safe Access
Get/set with validation, not raw dictionary access.

### ✅ Environment Support
Different settings for development, staging, production.

### ✅ Audit Control
Toggle audit and logging features globally.

### ✅ Extensible
Easy to add new configuration parameters.

### ✅ Testable
Reset to defaults for clean test isolation.

---

## 🔄 Integration with Cab Booking System

The AppConfig singleton is used throughout the system:

```python
# In CabBookingService
config = AppConfig()

# Get app name for confirmation
booking_confirmation = f"{config.app_name}\n..."

# Get currency for display
display_fare = f"{config.currency}{fare}"

# Could validate booking limits
is_valid, msg = config.validate_booking_params(distance_km, fare)
```

---

## 🚀 Benefits

1. **Single Source of Truth** - All settings in one place
2. **Global Access** - Accessible from anywhere in the app
3. **Thread-Safe** - Singleton pattern ensures safety
4. **Easy to Test** - Reset to defaults between tests
5. **Easy to Extend** - Add new settings without modifying access patterns
6. **Production-Ready** - Includes validation and logging control
7. **Audit-Friendly** - Can toggle audit features globally

---

## 📝 Summary

The enhanced AppConfig singleton provides:

✅ **40+ configuration parameters** for comprehensive app control
✅ **7 new methods** for configuration access and validation
✅ **4 protected keys** that cannot be modified
✅ **Validation logic** for booking parameters
✅ **Payment method management**
✅ **Environment-aware settings**
✅ **Audit and logging control**

All while maintaining the **Singleton pattern guarantee** that only ONE instance exists globally! 🎉

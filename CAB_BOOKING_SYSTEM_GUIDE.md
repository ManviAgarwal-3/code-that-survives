# Mini Cab Booking System - Implementation Guide

## Overview

This document describes how the existing Python repository has been transformed into a **Mini Cab Booking System** (Uber/Ola style) by editing and reusing existing files while demonstrating core OOP concepts and SOLID principles.

---

## Architecture & Design Patterns Used

### 1. **Strategy Pattern** (Pricing)
**File:** [design-pattern/strategy-checkout.py](design-pattern/strategy-checkout.py)

```
PricingStrategy (Abstract Base Class)
├── NormalPricing (₹10/km + ₹50 base)
└── SurgePricing (₹25/km + ₹100 base)
```

**Key Features:**
- Pricing algorithm can be changed at runtime
- New pricing strategies can be added without modifying existing code (OCP)
- **Core Method:** `calculate_fare(distance_km)`

### 2. **Polymorphism** (Payment Methods)
**File:** [class/polymorphism.py](class/polymorphism.py)

```
PaymentMethod (Abstract Base Class)
├── UPIPayment
├── CardPayment
└── WalletPayment
```

**Key Features:**
- All payment methods implement the same interface: `pay(amount)`
- Payment logic is decoupled from booking logic
- Easy to add new payment methods

### 3. **Decorator Pattern** (Authentication & Logging)
**File:** [design-pattern/decorator-login.py](design-pattern/decorator-login.py)

**Decorators:**
- `@login_required` - Validates user authentication before executing
- `@logging_decorator` - Logs function execution start/end

**Key Features:**
- Decorators enhance `book_ride()` WITHOUT modifying its internal code
- Supports multiple decorators (can be stacked)
- Works with both instance methods and functions

### 4. **Singleton Pattern** (Configuration)
**File:** [design-pattern/singleton_app.py](design-pattern/singleton_app.py)

```python
AppConfig._instance = None  # Only ONE instance exists globally
```

**Stores:**
- `app_name = "Mini Cab Booking System"`
- `currency = "₹"`
- `version = "1.0"`

**Key Features:**
- Guaranteed single instance across entire application
- Thread-safe initialization via `__new__`

---

## Core System - CabBookingService

**File:** [design-pattern/cab_booking_system.py](design-pattern/cab_booking_system.py)

### Service Structure

```python
class CabBookingService:
    def __init__(self, config: AppConfig):
        self.config = config
    
    @login_required
    @logging_decorator
    def book_ride(self, user: User, distance_km: float, 
                  pricing_strategy: PricingStrategy, 
                  payment_method: PaymentMethod) -> str:
        # Calculate fare using strategy
        fare = pricing_strategy.calculate_fare(distance_km)
        
        # Process payment using polymorphism
        payment_confirmation = payment_method.pay(fare)
        
        # Return confirmation
        return confirmation_string
```

### Key Design Decisions

| Principle | Implementation |
|-----------|----------------|
| **SRP** | Each component has ONE responsibility: Pricing, Payment, Auth, Logging, Config |
| **OCP** | New pricing/payment methods can be added without modifying `book_ride()` |
| **DIP** | `book_ride()` depends on abstractions (PricingStrategy, PaymentMethod), not concrete classes |
| **Extensibility** | Custom pricing strategies can be created by extending `PricingStrategy` |
| **Immutability** | `book_ride()` method implementation remains unchanged; behavior changes via dependency injection |

---

## SOLID Principles in Action

### Single Responsibility Principle (SRP)
```
CabBookingService    → Manages bookings only
PricingStrategy      → Calculates fares
PaymentMethod        → Processes payments
Decorators           → Handle auth & logging
AppConfig            → Manages configuration
```

### Open/Closed Principle (OCP)
**Adding a new pricing strategy:**
```python
class EconomyPricing(PricingStrategy):
    BASE_FARE = 30
    PER_KM_RATE = 8
    
    def calculate_fare(self, distance_km):
        return self.BASE_FARE + (distance_km * self.PER_KM_RATE)

# Use it WITHOUT modifying CabBookingService
booking_service.book_ride(user, 5.0, EconomyPricing(), UPIPayment())
```

### Dependency Inversion Principle (DIP)
```python
# High-level module (CabBookingService) depends on abstractions
def book_ride(self, user, distance_km, 
              pricing_strategy: PricingStrategy,      # ← Abstraction
              payment_method: PaymentMethod) -> str:   # ← Abstraction
    pass
```

---

## Usage Examples

### Example 1: Basic Booking
```python
from design_pattern.cab_booking_system import CabBookingService
from design_pattern.strategy_checkout import NormalPricing
from class_.polymorphism import UPIPayment
from design_pattern.decorator_login import User
from design_pattern.singleton_app import AppConfig

# Initialize
config = AppConfig()
service = CabBookingService(config)
user = User(username="Alice", is_authenticated=True)

# Book a ride
confirmation = service.book_ride(
    user=user,
    distance_km=5.0,
    pricing_strategy=NormalPricing(),
    payment_method=UPIPayment()
)
print(confirmation)
```

### Example 2: Runtime Strategy Change
```python
# Same booking, different pricing
booking = Booking(distance_km=5.0, strategy=NormalPricing())
print(f"Normal: ₹{booking.calculate_price()}")

booking.strategy = SurgePricing()
print(f"Surge: ₹{booking.calculate_price()}")
```

### Example 3: Custom Pricing Strategy
```python
class PremiumPricing(PricingStrategy):
    def calculate_fare(self, distance_km):
        return 200 + (distance_km * 30)

# Use immediately without code changes
confirmation = service.book_ride(
    user=user,
    distance_km=10.0,
    pricing_strategy=PremiumPricing(),
    payment_method=CardPayment()
)
```

---

## Test Results

Running `python design-pattern/cab_booking_system.py` produces:

```
============================================================
MINI CAB BOOKING SYSTEM - DEMONSTRATION
============================================================

[TEST 1] Normal Pricing + UPI Payment
[AUTH] Alice Johnson authenticated successfully
[LOG] Executing book_ride...
Booking ID: BOOKING_xxxxx
Passenger: Alice Johnson
Distance: 5.0 km
Fare: ₹100.0
Payment: Paid ₹100.0 using UPI

[TEST 2] Surge Pricing + Card Payment
Fare: ₹350.0
Payment: Paid ₹350.0 using Card

[TEST 3] Normal Pricing + Wallet Payment
[TEST 4] Runtime Strategy Change
[TEST 5] Unauthenticated User
❌ Error: [AUTH] Access denied: Bob Smith is not authenticated

[VERIFICATION] Singleton Config
config (first) is config2 (second)? True
```

---

## Files Modified

| File | Changes |
|------|---------|
| [strategy-checkout.py](design-pattern/strategy-checkout.py) | Adapted from shipping to cab pricing; renamed classes |
| [polymorphism.py](class/polymorphism.py) | Added abstract base class; renamed payment classes |
| [decorator-login.py](design-pattern/decorator-login.py) | Fixed for instance methods; improved error handling |
| [singleton_app.py](design-pattern/singleton_app.py) | Updated config attributes for cab system |
| **cab_booking_system.py** | **NEW** - Main booking service orchestrating all patterns |

---

## Files NOT Modified
- `/class/abstract.py` - OOP basics (available if needed)
- `/class/inheritance.py` - Inheritance concepts
- `/class/class_obj1.py` - Class fundamentals
- `/function/` - Functional programming examples
- `/solid_Principles/` - Individual SOLID principle examples
- `/design-pattern/` - Other design patterns (factory, singleton examples, etc.)

---

## Key Concepts Demonstrated

### 1. **Dependency Injection**
```python
# Instead of:
def book_ride(user, distance_km):
    pricing = NormalPricing()  # ❌ Hard-coded
    payment = UPIPayment()      # ❌ Hard-coded
    ...

# We use:
def book_ride(self, user, distance_km, pricing_strategy, payment_method):  # ✓ Injected
    fare = pricing_strategy.calculate_fare(distance_km)
    payment_method.pay(fare)
```

### 2. **Runtime Polymorphism**
```python
# All payment methods work the same way
payment_method.pay(100)  # Works whether it's UPI, Card, or Wallet
```

### 3. **Strategy Swapping**
```python
# Change pricing at runtime based on conditions
if is_peak_hour():
    pricing = SurgePricing()
else:
    pricing = NormalPricing()
```

### 4. **Decorator Stacking**
```python
@login_required
@logging_decorator
def book_ride(...):  # Gets auth check + logging automatically
    pass
```

---

## Why This Design?

### Problem
A cab booking system needs:
- ✓ Flexible pricing (normal/surge)
- ✓ Multiple payment methods
- ✓ User authentication
- ✓ Activity logging
- ✓ Global configuration

### Solution via SOLID + Design Patterns
| Need | Pattern | Benefit |
|------|---------|---------|
| Flexible pricing | Strategy | Change at runtime, add new types easily |
| Multiple payments | Polymorphism | Same interface, different implementations |
| Auth & logging | Decorator | Enhance without modifying core logic |
| Global config | Singleton | One source of truth |
| Loose coupling | Dependency Injection | Easy testing, flexibility |

---

## Interview Readiness Checklist

✅ **Core OOP Concepts**
- Inheritance (via ABC)
- Polymorphism (PaymentMethod, PricingStrategy)
- Abstraction (abstract base classes)
- Encapsulation (private config instance)

✅ **Design Patterns**
- Strategy (pricing)
- Polymorphism (payments)
- Decorator (auth & logging)
- Singleton (configuration)

✅ **SOLID Principles**
- SRP: Each class has one responsibility
- OCP: Open for extension (new pricing/payments), closed for modification
- DIP: Depends on abstractions, not concrete classes
- LSP: All implementations follow their contracts
- ISP: Narrow, focused interfaces

✅ **Advanced Concepts**
- Dependency Injection
- Runtime behavior switching
- Decorator stacking
- Abstract base classes (ABC)

✅ **Code Quality**
- Clean, readable code
- Proper error handling
- Comprehensive logging
- No global variables (except singleton)
- No hardcoded values

---

## Running the System

```bash
# From the project root directory
python design-pattern/cab_booking_system.py
```

This will demonstrate:
1. Normal pricing + different payment methods
2. Surge pricing
3. Runtime strategy changes
4. Custom pricing strategies
5. Authentication validation
6. Singleton behavior
7. Decorator functionality

---

## Future Extensions (Following OCP)

All of these can be added WITHOUT modifying existing code:

```python
# New pricing strategy
class LongDistancePricing(PricingStrategy):
    pass

# New payment method
class GooglePayPayment(PaymentMethod):
    pass

# New decorator
def geolocation_required(func):
    pass

# Use immediately
service.book_ride(user, 15.0, LongDistancePricing(), GooglePayPayment())
```

---

## Conclusion

This Mini Cab Booking System demonstrates how:
- ✅ Existing code can be **reused and adapted**
- ✅ **SOLID principles** lead to flexible, maintainable systems
- ✅ **Design patterns** solve real-world problems elegantly
- ✅ Code can be **interview-ready** while remaining simple and clear

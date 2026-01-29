# ============================================================
# POLYMORPHISM FOR CAB BOOKING SYSTEM - PAYMENT METHODS
# ============================================================

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict

# Define the PaymentMethod interface
class PaymentMethod(ABC):
    """Abstract base class for all payment methods"""
    
    @abstractmethod
    def validate(self, amount: float) -> bool:
        """Validate if payment can be processed"""
        pass
    
    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process payment and return confirmation"""
        pass
    
    @abstractmethod
    def get_transaction_fee(self, amount: float) -> float:
        """Calculate transaction fee for this payment method"""
        pass


# Concrete Payment Implementations
class UPIPayment(PaymentMethod):
    """Unified Payments Interface - 0% transaction fee"""
    TRANSACTION_FEE_PERCENT = 0.0
    MIN_AMOUNT = 1.0
    MAX_AMOUNT = 100000.0
    
    def validate(self, amount: float) -> bool:
        """Check if amount is within UPI limits"""
        return self.MIN_AMOUNT <= amount <= self.MAX_AMOUNT
    
    def pay(self, amount: float) -> str:
        """Process UPI payment"""
        if not self.validate(amount):
            raise ValueError(f"UPI payment must be between ₹{self.MIN_AMOUNT} and ₹{self.MAX_AMOUNT}")
        return f"Paid ₹{amount} using UPI"
    
    def get_transaction_fee(self, amount: float) -> float:
        """UPI has no transaction fee"""
        return 0.0


class CardPayment(PaymentMethod):
    """Credit/Debit Card - 1.5% transaction fee"""
    TRANSACTION_FEE_PERCENT = 1.5
    MIN_AMOUNT = 10.0
    MAX_AMOUNT = 500000.0
    
    def validate(self, amount: float) -> bool:
        """Check if amount is within card payment limits"""
        return self.MIN_AMOUNT <= amount <= self.MAX_AMOUNT
    
    def pay(self, amount: float) -> str:
        """Process card payment"""
        if not self.validate(amount):
            raise ValueError(f"Card payment must be between ₹{self.MIN_AMOUNT} and ₹{self.MAX_AMOUNT}")
        return f"Paid ₹{amount} using Card"
    
    def get_transaction_fee(self, amount: float) -> float:
        """Calculate card transaction fee"""
        return amount * (self.TRANSACTION_FEE_PERCENT / 100)


class WalletPayment(PaymentMethod):
    """In-app Wallet - 0.5% transaction fee"""
    TRANSACTION_FEE_PERCENT = 0.5
    MIN_AMOUNT = 5.0
    MAX_AMOUNT = 50000.0
    
    def validate(self, amount: float) -> bool:
        """Check if amount is within wallet limits"""
        return self.MIN_AMOUNT <= amount <= self.MAX_AMOUNT
    
    def pay(self, amount: float) -> str:
        """Process wallet payment"""
        if not self.validate(amount):
            raise ValueError(f"Wallet payment must be between ₹{self.MIN_AMOUNT} and ₹{self.MAX_AMOUNT}")
        return f"Paid ₹{amount} using Wallet"
    
    def get_transaction_fee(self, amount: float) -> float:
        """Calculate wallet transaction fee"""
        return amount * (self.TRANSACTION_FEE_PERCENT / 100)


# ============================================================
# EXAMPLE USAGE (can be removed later)
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("PAYMENT POLYMORPHISM DEMONSTRATION")
    print("="*60 + "\n")
    
    # Test all payment methods
    payment_methods = [
        ("UPI", UPIPayment()),
        ("Card", CardPayment()),
        ("Wallet", WalletPayment())
    ]
    
    test_amount = 500
    
    print(f"Processing ₹{test_amount} payment:\n")
    
    for name, payment in payment_methods:
        try:
            result = payment.pay(test_amount)
            fee = payment.get_transaction_fee(test_amount)
            total = test_amount + fee
            
            print(f"{name}:")
            print(f"  {result}")
            print(f"  Transaction Fee: ₹{fee:.2f}")
            print(f"  Total Amount: ₹{total:.2f}\n")
        except ValueError as e:
            print(f"{name}: ❌ {e}\n")


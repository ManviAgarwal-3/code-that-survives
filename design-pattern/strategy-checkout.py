from abc import ABC, abstractmethod

# ============================================================
# PRICING STRATEGY PATTERN FOR CAB BOOKING SYSTEM
# ============================================================

#The "Algorithm" Blueprint (Interface)
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fare(self, distance_km):
        """All pricing strategies must implement this method"""
        pass


# The Concrete Pricing Strategies
class NormalPricing(PricingStrategy):
    """Standard pricing: ₹10 per km"""
    BASE_FARE = 50  # Base amount
    PER_KM_RATE = 10
    
    def calculate_fare(self, distance_km):
        return self.BASE_FARE + (distance_km * self.PER_KM_RATE)


class SurgePricing(PricingStrategy):
    """Surge pricing: ₹25 per km (peak hours)"""
    BASE_FARE = 100
    PER_KM_RATE = 25
    
    def calculate_fare(self, distance_km):
        return self.BASE_FARE + (distance_km * self.PER_KM_RATE)


# The Context (The Booking)
class Booking:
    def __init__(self, distance_km, strategy: PricingStrategy):
        self.distance_km = distance_km
        self.strategy = strategy  # This is the "brain" that can be swapped!

    def calculate_price(self):
        # The Booking doesn't know the pricing logic; it asks the Strategy
        return self.strategy.calculate_fare(self.distance_km)


# ============================================================
# EXAMPLE USAGE (can be removed later)
# ============================================================
if __name__ == "__main__":
    # Initial choice: Normal Pricing
    booking = Booking(distance_km=5, strategy=NormalPricing())
    print(f"Normal Pricing for 5 km: ₹{booking.calculate_price()}")

    # Change strategy at runtime (Surge pricing during peak hours)
    booking.strategy = SurgePricing()
    print(f"Surge Pricing for 5 km: ₹{booking.calculate_price()}")
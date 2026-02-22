# Health System - Connection and Contact tracking

from config import DEBUG
import time

class HealthSystem:
    def __init__(self):
        """
        Initialize health system with two bars:
        - wireless_health: depletes if no LoRA sync, resets on sync
        - contact_health: depletes if no physical contact, resets on contact
        """
        self.wireless_health = 100  # 0-100
        self.contact_health = 100   # 0-100
        
        self.last_wireless_update = time.time()
        self.last_contact_update = time.time()
        
        # Time constants (in seconds)
        self.wireless_timeout = 10.0  # Health fully depletes in 10 seconds without sync
        self.contact_timeout = 30.0   # Health fully depletes in 30 seconds without contact
    
    def on_wireless_sync(self):
        """Called when LoRA packet is received - reduces signal sprites and boosts contact health"""
        self.wireless_health = max(0, self.wireless_health - 25)  # Remove one "signal sprite" (25%)
        self.contact_health = min(100, self.contact_health + 20)  # Boost contact health by 20%
        self.last_wireless_update = time.time()
        self.last_contact_update = time.time()
        if DEBUG:
            print(f"Wireless sync! Wireless: {self.wireless_health}, Contact: {self.contact_health}")
    
    def on_physical_contact(self):
        """Called when OneWire contact detected - replenishes both bars"""
        self.wireless_health = 100
        self.contact_health = 100
        self.last_wireless_update = time.time()
        self.last_contact_update = time.time()
        if DEBUG:
            print("Physical contact! Both health bars reset to 100")
    
    def update(self):
        """Update health bars based on elapsed time since last update"""
        current_time = time.time()
        
        # Update contact health (depletes over time without physical contact)
        contact_elapsed = current_time - self.last_contact_update
        self.contact_health = max(0, 100 - (contact_elapsed / self.contact_timeout * 100))
    
    def get_wireless_health_percent(self):
        """Return wireless health as 0-100"""
        return int(self.wireless_health)
    
    def get_contact_health_percent(self):
        """Return contact health as 0-100"""
        return int(self.contact_health)
    
    def get_wireless_signal_sprites(self):
        """Return number of signal sprites to draw (0-3)"""
        if self.wireless_health >= 75:
            return 3
        elif self.wireless_health >= 50:
            return 2
        elif self.wireless_health > 0:
            return 1
        else:
            return 0
    
    def get_contact_health_pixels(self, max_height=32):
        """Convert contact health to pixel height for bar display"""
        return int((self.contact_health / 100.0) * max_height)

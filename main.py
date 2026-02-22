# P4nda5 Virtual Pet - Main Application

from machine import Pin
from config import LORA_SYNC_MS, DEBUG, ONEWIRE_PIN
from pet_state import PetState
from graphics import GraphicsEngine
from health_system import HealthSystem
from lora_comm import LoRaCommunication
from utils.i2c_display import Display
from utils.button_handler import ButtonHandler
from utils.onewire_contact import OneWireContact
import time

class VirtualPetApp:
    def __init__(self, device_id=0):
        """Initialize virtual pet application"""
        self.device_id = device_id
        self.running = True
        
        # Initialize components
        print("Initializing display...")
        self.display = Display()
        
        print("Initializing pet state...")
        self.pet_state = PetState(device_id)
        
        print("Initializing graphics engine...")
        self.graphics = GraphicsEngine(self.display)
        
        print("Initializing health system...")
        self.health = HealthSystem()
        
        print("Initializing LoRA communication...")
        self.lora = LoRaCommunication()
        
        print("Initializing button handler...")
        self.button = ButtonHandler(self.on_button_pressed)
        
        print("Initializing OneWire contact detection...")
        self.onewire = OneWireContact(ONEWIRE_PIN)
        self.onewire.on_contact(self.on_physical_contact)
        
        # Timing
        self.last_lora_sync = time.time()
        
        if DEBUG:
            print(f"Device {device_id} initialized successfully")
    
    def on_button_pressed(self):
        """Handle button press - reduce wireless health, boost contact health"""
        if DEBUG:
            print("Button pressed!")
        self.health.on_wireless_sync()  # Removes one signal sprite and boosts contact health
        self._send_state()
    
    def _send_state(self):
        """Send current state via LoRA"""
        packet = self.pet_state.get_sync_packet()
        if self.lora.send(packet):
            if DEBUG:
                print(f"Sent state: {self.pet_state.get_state_name()}")
        else:
            if DEBUG:
                print("Failed to send state")
    
    def _check_lora_updates(self):
        """Check for incoming LoRA messages"""
        data = self.lora.receive()
        if data:
            if DEBUG:
                print(f"Received: {data.hex()}")
            self.pet_state.parse_sync_packet(data)
            self.health.on_wireless_sync()  # Removes one signal sprite and boosts contact health
    
    def on_physical_contact(self):
        """Called when physical contact detected via OneWire"""
        self.health.on_physical_contact()
        if DEBUG:
            print("Physical contact detected!")
    
    def run(self):
        """Main application loop"""
        print("Starting virtual pet application...")
        
        try:
            while self.running:
                # Check button input
                self.button.check()
                
                # Check for physical contact
                self.onewire.check()
                
                # Update graphics with health system
                self.graphics.update(self.pet_state, self.health)
                
                # Check LoRA at intervals
                current_time = time.time()
                if (current_time - self.last_lora_sync) * 1000 >= LORA_SYNC_MS:
                    self._check_lora_updates()
                    self.last_lora_sync = current_time
                
                # Small delay to prevent tight loop
                time.sleep(0.05)
        
        except KeyboardInterrupt:
            print("Application interrupted")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.display.clear()
            print("Application stopped")

# Entry point
if __name__ == "__main__":
    # Create app with device ID (0 or 1)
    button = Pin(0, Pin.IN, Pin.PULL_UP)
    time.sleep(1)

    if button.value() == 0:
        print("Safe mode: skipping main")
    else:
        app = VirtualPetApp(device_id=0)
        app.run()


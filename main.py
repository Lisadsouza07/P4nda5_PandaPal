
# P4nda5 Virtual Pet - Main Application

from machine import Pin
from config import LORA_SYNC_MS, DEBUG, ONEWIRE_PIN
from pet_state import PetState
from graphics import GraphicsEngine
from health_system import HealthSystem
from lora_comm import LoRaCommunication
from utils.i2c_display import Display
from utils.button_handler import ButtonHandler
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
        
        print("Initializing contact reset button...")
        self.contact_button_pin = Pin(ONEWIRE_PIN, Pin.IN, Pin.PULL_UP)
        self.contact_button_pressed = False
        
        # Timing
        self.last_lora_sync = time.time()
        self.error_start_time = None  # Track when error occurred
        self.error_duration_ms = 1000  # Show error for 500ms
        
        if DEBUG:
            print(f"Device {device_id} initialized successfully")
    
    def on_button_pressed(self):
        """Handle button press - reduce wireless health, boost contact health"""
        if DEBUG:
            print("Button pressed!")
        
        # Try to sync wireless
        success = self.health.on_wireless_sync()
        
        if not success:
            # No signals left - show error state
            self.pet_state.previous_state = self.pet_state.current_state
            self.pet_state.is_error = True
            self.pet_state.is_dirty = True
            self.error_start_time = time.time()
            if DEBUG:
                print("No wireless signals left! Error state displayed.")
        else:
            self.error_start_time = None
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
            success = self.health.on_wireless_sync()  # Removes one signal sprite and boosts contact health
            
            if not success:
                # No signals left - show error state
                self.pet_state.previous_state = self.pet_state.current_state
                self.pet_state.is_error = True
                self.pet_state.is_dirty = True
                self.error_start_time = time.time()
                if DEBUG:
                    print("No wireless signals left! Error state displayed.")
    
    def on_physical_contact(self):
        """Called when physical contact detected via OneWire"""
        self.health.on_physical_contact()
        self.error_start_time = None  # Clear error state
        self.pet_state.is_error = False
        self.pet_state.is_dirty = True
        if DEBUG:
            print("Physical contact detected!")
    
    def run(self):
        """Main application loop"""
        print("Starting virtual pet application...")
        
        try:
            while self.running:
                # Check if error display timeout has elapsed
                if self.error_start_time is not None:
                    elapsed_ms = (time.time() - self.error_start_time) * 1000
                    if elapsed_ms >= self.error_duration_ms:
                        # Revert from error state
                        self.pet_state.is_error = False
                        self.pet_state.current_state = self.pet_state.previous_state
                        self.pet_state.is_dirty = True
                        self.error_start_time = None
                        if DEBUG:
                            print("Error cleared, reverting to previous state")
                
                # Check button input
                self.button.check()
                
                # Check for contact reset button (GPIO pulled high, pressed = low)
                contact_pressed = self.contact_button_pin.value() == 0
                if contact_pressed and not self.contact_button_pressed:
                    self.on_physical_contact()
                self.contact_button_pressed = contact_pressed
                
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
        app = VirtualPetApp(device_id=1)
        app.run()


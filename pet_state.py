# Virtual Pet State Machine

from config import PET_STATES
import time

class PetState:
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.current_state = 0  # Start with "happy"
        self.last_update = time.time()
        self.animation_frame = 0
        self.is_dirty = True  # Flag for display refresh
        
    def set_state(self, state_id):
        """Change pet state"""
        if state_id in PET_STATES:
            if self.current_state != state_id:
                self.current_state = state_id
                self.animation_frame = 0
                self.is_dirty = True
            return True
        return False
    
    def update_state_from_health(self, contact_health):
        """Update pet state based on contact health percentage"""
        if contact_health >= 80:
            new_state = 0  # happy
        elif contact_health >= 60:
            new_state = 1  # hungry
        elif contact_health >= 40:
            new_state = 2  # sad
        elif contact_health >= 20:
            new_state = 3  # sleeping
        else:
            new_state = 4  # playful (desperate state)
        
        self.set_state(new_state)
    
    def get_state_name(self):
        """Get current state name"""
        return PET_STATES.get(self.current_state, "unknown")
    
    def update_animation(self):
        """Update animation frame"""
        self.animation_frame = (self.animation_frame + 1) % 4  # 4 frames per state
        self.is_dirty = True
    
    def get_sync_packet(self):
        """
        Generate minimal LoRA sync packet
        Format: [device_id(1 byte), state_id(1 byte)]
        Total: 2 bytes for maximum range
        """
        return bytes([self.device_id & 0xFF, self.current_state & 0xFF])
    
    def parse_sync_packet(self, packet):
        """Parse incoming sync packet"""
        if len(packet) >= 2:
            device_id = packet[0]
            state_id = packet[1]
            if state_id in PET_STATES:
                self.current_state = state_id
                self.animation_frame = 0
                self.is_dirty = True
                return True
        return False
    
    def reset_dirty_flag(self):
        """Clear the dirty flag after display update"""
        self.is_dirty = False

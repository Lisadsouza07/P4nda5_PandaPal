# Graphics Rendering Engine

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, ANIMATION_FRAME_MS
from sprites.sprite_manager import SpriteManager
from sprites.sprite_data import SPRITE_DATA
import time

class GraphicsEngine:
    def __init__(self, display):
        """
        Initialize graphics engine
        
        Args:
            display: SSD1306 display object
        """
        self.display = display
        self.sprite_manager = SpriteManager()
        self.last_frame_time = time.time()
        self.should_update_frame = False
    
    def update(self, pet_state, health_system=None):
        """
        Update and render the display
        
        Args:
            pet_state: PetState object
            health_system: HealthSystem object (optional)
        """
        current_time = time.time()
        elapsed_ms = (current_time - self.last_frame_time) * 1000
        
        # Update health system if provided
        if health_system:
            health_system.update()
            # Update pet state based on health
            pet_state.update_state_from_health(health_system.get_contact_health_percent())
        
        # Check if it's time to update animation frame
        if elapsed_ms >= ANIMATION_FRAME_MS:
            pet_state.update_animation()
            self.last_frame_time = current_time
        
        # Only redraw if state changed or animation frame changed
        if pet_state.is_dirty or elapsed_ms >= ANIMATION_FRAME_MS:
            self.draw_frame(pet_state, health_system)
    
    def draw_frame(self, pet_state, health_system=None):
        """Draw current pet state with health bars"""
        self.display.fill(0)  # Clear display
        
        if pet_state.is_error:
            # Draw error sprite (X symbol)
            self._draw_error_sprite()
        else:
            state_name = pet_state.get_state_name()
            frame_idx = pet_state.animation_frame
            
            # Get sprite for current state and frame
            sprite_bitmap = self.sprite_manager.get_sprite(state_name, frame_idx)
            
            if sprite_bitmap:
                # Draw sprite centered on display
                sprite_width = sprite_bitmap.get('width', 32)
                sprite_height = sprite_bitmap.get('height', 32)
                x = (DISPLAY_WIDTH - sprite_width) // 2
                y = (DISPLAY_HEIGHT - sprite_height) // 2
                
                self._draw_bitmap(sprite_bitmap, x, y)
            
            # Draw health indicators on sides if health_system provided
            if health_system:
                self._draw_health_indicators(health_system)
        
        # Draw status text at bottom
        state_name = pet_state.get_state_name()
        self.display.text(state_name.upper(), 0, 56, 1)
        
        self.display.show()
        pet_state.reset_dirty_flag()
    
    def _draw_health_indicators(self, health_system):
        """
        Draw health indicators:
        Left: 0-3 signal sprites (wireless health)
        Right: Contact health bar
        """
        sprite_size = 8
        spacing = 2
        
        # Left side - Signal sprites (max 3)
        signal_sprites = health_system.get_wireless_signal_sprites()
        start_x = 2
        start_y = 10
        
        for i in range(3):  # Draw up to 3 sprite slots
            # Draw outline for all 3 positions
            for px in range(sprite_size):
                self.display.pixel(start_x + px, start_y + i * (sprite_size + spacing), 1)
                self.display.pixel(start_x + px, start_y + i * (sprite_size + spacing) + sprite_size - 1, 1)
            for py in range(sprite_size):
                self.display.pixel(start_x, start_y + i * (sprite_size + spacing) + py, 1)
                self.display.pixel(start_x + sprite_size - 1, start_y + i * (sprite_size + spacing) + py, 1)
            
            # Draw filled signal sprites for active ones
            if i < signal_sprites:
                self._draw_heart_icon(start_x + 1, start_y + i * (sprite_size + spacing) + 1)
        
        # Right side - Contact health bar
        bar_width = 4
        bar_height = 32
        bar_x = DISPLAY_WIDTH - bar_width - 2
        bar_y = (DISPLAY_HEIGHT - bar_height) // 2
        
        # Draw contact icon above bar
        self._draw_contact_icon(bar_x - 2, bar_y - 8)
        
        # Draw health bar outline
        for px in range(bar_width):
            self.display.pixel(bar_x + px, bar_y, 1)
            self.display.pixel(bar_x + px, bar_y + bar_height - 1, 1)
        for py in range(bar_height):
            self.display.pixel(bar_x, bar_y + py, 1)
            self.display.pixel(bar_x + bar_width - 1, bar_y + py, 1)
        
        # Draw filled portion based on contact health
        contact_pixels = health_system.get_contact_health_pixels(bar_height)
        if contact_pixels > 0:
            for px in range(bar_width):
                for py in range(contact_pixels):
                    self.display.pixel(bar_x + px, bar_y + (bar_height - py - 1), 1)
    
    def _draw_heart_icon(self, x, y):
        """Draw wireless/signal indicator icon (8x8) from sprite data"""
        if "heart_icon" in SPRITE_DATA and SPRITE_DATA["filled_heart_icon"]:
            icon_bitmap = SPRITE_DATA["filled_heart_icon"][0]
            self._draw_bitmap(icon_bitmap, x, y)
    
    def _draw_contact_icon(self, x, y):
        """Draw contact/touch indicator icon (8x8) from sprite data"""
        if "contact_icon" in SPRITE_DATA and SPRITE_DATA["contact_icon"]:
            icon_bitmap = SPRITE_DATA["contact_icon"][0]
            self._draw_bitmap(icon_bitmap, x, y)
    
    def _draw_bitmap(self, bitmap_data, x, y):
        """
        Draw bitmap to display
        
        Args:
            bitmap_data: Dictionary with 'width', 'height', and 'data' keys
            x, y: Position on display
        """
        width = bitmap_data.get('width', 0)
        height = bitmap_data.get('height', 0)
        data = bitmap_data.get('data', [])
        
        if not data:
            return
        
        # Draw pixel by pixel (bitmap format: list of bytes, 8 pixels per byte)
        for byte_idx, byte_val in enumerate(data):
            row = byte_idx // ((width + 7) // 8)
            col = (byte_idx % ((width + 7) // 8)) * 8
            
            for bit in range(8):
                if col + bit < width and row < height:
                    if byte_val & (1 << bit):
                        px = x + col + bit
                        py = y + row
                        if 0 <= px < DISPLAY_WIDTH and 0 <= py < DISPLAY_HEIGHT:
                            self.display.pixel(px, py, 1)
    
    def _draw_error_sprite(self):
        """Draw error sprite (X symbol) in center of display"""
        center_x = DISPLAY_WIDTH // 2
        center_y = (DISPLAY_HEIGHT - 16) // 2  # Offset for text at bottom
        size = 16
        
        # Draw X (two diagonal lines)
        for i in range(size):
            # Draw from top-left to bottom-right
            x1 = center_x - size // 2 + i
            y1 = center_y - size // 2 + i
            if 0 <= x1 < DISPLAY_WIDTH and 0 <= y1 < DISPLAY_HEIGHT:
                self.display.pixel(x1, y1, 1)
            
            # Draw from top-right to bottom-left
            x2 = center_x + size // 2 - i
            y2 = center_y - size // 2 + i
            if 0 <= x2 < DISPLAY_WIDTH and 0 <= y2 < DISPLAY_HEIGHT:
                self.display.pixel(x2, y2, 1)

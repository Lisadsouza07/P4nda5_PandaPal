# LoRA Communication Module

from config import (
    LORA_MOSI_PIN, LORA_MISO_PIN, LORA_CLK_PIN, LORA_SS_PIN,
    LORA_RESET_PIN, LORA_DIO0_PIN, LORA_FREQUENCY,
    LORA_BANDWIDTH, LORA_SPREADING_FACTOR, LORA_CODING_RATE, LORA_POWER
)
from machine import SPI, Pin
from sx127x import SX127x
import time

class LoRaCommunication:
    def __init__(self):
        """Initialize LoRA module using sx127x driver"""
        try:
            # Hardware reset sequence
            reset_pin = Pin(LORA_RESET_PIN, Pin.OUT)
            reset_pin.value(0)
            time.sleep(0.01)
            reset_pin.value(1)
            time.sleep(0.1)
            
            # SPI configuration
            self.spi = SPI(
                1,
                baudrate=1000000,
                polarity=0,
                phase=0,
                bits=8,
                sck=Pin(LORA_CLK_PIN),
                mosi=Pin(LORA_MOSI_PIN),
                miso=Pin(LORA_MISO_PIN)
            )
            
            # Pin mapping for sx127x (must use 'ss' and 'dio_0' as expected by driver)
            pins = {
                'ss': LORA_SS_PIN,
                'reset': LORA_RESET_PIN,
                'dio_0': LORA_DIO0_PIN
            }
            
            # LoRA parameters
            parameters = {
                'frequency': LORA_FREQUENCY,
                'tx_power_level': LORA_POWER,
                'signal_bandwidth': LORA_BANDWIDTH,
                'spreading_factor': LORA_SPREADING_FACTOR,
                'coding_rate': LORA_CODING_RATE,
                'preamble_length': 8,
                'implicit_header': False,
                'sync_word': 0x12,
                'enable_CRC': False,
                'invert_IQ': False,
            }
            
            # Initialize LoRA
            self.lora = SX127x(self.spi, pins, parameters)
            self.lora.receive()  # Start in receive mode
            self.initialized = True
            print("LoRA initialized successfully")
        
        except Exception as e:
            print(f"LoRA initialization error: {e}")
            self.initialized = False
    
    def send(self, data):
        """
        Send data via LoRA
        
        Args:
            data: Bytes to send
        
        Returns:
            True if successful, False otherwise
        """
        if not self.initialized:
            return False
        
        try:
            self.lora.println(data, implicit_header=False)
            self.lora.receive()  # Return to receive mode after sending
            return True
        except Exception as e:
            print(f"LoRA send error: {e}")
            return False
    
    def receive(self):
        """
        Check for incoming LoRA data
        
        Returns:
            Received bytes or None if no data
        """
        if not self.initialized:
            return None
        
        try:
            if self.lora.received_packet():
                payload = self.lora.read_payload()
                # Resume receiving after reading payload
                self.lora.receive()
                return payload
        except Exception as e:
            print(f"LoRA receive error: {e}")
        
        return None

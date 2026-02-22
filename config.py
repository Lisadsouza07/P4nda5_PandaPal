# ESP32-S3 Pin Configuration and Settings

# I2C Display Configuration
I2C_SDA_PIN = 4
I2C_SCL_PIN = 5
I2C_FREQ = 400000

# LoRA Module Configuration (SX1278)
LORA_MOSI_PIN = 10
LORA_MISO_PIN = 8
LORA_CLK_PIN = 9
LORA_SS_PIN = 3  # Slave Select (Chip Select)
LORA_RESET_PIN = 2
LORA_DIO0_PIN = 11  # Interrupt pin
LORA_FREQUENCY = 915000000  # 915 MHz for US, adjust for your region
LORA_BANDWIDTH = 31250
LORA_SPREADING_FACTOR = 10
LORA_CODING_RATE = 8
LORA_POWER = 20

# Button Configuration
BUTTON_PIN = 12
BUTTON_DEBOUNCE_MS = 50

# OneWire Contact Detection (physical touch)
ONEWIRE_PIN = 0

# Display Configuration
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
DISPLAY_I2C_ADDR = 0x3C

# Pet State Definitions
PET_STATES = {
    0: "happy",
    1: "angry",
    2: "sad",
    3: "sleeping",
}

# Animation frame rate (ms per frame)
ANIMATION_FRAME_MS = 50

# LoRA sync interval (ms)
LORA_SYNC_MS = 1000

# Debug mode
DEBUG = True

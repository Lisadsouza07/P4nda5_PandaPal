# ESP32-C3 Pin Configuration and Settings

# I2C Display Configuration
I2C_SDA_PIN = 9
I2C_SCL_PIN = 8
I2C_FREQ = 400000

# LoRA Module Configuration (SX1278)
LORA_MOSI_PIN = 7
LORA_MISO_PIN = 2
LORA_CLK_PIN = 6
LORA_SS_PIN = 10  # Slave Select (Chip Select)
LORA_RESET_PIN = 4
LORA_DIO0_PIN = 5  # Interrupt pin
LORA_FREQUENCY = 915000000  # 915 MHz for US, adjust for your region
LORA_BANDWIDTH = 125000
LORA_SPREADING_FACTOR = 7
LORA_CODING_RATE = 5
LORA_POWER = 17

# Button Configuration
BUTTON_PIN = 0
BUTTON_DEBOUNCE_MS = 50

# Display Configuration
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
DISPLAY_I2C_ADDR = 0x3C

# Pet State Definitions
PET_STATES = {
    0: "happy",
    1: "hungry",
    2: "sad",
    3: "sleeping",
    4: "playful"
}

# Animation frame rate (ms per frame)
ANIMATION_FRAME_MS = 200

# LoRA sync interval (ms)
LORA_SYNC_MS = 1000

# Debug mode
DEBUG = True

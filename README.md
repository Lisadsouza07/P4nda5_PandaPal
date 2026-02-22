# PandaPal - ESP32-C3 Virtual Pet Pair

A dual ESP32-C3 based virtual pet system using LoRA for wireless synchronization.

## Hardware Requirements
- 2x ESP32-C3 microcontroller boards
- 2x SSD1306 I2C OLED displays (128x64)
- 2x SX1278 LoRA modules
- 2x Push buttons (GPIO input)
- Power supply (USB or battery)

## Features
- Sprite-based virtual pet display with state machine
- Real-time state synchronization via LoRA
- Minimal data packet size for maximum range
- Easy sprite creation and animation system
- MicroPython implementation

## Project Structure
```
P4nda5/
├── main.py                 # Entry point
├── config.py              # Configuration and pin definitions
├── pet_state.py           # State machine and state management
├── graphics.py            # Graphics rendering engine
├── lora_comm.py           # LoRA communication
├── sprites/               # Sprite definitions and utilities
│   ├── sprite_manager.py  # Sprite loading and animation
│   ├── sprite_data.py     # Sprite bitmap data
│   └── sprites.png        # Source pixel art sprites
├── utils/
│   ├── i2c_display.py     # I2C OLED driver wrapper
│   └── button_handler.py  # Button input handling
└── tools/
    └── png_to_bitmap.py   # Python utility to convert PNG sprites to bitmaps
```

## Installation
1. Flash MicroPython to both ESP32-C3 boards
2. Upload all `.py` files to both boards
3. Customize sprites using the PNG to bitmap converter
4. Power up and pair the devices via LoRA

## Configuration
Edit `config.py` to adjust:
- I2C pins and display address
- LoRA module pins and frequency
- Button GPIO pins
- Pet state definitions

## Key Features Implemented
- ✅ **2-byte LoRA packets** for maximum range (state sync only)
- ✅ **4-frame animation system** per state
- ✅ **State machine** with 5 base states (easily extensible)
- ✅ **Button-driven state changes**
- ✅ **Automatic sync** between paired devices
- ✅ **SSD1306 display support**
- ✅ **Efficient bitmap rendering**
- ✅ **Sprite management system**

The system prioritizes **range over data density** — just 2 bytes per sync packet!

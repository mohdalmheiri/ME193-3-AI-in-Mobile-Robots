# LEGO Single Motor Control

A Python project for controlling a LEGO Education Single Motor using the `legoeducation` library.

## Overview

This project demonstrates how to control a LEGO Education Single Motor programmatically. It includes examples of:
- Connecting to a motor device
- Running the motor for a specified number of degrees
- Running the motor for a specified duration
- Monitoring motor position in real-time
- Proper connection management and cleanup

## Requirements

- Python 3.8 or higher
- macOS (currently configured for Mac)
- LEGO Education Single Motor (powered on and broadcasting)

## Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ME193
```

### 2. Create a Virtual Environment
```bash
python3 -m venv my_env
source my_env/bin/activate  # On Mac/Linux
# or
my_env\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install legoeducation
```

## Usage

### Basic Connection and Motor Control
```bash
python test.py
```

This will:
1. Connect to your LEGO Single Motor
2. Run the motor for 180 degrees
3. Run the motor for 2 seconds at 50% speed
4. Monitor the motor position for a few seconds
5. Stop the motor and disconnect

### Customizing Motor Commands

Edit `test.py` to customize:
- **Speed**: Change the `speed` parameter (0-100%)
- **Duration**: Modify the `time_ms` parameter (in milliseconds)
- **Degrees**: Adjust the `degrees` parameter for rotation angle
- **Direction**: Use `le.MOTOR_MOVE_DIRECTION_CLOCKWISE` or `le.MOTOR_MOVE_DIRECTION_COUNTERCLOCKWISE`

### Connection Card Configuration

If you have multiple LEGO devices, update the connection parameters in `test.py`:
```python
singlemotor.connect(card_color=le.LEGO_COLOR_AZURE, card_serial="3683")
```

Replace the color and serial number to match your Connection Card.

## Project Structure

```
ME193/
├── test.py           # Main motor control script
├── my_env/           # Virtual environment (not pushed to GitHub)
├── .gitignore        # Git ignore file
└── README.md         # This file
```

## Features

### Motor Commands Available

- `motor_run()` - Run motor continuously
- `motor_run_for_degrees(degrees)` - Rotate motor by specified degrees
- `motor_run_for_time(time_ms)` - Run motor for specified duration
- `motor_stop()` - Stop the motor
- `motor_set_speed(speed)` - Set motor speed
- `motor_reset_relative_position()` - Reset position counter

### Motor Monitoring

Access motor data:
- `singlemotor.motor.position` - Current position in degrees
- `singlemotor.motor.motorState` - Current motor state
- `singlemotor.motor.speed` - Current speed

## Troubleshooting

### Connection Failed
- Ensure the LEGO Single Motor is powered on
- Check that the motor is broadcasting in Bluetooth
- Verify you're using the correct Connection Card color and serial number

### Module Not Found Error
- Make sure the virtual environment is activated
- Run `pip install legoeducation` again

### Permission Denied
- On macOS, you may need to grant Bluetooth permissions to your terminal

## Reference

For more information about the LEGO Education Python API:
- [GitHub Repository](https://github.com/LEGO/LEGOEducation)
- [Official Documentation](https://github.com/LEGO/LEGOEducation/blob/main/README.md)

## License

This project uses the LEGO Education Python API. Please refer to the LEGO Education repository for license information.

## Author

Created for LEGO Education motor control examples.

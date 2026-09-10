import legoeducation as le
import time

# Create a Single Motor instance
singlemotor = le.SingleMotor()

# Connect to the motor
# You can specify card_color and card_serial to connect to a specific device
# or leave empty to connect to the first available device
singlemotor.connect()

# Check if connection was successful
if not singlemotor.connected:
    print('Error connecting to Single Motor.')
    exit(1)

# Example 1: Run motor for 180 degrees
print('Running motor for 180 degrees...')
singlemotor.motor_run_for_degrees(180)

# Example 2: Run motor for 2 seconds at 50% speed
print('Running motor for 2 seconds at 50% speed...')
singlemotor.motor_run_for_time(2000, speed=50)

# Example 3: Run motor continuously for a bit, then check position
print('Running motor continuously and monitoring position...')
singlemotor.motor_reset_relative_position()
singlemotor.motor_run(speed=30)

for i in range(20):
    print(f'Motor position: {singlemotor.motor.position}')
    time.sleep(0.1)

# Stop the motor
singlemotor.motor_stop()

# Disconnect
singlemotor.disconnect()
print('Done!')
exit(0)
import time

# DEMO VERSION - Simulates a LEGO Single Motor without requiring actual hardware

class SimulatedMotor:
    """Simulates a LEGO Single Motor for testing purposes"""
    def __init__(self):
        self.position = 0
        self.speed = 0
        self.is_running = False
        
    def motor_run_for_degrees(self, degrees, speed=50):
        print(f'📍 Running motor for {degrees} degrees at {speed}% speed...')
        self.position += degrees
        time.sleep(1)  # Simulate motor running time
        print(f'✓ Motor completed: position now at {self.position}°')
        
    def motor_run_for_time(self, time_ms, speed=50):
        print(f'⏱️  Running motor for {time_ms}ms ({time_ms/1000}s) at {speed}% speed...')
        self.speed = speed
        self.is_running = True
        time.sleep(time_ms / 1000)
        self.is_running = False
        self.position += int((time_ms / 1000) * speed)
        print(f'✓ Motor completed: position now at {self.position}°')
        
    def motor_reset_relative_position(self):
        print('🔄 Resetting motor position to 0°')
        self.position = 0
        
    def motor_run(self, speed=50):
        print(f'🔄 Motor running continuously at {speed}% speed...')
        self.speed = speed
        self.is_running = True
        
    def motor_stop(self):
        print('⏹️  Motor stopped')
        self.is_running = False


# Create a simulated motor
singlemotor = SimulatedMotor()

print("=" * 50)
print("LEGO SINGLE MOTOR - DEMO VERSION (No Hardware)")
print("=" * 50)
print()

# Example 1: Run motor for 180 degrees
print('Example 1: Run motor for 180 degrees')
singlemotor.motor_run_for_degrees(180)
print()

# Example 2: Run motor for 2 seconds at 50% speed
print('Example 2: Run motor for 2 seconds at 50% speed')
singlemotor.motor_run_for_time(2000, speed=50)
print()

# Example 3: Run motor continuously and monitor position
print('Example 3: Run motor continuously and monitor position')
singlemotor.motor_reset_relative_position()
singlemotor.motor_run(speed=30)

print('📊 Monitoring motor position for 2 seconds:')
for i in range(20):
    print(f'  Sample {i+1}: Motor position = {singlemotor.position}°, Speed = {singlemotor.speed}%')
    time.sleep(0.1)

singlemotor.motor_stop()
print()

print("=" * 50)
print("✅ Demo completed successfully!")
print("=" * 50)
print()
print("To use with real LEGO hardware:")
print("1. Power on your LEGO Single Motor")
print("2. Enable Bluetooth broadcasting")
print("3. Remove the SimulatedMotor class and uncomment the legoeducation code")
print()
exit(0)
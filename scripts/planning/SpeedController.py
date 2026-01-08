import numpy as np

class SpeedController:
    def __init__(self, target_speed, kp=1.0, ki=0.3, kd=0.05, dt=0.5, 
                    integral_limit=100.0, acc_to_throttle=10.0,
                    throttle_deadzone=0.02, brake_deadzone=0.02):
        
        self.target_speed = target_speed
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0.0
        self.prev_error = 0.0
        self.dt = dt
        self.integral_limit = integral_limit
        self.acc_to_throttle = acc_to_throttle
        self.throttle_deadzone = throttle_deadzone
        self.brake_deadzone = brake_deadzone

    def run(self, speed):
        """
        PID speed controller (speed in m/s).
        - target_speed, speed: m/s
        - dt: seconds between calls
        - integral_limit: saturation for anti-windup
        - acc_to_throttle: factor to convert 'acc' to throttle
        """

        # Error
        error = self.target_speed - speed

        # Integral with anti-windup
        self.integral += error * self.dt
        self.integral = np.clip(self.integral, -self.integral_limit, self.integral_limit)

        # Derivative
        derivative = (error - self.prev_error) / (self.dt + 1e-6)

        # PID signal (desired acceleration, *not* in exact m/s², is a signal)
        acc = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Convert to throttle/brake
        # Simple adjustment: throttle = acc / acc_to_throttle, brake if acc < 0
        throttle = np.clip(acc / self.acc_to_throttle, 0.0, 1.0)
        brake = 0.0
        if acc < 0:
            brake = np.clip(abs(acc) / self.acc_to_throttle, 0.0, 1.0)
            throttle = 0.0

        # deadzone: avoids short pulses
        if throttle < self.throttle_deadzone:
            throttle = 0.0
        if brake < self.brake_deadzone:
            brake = 0.0

        return throttle, brake, self.integral, error



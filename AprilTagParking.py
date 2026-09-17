"""AprilTag parking.

Detect an AprilTag (36h11, see for17sep.py) taped to a tower on the car in
the live webcam feed, and drive the car so the tag centers itself
horizontally in the frame.

The car drives back and forth in a straight line parallel to the screen, so
control only needs one axis: the horizontal (x) pixel offset between the
tag's centroid and the frame's horizontal center. A proportional (P)
controller maps that offset directly to motor speed - big offset -> fast,
small offset -> slow - and both wheels get the same speed/direction since
the car is just going straight forward/backward, not turning.

NOTE ON SIGN: whether positive error should drive the car left or right
depends on which way your camera/car are facing, which can't be known ahead
of time. If the car drives away from center instead of toward it, flip the
sign of KP (or SPRING_K).
"""

import time

import cv2
import legoeducation as le
import numpy as np

# --- Configuration ---------------------------------------------------------

# Update these to match the Connection Card plugged into the car's Double Motor
CARD_COLOR = le.LEGO_COLOR_RED
CARD_SERIAL = "0999"

CAMERA_INDEX = 0
TAG_FAMILY = cv2.aruco.DICT_APRILTAG_36h11

# Proportional controller: motor_speed = KP * pixel_error, clamped to +-MAX_SPEED.
# Negative: on this car, a positive movement_move() speed drives toward positive
# pixel error instead of away from it, so KP has to be negative to correct it.
KP = -0.25
MAX_SPEED = 60
DEADBAND_PX = 15  # stop once the tag centroid is within this many px of center
SEND_THRESHOLD = 3  # only send a new BLE command if speed changed by more than this (%)

# "Spring loaded" bonus mode: simulate a mass-spring-damper instead of a plain
# P controller with a deadband, so the car overshoots the center and settles
# back onto it instead of just stopping dead the first time it crosses center.
SPRING_LOADED = False
SPRING_K = -0.35  # spring stiffness - how hard the "spring" pulls speed toward the center (sign matches KP)
SPRING_DAMPING = 0.90  # velocity decay per frame - lower = more overshoot/oscillation


def try_connect(device, card_color, card_serial, label):
    """Connect a LEGO device, treating any connection-time error the same as
    a failed scan instead of crashing the whole program."""
    try:
        device.connect(card_color=card_color, card_serial=card_serial)
    except Exception as exc:
        print(f"Could not connect to the {label}: {exc}")
        return False
    if not device.connected:
        print(f"Could not connect to the {label} - not found.")
        return False
    return True


def find_tag_centroid(frame, detector):
    corners, ids, _ = detector.detectMarkers(frame)
    if ids is None or len(corners) == 0:
        return None, None
    tag_corners = corners[0][0]  # first detected tag, 4x2 array of (x, y) corners
    centroid = tag_corners.mean(axis=0)
    return centroid, tag_corners


def p_controller(error_px):
    """Plain proportional control with a deadband so the motors fully stop
    once the tag is centered, instead of jittering around zero error."""
    if abs(error_px) < DEADBAND_PX:
        return 0.0
    return float(np.clip(KP * error_px, -MAX_SPEED, MAX_SPEED))


def spring_controller(error_px, velocity):
    """Mass-spring-damper: treat the car like a mass on a spring anchored at
    the frame center. The spring force pulls it toward center; with light
    damping it overshoots past center before the spring pulls it back, then
    settles - instead of stopping dead the instant it crosses center."""
    force = SPRING_K * error_px
    velocity = float(np.clip(SPRING_DAMPING * velocity + force, -MAX_SPEED, MAX_SPEED))
    return velocity, velocity


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    dictionary = cv2.aruco.getPredefinedDictionary(TAG_FAMILY)
    detector = cv2.aruco.ArucoDetector(dictionary)

    car = le.DoubleMotor()
    connected = try_connect(car, CARD_COLOR, CARD_SERIAL, "car")
    if not connected:
        print("Running in camera preview-only mode.")

    last_speed = 0.0
    velocity = 0.0  # only used by the spring controller

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            h, w = frame.shape[:2]
            frame_center_x = w / 2
            centroid, tag_corners = find_tag_centroid(frame, detector)

            if centroid is None:
                # No tag detected: stop rather than guess at a direction.
                speed = 0.0
                velocity = 0.0
                cv2.putText(
                    frame, "No tag detected - stopped", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                )
            else:
                error_px = centroid[0] - frame_center_x
                if SPRING_LOADED:
                    speed, velocity = spring_controller(error_px, velocity)
                else:
                    speed = p_controller(error_px)

                cv2.polylines(frame, [tag_corners.astype(int)], True, (0, 0, 255), 3)
                cx, cy = int(centroid[0]), int(centroid[1])
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.putText(
                    frame, f"centroid=({cx},{cy})  speed={speed:.0f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                )

            cv2.line(frame, (int(frame_center_x), 0), (int(frame_center_x), h), (0, 255, 0), 1)

            if connected and abs(speed - last_speed) > SEND_THRESHOLD:
                # movement_move() drives both wheels straight forward/backward from a
                # single signed speed. Driving MOTOR_LEFT/MOTOR_RIGHT individually with
                # the same raw speed instead turns the car on this unit - the two motors
                # are mounted with opposite sign conventions, so movement_move() (which
                # already accounts for that) is what actually goes straight.
                # blocking=False: fire-and-forget, so the camera loop never waits on BLE
                car.movement_move(speed=speed, blocking=False)
                last_speed = speed

            cv2.imshow("AprilTag Parking (press q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        if connected:
            try:
                car.motor_stop(motor=le.MOTOR_BOTH)
                car.disconnect()
            except Exception as exc:
                print(f"Error while stopping/disconnecting the car: {exc}")
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

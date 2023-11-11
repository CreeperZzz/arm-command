import cv2
import mediapipe as mp
import math
import asyncio
from kasa import SmartPlug
import pyrealsense2 as rs
import numpy as np

async def turn_on(plug: SmartPlug):
    await plug.turn_on()

async def turn_off(plug: SmartPlug):
    await plug.turn_off()

def main():

    plug = SmartPlug('192.168.1.202')
    asyncio.run(plug.update())
    lightIsOn = plug.is_on


    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=1
    )

    mp_drawing = mp.solutions.drawing_utils

    pipeline = rs.pipeline()

    # Create a config and configure the pipeline to stream
    # different resolutions of color and depth streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Convert images to numpy arrays
        rgb_frame = np.asanyarray(color_frame.get_data())

        # Process the frame
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                if(results.multi_handedness[idx].classification[0].label == 'Left'):
                    finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        
                    print(f'finger_base: x:{finger_base.x:.4f}, y:{finger_base.y:.4f}, z:{finger_base.z:.4f}')
                    print(f'finger_tip: x:{finger_tip.x:.4f}, y:{finger_tip.y:.4f}, z:{finger_tip.z:.4f}')
                    up = finger_tip.y < finger_base.y
                    print('up' if up else 'down')
                    if up:
                        if not lightIsOn:
                            try:
                                asyncio.run(turn_on(plug))
                                lightIsOn = True
                                print('on')
                            except Exception as e:
                                print(e)
                    else:
                        if lightIsOn:
                            try:
                                asyncio.run(turn_off(plug))
                                lightIsOn = False
                                print('off')
                            except Exception as e:
                                print(e)

                # mp_drawing.draw_landmarks(
                #     image=rgb_frame,
                #     landmark_list=hand_landmarks,
                #     connections=mp_hands.HAND_CONNECTIONS,
                #     landmark_drawing_spec=mp_drawing.DrawingSpec(thickness=2, circle_radius=2),
                #     connection_drawing_spec=mp_drawing.DrawingSpec(thickness=1, circle_radius=2)
                # )

        # Display the frame
        # cv2.imshow('hands', cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    # cap.release()
    pipeline.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

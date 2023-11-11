import cv2
import mediapipe as mp
import math
import asyncio
from kasa import SmartPlug
from picamera2 import Picamera2

async def turn_on(plug: SmartPlug):
    # await plug.update()
    # if plug.is_off:
        await plug.turn_on()

async def turn_off(plug: SmartPlug):
    # await plug.update()
    # if plug.is_on:
        await plug.turn_off()



def main():
    
    plug = SmartPlug('192.168.1.202')
    asyncio.run(plug.update())
    on = plug.is_on
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        min_detection_confidence = 0.8,
        min_tracking_confidence = 0.3,
        max_num_hands = 2
    )

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
    picam2.start() 
    
    # print(picam2.camera_properties)
    
    while True:
        frame = picam2.capture_array()
        
        # frame = cv2.flip(frame, 1)
        frame = cv2.flip(frame, 0)
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                if(results.multi_handedness[idx].classification[0].label == 'Right'):
                    finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        
                    print(f'finger_base: x:{finger_base.x:.4f}, y:{finger_base.y:.4f}, z:{finger_base.z:.4f}')
                    print(f'finger_tip: x:{finger_tip.x:.4f}, y:{finger_tip.y:.4f}, z:{finger_tip.z:.4f}')
                    up = finger_tip.y < finger_base.y
                    print('up' if up else 'down')
                    if up:
                        if not on:
                            try:
                                asyncio.run(turn_on(plug))
                                on = True
                            except Exception as e:
                                print(e)
                    else:
                        if on:
                            try:
                                asyncio.run(turn_off(plug))
                                on = False
                            except Exception as e:
                                print(e)
        # cv2.imshow('hands', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    picam2.close()

if __name__ == '__main__':
    main()

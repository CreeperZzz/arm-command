import cv2
import mediapipe as mp
import math
from picamera2 import Picamera2
def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        min_detection_confidence = 0.4,
        min_tracking_confidence = 0.3,
        max_num_hands = 1
    )

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
    picam2.start() 
    
    print(picam2.camera_properties)
    
    while True:
        frame = picam2.capture_array()
        
        frame = cv2.flip(frame, 1)
        frame = cv2.flip(frame, 0)
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    image= rgb_frame,
                    landmark_list= hand_landmarks,
                    connections=mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec= mp_drawing.DrawingSpec(thickness=2, circle_radius=2),
                    connection_drawing_spec= mp_drawing.DrawingSpec(thickness=1, circle_radius=2)
                )
                
                finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                
                print(f'finger_base: x:{finger_base.x:.4f}, y:{finger_base.y:.4f}, z:{finger_base.z:.4f}')
                print(f'finger_tip: x:{finger_tip.x:.4f}, y:{finger_tip.y:.4f}, z:{finger_tip.z:.4f}')
                
        # rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        cv2.imshow('hands', rgb_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    picam2.close()

if __name__ == '__main__':
    main()

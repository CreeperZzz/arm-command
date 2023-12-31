import cv2
import mediapipe as mp
import math
import asyncio
from kasa import SmartPlug
import pyrealsense2 as rs
import numpy as np
import torch
import myutils

async def turn_on(plug: SmartPlug):
    await plug.turn_on()

async def turn_off(plug: SmartPlug):
    await plug.turn_off()

def main():
    prevUp = False
    light = SmartPlug('192.168.1.201')
    monitor = SmartPlug('192.168.1.182')
    devices = {0: light, 1: monitor}


    model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/masters/repo/arm-command/src/model/best.pt')
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        min_detection_confidence=0.3,
        min_tracking_confidence=0.3,
        max_num_hands=2
    )

    mp_drawing = mp.solutions.drawing_utils

    pipeline = rs.pipeline()

    # Create a config and configure the pipeline to stream
    # different resolutions of color and depth streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)



    # Start streaming
    pipeline.start(config)
    sensor = pipeline.get_active_profile().get_device().first_color_sensor()
    sensor.set_option(rs.option.exposure, 500)
    align = rs.align(rs.stream.color)
    objects = None
    image_result = None
    try:
        while True:
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
            color_frame = aligned_frames.get_color_frame()

            if not aligned_depth_frame or not color_frame:
                continue        

            # Convert images to numpy arrays
            rgb_frame = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(aligned_depth_frame.get_data())

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            while objects is None:
            
                #procee the object detection
                object_results = model(rgb_frame)
                # frame = object_results.render()[0]
                detections = object_results.xyxy[0]
                good_result = True
                # for detection in detections.numpy():
                #     xmin, ymin, xmax, ymax, confidence, class_id = detection
                #     if confidence < 0.5:
                #         good_result = False
                #         print(class_id)
                #         break

                # if good_result:
                objects = []
                image_result = object_results
                for detection in detections.numpy():
                    xmin, ymin, xmax, ymax, confidence, class_id = detection
                    object_min_corner = (xmin, ymin, aligned_depth_frame.get_distance(int(xmin+(xmax-xmin)/2), int(ymin+(ymax-ymin)/2))-0.1)
                    object_max_corner = (xmax, ymax, aligned_depth_frame.get_distance(int(xmin+(xmax-xmin)/2), int(ymin+(ymax-ymin)/2))+0.1)
                    
                    objects.append((class_id, object_min_corner, object_max_corner))

            frame = image_result.render()[0]

            # Process the hand detection
            results = hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    if(results.multi_handedness[idx].classification[0].label == 'Right'):
                        finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                        finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        
                        if finger_tip.y < 0  or finger_base.y < 0 or finger_tip.y >=1   or finger_base.y >=1:
                            continue

                        if finger_tip.x < 0  or finger_base.x < 0 or finger_tip.x >=1   or finger_base.x >=1:
                            continue 
                        
                        #get the finger vector
                        dx = (finger_tip.x - finger_base.x) * 640
                        dy = (finger_tip.y - finger_base.y) * 480
                        dz = aligned_depth_frame.get_distance(int(640*finger_tip.x), int(480*finger_tip.y))- aligned_depth_frame.get_distance(int(640*finger_base.x), int(480*finger_base.y))     
                        vector_start = (finger_base.x*640, finger_base.y*480, aligned_depth_frame.get_distance(int(640*finger_base.x), int(480*finger_base.y)))
                        vector_direction = (dx, dy, dz)
                        up = myutils.is_thumbs_up(hand_landmarks)

                        # detections = objects.xyxy[0]
                        for detection in objects: #loop all detected object
                            # print(detection)
                            class_id, object_min_corner, object_max_corner = detection
                            # object_min_corner = (xmin, ymin, aligned_depth_frame.get_distance(int(xmin+(xmax-xmin)/2), int(ymin+(ymax-ymin)/2))-0.1)
                            # object_max_corner = (xmax, ymax, aligned_depth_frame.get_distance(int(xmin+(xmax-xmin)/2), int(ymin+(ymax-ymin)/2))+0.3)

                            #check the intersection
                            if vector_start and vector_direction and object_min_corner and object_max_corner:
                                if myutils.check_intersection(vector_start, vector_direction, object_min_corner, object_max_corner):
                                    cv2.putText(rgb_frame, f"Pointed: {class_id}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                                    # print('up' if up else 'down')
                                    if up and not prevUp:
                                        plug = devices[class_id]
                                        asyncio.run(plug.update())
                                        lightIsOn = plug.is_on
                                        print("change")
                                        if not lightIsOn:
                                            try:
                                                asyncio.run(turn_on(plug))
                                                print('on')
                                            except Exception as e:
                                                print(e)
                                        if lightIsOn:
                                            try:
                                                asyncio.run(turn_off(plug))
                                                print('off')
                                            except Exception as e:
                                                print(e)
                                    break
                        prevUp = up
                    
                    mp_drawing.draw_landmarks(
                        image=rgb_frame,
                        landmark_list=hand_landmarks,
                        connections=mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing.DrawingSpec(thickness=2, circle_radius=2),
                        connection_drawing_spec=mp_drawing.DrawingSpec(thickness=1, circle_radius=2)
                    )
            # Display the frame
            # cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
            # cv2.imshow('hands', depth_colormap)
            cv2.imshow('handsRGB', cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
            cv2.imshow('object', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release resources
    # cap.release()
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

# Table of Contents
* Abstract
* [Introduction](#1-introduction)
* [Related Work](#2-related-work)
* [Technical Approach](#3-technical-approach)
* [Evaluation and Results](#4-evaluation-and-results)
* [Discussion and Conclusions](#5-discussion-and-conclusions)
* [References](#6-references)

# Abstract


Arm command aims to streamline and simplify the user interaction with smart devices in one's home. By leveraging a Lidar, RGB camera, and an intel NUC, we allow the user to simply point to a smart device and toggle it on/off by raising their thumb.
We utilized MediaPipe's hand detection model to identify the user's hand, and then created our own algorithm to create a vector of the index finger to then determine the object being pointed to. By training a YOLO object detector model, we are currently able to indentify a lamp and a computer monitor, allowing the user to control both by simply making a thumbs up. The object's hitbox were created based on the location in the image and then extruded to become a 3d object. We then project tyhe finger's vector trajectory and check for any collion with the hitboxes.
Our first success metric is related to response time: time elapsed from the moment the user controlled a device until when the action happened. In the current setting, we measured an average response time of less than 1 second.
Another success metric is related to detection accuracy: how close can objects be and still be accurately controllable. In our testing, as long as the objects are not overlapping, the system will work as expected.

# 1. Introduction
## Motivation and Objective

As home automation becomes more popular, users may seek a more intuitive way of interacting with smart home devices such as lights and other electronics. However, the current approach used by the majority of the main automation services require the user to name individual devices or scenes to then activate/deactivate with voice commands. As the number of devices in one’s house increases, this process can become somewhat of a burden. But what if we could control devices simply by pointing at them?

By using a small computer, a camera, and a Lidar, we are able to first detect a person’s fingers and determine which object the user is pointing to. Then, with a simple command (raising the thumb) the smart home device will toggle on/off.

### State of the Art
- Setup devices and scenes through app
- User interaction based on voice prompts using devices’/scenes names 
- Gesture controls need wearable devices.

### Limitations
- Have to remember the name of devices
- Tedious/hard setup process
- Need of a wearable device
  

### Novelty
- Integration of camera and Lidar (tof sensor) to compute direction in which the user is pointing and then interacting with smart devices.
- No need of wearable device
- No need to call the names every devices

### Potential Impact
- Instead of voice control, gesture control will be the major method to control home devices because it’s convenient and smooth.
- People with speech disabilities can also use this solution to control smart home devices if adapted to detect gestures
  

### Challenges:
- Precision of tof sensor detection, the accuracy of 3d metrics
- The model precision to detect human skeletons
- Delays due to computations

### Risks:
- As we’re dealing with a camera, this could result in privacy issues.


### Requirements for Success

- Be able to detect user hand's landmarks
- Locate smart home devices using camera
- Create depth map using Lidar
- Combine Lidar and camera work to determine position where user is pointing to
- Point laser at chosen device
- Interface with smart device to toggle on/off


### Metrics of Success

- Accuracy when determining which device user is pointing to
- Time taken to determine device


# 2. Related Work
### Papers
- [SeleCon](https://ieeexplore.ieee.org/document/7946862) : This paper presents the idea of using a ultra-wideband (UWB) equipped smartwatch to implement a pointing approach to interact with smart devices. This is similar to our approach but it relies on a wearable device and pre-configured "scenes" to determine where the user is pointing to.
- [Minuet](https://dl.acm.org/doi/10.1145/3357251.3357581) : This paper explores the HCI aspect of using of multimodal approach to interacting with smart home devices.

# 3. Technical Approach
### Hand Detections
We use the Mediapipe hand model to detect hand skeletons in realtime. And we calculate the index finger vector based on its finger base and finger tip. 
### Object Detetions
We trained a YOLO v5s model to perform the object detection of both the lamp and computer monitor. We then create a boundary cube around the objects to serve as a hitbox.
### Pointing Check
We then calculate the intercept between the finger vector and the objects’ hitbox to determine which object is being pointed to.
### Device Control
By using the fingers landmarks, we determine if the user does a thumbs up to then toggle on/off the pointed object.
Communicating to the Kasa smart plugs through wifi.


# 4. Evaluation and Results
When evaluating the system, we first wanted to make sure that it was functioning as expected. As such, the main metric for user interaction/experience was the time taken from the moment the user interact with the system to when the action is triggered. In this case, this means the delay from the moment the user points and raises a thumb, to the moment the smart device toggles on/off. We ran an experiment and measured the time taken over 10 distinct interactions. After collecting the data, we calculated an average delay of less than 1 second, meaning it was unnoticeable. When comparing it to a system such as Alexa, our system presented a shorted delay due to the fact that it does not need to listen to the command and interpret it using a NLP algorithm.

The second metric we measured was the accuracy of our object detection model and the generated "hitbox" for the objects. In this case, we wanted to see how close can two objects be before the system does not behave as expected due to conflicting hitboxes. For our surprise, as long as the objects are not overlapping each other, it performs as expected. This is mainly due to the fact that we are only using one camera, thus limiting our point of view to a stationary observer.

# 5. Discussion and Conclusions

# 6. References

- [Intel Realsense](https://www.intelrealsense.com/developers/)
- [Mediapipe Hand Landmark detection model](https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md)
- [SeleCon](https://ieeexplore.ieee.org/document/7946862)
- [Minuet](https://dl.acm.org/doi/10.1145/3357251.3357581)

# Project Proposal

## 1. Motivation & Objective
### Motivation
As home automation becomes more popular, users may seek a more intuitive way of interacting with smart home devices such as lights and other electronics. However, the current approach used by the majority of the main automation services require the user to name individual devices or scenes to then activate/deactivate with voice commands. As the number of devices in one’s house increases, this process can become somewhat of a burden. But what if we could control devices simply by pointing at them?
### Objective
By using a raspberry pi, a camera, and a Lidar, we are able to first detect a person's fingers, create a depth map, and determine which object the user is pointing to. Then, with a simple command (such as saying "on/off") the smart home device will behave as expected. In addition, we plan on adding a laser pointer to provide the user a visual feedback to which object the system determined he/she is pointing to.

## 2. State of the Art & Its Limitations
### State of the Art
- Setup devices and scenes through app
- User interaction based on voice prompts using devices’/scenes names 
- Gesture controls need wearable devices. 
### Limitations
- Have to remember the name of devices
- Tedious/hard setup process
- Need of a wearable device
  
## 3. Novelty & Rationale

### Approach
Integration of camera and Lidar (tof sensor) to compute direction in which the user is pointing and then interacting with smart devices.
- No need of wearable device
- No need to call the names every devices

## 4. Potential Impact

- Instead of voice control, gesture control will be the major method to control home devices because it’s convenient and smooth.
- People with speech disabilities can also use this solution to control smart home devices if adapted to detect gestures
  

## 5. Challenges
### Challenges:
- Precision of tof sensor detection, the accuracy of 3d metrics
- The model precision to detect human skeletons
- Delays due to computations 
### Risks:
- As we’re dealing with a camera, this could result in privacy issues.


## 6. Requirements for Success

- Be able to detect user hand's landmarks
- Locate smart home devices using camera
- Create depth map using Lidar
- Combine Lidar and camera work to determine position where user is pointing to
- Point laser at chosen device
- Interface with smart device to toggle on/off


## 7. Metrics of Success

Accuracy when determining which device user is pointing to
Time taken to determine device

## 8. Execution Plan

- Integrate camera and lidar to detect user’s gesture and pointing direction. 
- Build connections with smart home devices
- Control the devices based on user’s command
- Optimize the algorithm to make it work correctly and fast

## 9. Related Work

### 9.a. Papers

List the key papers that you have identified relating to your project idea, and describe how they related to your project. Provide references (with full citation in the References section below).

### 9.b. Datasets

List datasets that you have identified and plan to use. Provide references (with full citation in the References section below).

### 9.c. Software

- Mediapipe Hand Landmark detection model

## 10. References

- [Intel Realsense](https://www.intelrealsense.com/developers/)
- [Mediapipe Hand Landmark detection model](https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md)

# Table of Contents
* Abstract
* [Introduction](#1-introduction)
* [Related Work](#2-related-work)
* [Technical Approach](#3-technical-approach)
* [Evaluation and Results](#4-evaluation-and-results)
* [Discussion and Conclusions](#5-discussion-and-conclusions)
* [References](#6-references)

# Abstract

Provide a brief overview of the project objhectives, approach, and results.

Arm command aims to streamline and simplify the user interaction with smart devices in one's home. By leveraging a Lidar, RGB camera, and an intel NUC, we allow the user to simply point to a smart device and toggle it on/off by raising their thumb.
We utilized MediaPipe's hand detection model to identify the user's hand, and then created our own algorithm to create a vector of the index finger to then determine the object being pointed to. By training a YOLO object detector model, we are currently able to indentify a lamp and a computer monitor, allowing the user to control both by simply making a thumbs up. The object's hitbox were created based on the location in the image and then extruded to become a 3d object. We then project tyhe finger's vector trajectory and check for any collion with the hitboxes.
We were able to achieve good accuracy when detecting the user's hand and intersect with the objects, and the system runs with minimal to no latency.

# 1. Introduction

This section should cover the following items:

* Motivation & Objective: What are you trying to do and why? (plain English without jargon)
* State of the Art & Its Limitations: How is it done today, and what are the limits of current practice?
* Novelty & Rationale: What is new in your approach and why do you think it will be successful?
* Potential Impact: If the project is successful, what difference will it make, both technically and broadly?
* Challenges: What are the challenges and risks?
* Requirements for Success: What skills and resources are necessary to perform the project?
* Metrics of Success: What are metrics by which you would check for success?

# 2. Related Work

# 3. Technical Approach

# 4. Evaluation and Results

# 5. Discussion and Conclusions

# 6. References

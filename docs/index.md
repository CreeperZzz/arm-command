# Abstract

Arm command aims to streamline and simplify the user interaction with smart devices in one's home. By leveraging a Lidar, RGB camera, and an intel NUC, we allow the user to simply point to a smart device and toggle it on/off by raising their thumb. We utilized MediaPipe's hand detection model to identify the user's hand, and then created our own algorithm to create a vector of the index finger to then determine the object being pointed to. By training a YOLO object detector model, we are currently able to indentify a lamp and a computer monitor, allowing the user to control both by simply making a thumbs up. The object's hitbox were created based on the location in the image and then extruded to become a 3d object. We then project tyhe finger's vector trajectory and check for any collion with the hitboxes. Our first success metric is related to response time: time elapsed from the moment the user controlled a device until when the action happened. In the current setting, we measured an average response time of less than 1 second. Another success metric is related to detection accuracy: how close can objects be and still be accurately controllable. In our testing, as long as the objects are not overlapping, the system will work as expected.
# Team

* Shiwei Hu
* Lucas Katayama

# Required Submissions

* [Proposal](proposal.md)
* [Midterm Checkpoint Presentation Slides](https://docs.google.com/presentation/d/15--kAbqFbjCWQvVked1_3T1IDAyJp2QNWh9XZ860J-c/edit?usp=sharing)
* [Final Presentation Slides](https://docs.google.com/presentation/d/1Sw6ULTTgbzVjkNbnwfmpK9u3tEsaYvLunu-oBCyh7cY/edit?usp=sharing)
* [Final Report](report.md)
* [Demos](https://drive.google.com/drive/folders/1p5mpjVXLcvMQhLbxxWtxbqmXDbhtCFwg?usp=drive_link)

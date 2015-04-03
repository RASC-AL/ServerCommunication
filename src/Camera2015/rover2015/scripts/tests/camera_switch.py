import numpy as np
import cv2

prev_cam = 0
cam = 0
cap = cv2.VideoCapture(cam)

def test_cam():
    global prev_cam, cam, cap

    while(True):
        
        with open('/tmp/ros_comm') as f:
            conf_str = f.read()
        s = conf_str.split(',')
        cam = int(s[0])
        if cam != prev_cam:
            cap.open(cam)
            prev_cam = cam
        # Capture frame-by-frame
        ret, frame = cap.read()
        # print type(frame)
    
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
test_cam()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

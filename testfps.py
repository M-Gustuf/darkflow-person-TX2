from darkflow.net.build import TFNet
import numpy as np
import cv2
import time

options  = {"model": "cfg/tiny-yolo-voc.cfg", "load": "bin/tiny-yolo-voc.weights", "threshold": 0.25}

tfnet = TFNet(options)

start_time = time.time()
x = 1
counter = 0

cap=cv2.VideoCapture(1)
while(1):  
    ret, frame = cap.read()  
    
    j = 0
    i = 0
    pt1 = []
    pt2 = []
        
    result = tfnet.return_predict(frame)
 
    for j in range(len(result)):
        if(result[j]['label'] == 'person'):
            pt1.append((result[j]['topleft']['x'],result[j]['topleft']['y']))
            pt2.append((result[j]['bottomright']['x'],result[j]['bottomright']['y']))
    
    for i in range(len(pt1)):
        cv2.rectangle(frame,pt1[i],pt2[i],(255,255,255),4)
        cv2.putText(frame, 'person', pt1[i], cv2.FONT_HERSHEY_SIMPLEX,0.8, (0,255,0),2)

    c = cv2.waitKey(1)   
    if c == 27:        
        break

    counter += 1
    if (time.time() - start_time) > x:
        cv2.putText(frame, 'FPS {0}'.format(str(counter / (time.time() - start_time))), (20,20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,0),1)
        counter = 0
        start_time = time.time()

    cv2.imshow("capture", frame)

cap.release()
cv2.destroyAllWindows()

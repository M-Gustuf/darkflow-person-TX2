from darkflow.net.build import TFNet
import numpy as np
import cv2

options  = {"model": "cfg/tiny-yolo-voc.cfg", "load": "bin/tiny-yolo-voc.weights", "threshold": 0.25}

tfnet = TFNet(options)
i = 1

cap=cv2.VideoCapture(1)
while(1):    # get a frame   
    ret, frame = cap.read()    # show a frame   
    
    j = 0
    k = 0
    pt1 = []
    pt2 = []
    result = tfnet.return_predict(frame)
    print(i)
    i = i + 1
    print(result)
    for j in range(len(result)):
        if(result[j]['label'] == 'person'):
            pt1.append((result[j]['topleft']['x'],result[j]['topleft']['y']))
            pt2.append((result[j]['bottomright']['x'],result[j]['bottomright']['y']))
    
    for k in range(len(pt1)):
        cv2.rectangle(frame,pt1[k],pt2[k],(255,255,255),4)
        cv2.putText(frame, 'person', pt1[k], cv2.FONT_HERSHEY_SIMPLEX,0.8, (0,255,0),2)

    cv2.imshow("capture", frame)

    c = cv2.waitKey(100)   
    if c == 27:        
        break

cap.release()
cv2.destroyAllWindows()

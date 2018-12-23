from darkflow.net.build import TFNet
import numpy as np
import cv2
import time
from chassis import *
import time, threading
from flask import Flask, render_template, Response
from flask import request

scene = 0

options  = {"model": "cfg/tiny-yolo-voc.cfg", "load": "bin/tiny-yolo-voc.weights", "threshold": 0.25}

tfnet = TFNet(options)

def car_control():
    start_time = time.time()
    x = 1
    counter = 0
    num=0

    a = chassis()

    cap=cv2.VideoCapture(1)
    while(1):  
        ret, frame = cap.read()  
        height, width, _ = frame.shape
        j = 0
        i = 0
        pt1 = []
        pt2 = []
        area=0
        max_x=0
        max_y=0
        max_area=0    
    
        result = tfnet.return_predict(frame)
 
        for j in range(len(result)):
            if(result[j]['label'] == 'person'):
                pt1.append((result[j]['topleft']['x'],result[j]['topleft']['y']))
                pt2.append((result[j]['bottomright']['x'],result[j]['bottomright']['y']))
       
        for i in range(len(pt1)):
            cv2.rectangle(frame,pt1[i],pt2[i],(255,255,255),4)
            cv2.putText(frame, 'person', pt1[i], cv2.FONT_HERSHEY_SIMPLEX,0.8, (0,255,0),2)
            area=(pt1[i][1]-pt2[i][1])*(pt2[i][0]-pt2[i][0])
            if(area>=max_area):
                max_x=(pt1[i][0]+pt2[i][0])/2
                max_y=(pt1[i][1]+pt2[i][1])/2
                max_area=area
        counter += 1
        
        if (time.time() - start_time) > x:
            cv2.putText(frame, 'FPS {0}'.format(str(counter / (time.time() - start_time))), (20,20),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,0),1)
            counter = 0
            start_time = time.time()
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        global scene
        scene = jpeg.tobytes()
        
        if max_x==0:
            num=num+1
        else: num=0
        if num==0:
            if max_area>60000:
                a.moveStepBackward(0.1)    
            elif max_x > 0.3 * width and max_x < 0.7* width:
                a.moveStepForward(0.2)
            elif max_x<0.3*width:
                a.moveStepLeft(0.0007*(0.3*width-max_x))
                a.moveStepForward(0.1)
            elif max_x>0.7*width:
                a.moveStepRight(0.0007*(max_x-0.7*width))
                a.moveStepForward(0.1)
        elif num!=0:
                a.moveStop()


def web():
    app = Flask(__name__)
    
    @app.route('/', methods=['GET'])
    def index():
        print("0000")
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen():
        while True:
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + scene + b'\r\n\r\n')

    app.run(host = '172.18.16.101', debug=False, threaded = True)

threading_car_control = threading.Thread(target = car_control)
threading_web = threading.Thread(target = web)

threading_car_control.start()
threading_web.start()

threading_car_control.join()
threading_web.join()

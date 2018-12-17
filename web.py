# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 21:40:31 2018

@author: han1h
"""
from flask import Flask, render_template, Response
from flask import request
import sys
import os
import cv2
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.pardir))
print(os.path.abspath(os.path.pardir))
print(os.path.dirname(os.path.abspath(__file__)))

#from camera import VideoCamera, VideoFile, VideoObjectDetection

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        
    def __del__(self):
        self.video.release()
        
    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
        

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    print("0000")
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


if __name__ == '__main__':
    app.run(host='192.168.1.112')#, debug=True)
    


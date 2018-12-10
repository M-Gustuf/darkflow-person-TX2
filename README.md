# Darkflow-Person-TX2

## Intro

A real-time person-detection project based on darkflow ([here](https://github.com/thtrieu/darkflow))running on Nvidia Jetson TX2 Develope Kits.

The project aims at using a portable vehicle to detect and track people automatically. The scene will be displayed remotely.

This project began at Sep, 2018, and are expected to complete at Jan, 2019.

## Dependencies

Python3, tensorflow 1.0, numpy, opencv 3, darkflow.

### Getting started

1. Getting the dependencies ready. 

2. Following the guide [here](https://github.com/thtrieu/darkflow) to install darkflow. You can also learn how to use darkflow in this web. 

## About the model

You can have ways dealing with the model weights.

1. Using the pre-trained YOLO weight files. Several kinds of YOLO can be choosed. In this project, as we only care about the category of person, the smallest net, tiny-yolo-voc, is recomended. It's weight file is in /bin. You can find other weight file  [here](http://pjreddie.com/darknet/yolo/) or [here](https://drive.google.com/drive/folders/0B1tW_VtY7onidEwyQ2FtQVplWEU), and put them in /bin.

2. Train the model yourself. In this project, we are going to train our model.


That's all.
Thank you for reading. 

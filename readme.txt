Name: MD Alifnoor Islam
Student Number: 240341
Project: Image Object Identification System on AWS

Description:
This project implements a cloud-based image object detection system on AWS.
A user uploads an image to an S3 bucket and calls a public API Gateway endpoint.
API Gateway triggers an AWS Lambda function, which uses AWS Systems Manager to
run YOLOv5 object detection on an EC2 instance. The annotated result image is
saved back to S3. The system demonstrates the integration of a machine learning
model with a serverless cloud architecture, separating orchestration (Lambda),
processing (EC2), and storage (S3).

Live API endpoint:
https://8e76ybg4il.execute-api.ap-southeast-2.amazonaws.com/prod/detect

Repository:
https://github.com/mdalifnoorislam-ui/bis202-assignment2

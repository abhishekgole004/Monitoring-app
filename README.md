# Monitoring-app
A real-time monitoring and notification system for AWS EC2 and RDS instances, etc using Python and AWS services. The goal of this project is to enhance operational awareness and ensure timely responses to changes in the state of critical cloud resources. The system is designed for reliability, featuring an infinite loop mechanism with delays to ensure continuous monitoring without overloading AWS resources.
Tech stack used:
	•	Python:  utilized the boto3 library to interact with AWS services and smtplib for sending email notifications.
	•	AWS Services: Amazon EC2, Amazon RDS, Amazon SNS, and CloudWatch Events

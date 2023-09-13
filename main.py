import boto3
import time

aws_access_key_id = '<Access-key>'
aws_secret_access_key = '<Secret-Key>'
region_name = 'us-east-1'

ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
rds = boto3.client('rds', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
sns = boto3.client('sns', region_name='us-east-1')

sns_topic_arn = "arn:aws:sns:us-east-1:860733330773:TestTopic"

def send_sns_notification(subject, message):
    sns.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject=subject
    )

def monitor_ec2_instances():
    previous_states = {}
    
    while True:
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped', 'terminated']}])
        print(instances)
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                if instance_id in previous_states:
                    previous_state = previous_states[instance_id]
                    if state != previous_state:
                        message = f"EC2 instance {instance_id} changed from {previous_state} to {state}."
                        send_sns_notification(f"EC2 Instance State Change", message)
                
                previous_states[instance_id] = state
        time.sleep(10)

def monitor_rds_instances():
    previous_states = {}
    
    while True:
        instances = rds.describe_db_instances()
        
        for instance in instances['DBInstances']:
            instance_id = instance['DBInstanceIdentifier']
            status = instance['DBInstanceStatus']
            
            if instance_id in previous_states:
                previous_status = previous_states[instance_id]
                
                if status != previous_status:
                    message = f"RDS instance {instance_id} changed from {previous_status} to {status}."
                    send_sns_notification(f"RDS Instance Status Change", message)
            
            previous_states[instance_id] = status
        
        time.sleep(10)

if __name__ == '__main__':
    monitor_ec2_instances()
    monitor_rds_instances()
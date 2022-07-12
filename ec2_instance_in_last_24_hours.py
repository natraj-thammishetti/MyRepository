import boto3
from datetime import datetime
from datetime import timezone


def instances_in_last_24_hours():
    try:
        # Initializing ec2 client using boto3 module
        ec2_resource = boto3.client("ec2")
        # describe_instance() method returns the dictionary that contains the details of ec2 instances
        instance_details = ec2_resource.describe_instances()["Reservations"]
        instances = {}
        for instance in instance_details:
            instances[instance['Instances'][0]['InstanceId']] = {}
            instances[instance['Instances'][0]['InstanceId']]['launch_time'] = instance['Instances'][0]['LaunchTime']
            instances[instance['Instances'][0]['InstanceId']]['state'] = instance['Instances'][0]['State']['Name']

        print("List of Instances created in last 24 hours :")
        # printing the instances that were created in less than 24 hours
        count = 0
        for k, v in instances.items():
            time_diff = datetime.now(timezone.utc)-v['launch_time']
            hours = time_diff.total_seconds()//(60*60)
            if hours < 24:
                print("Id :", k, "- Time :", v['launch_time'], "- State :", v['state'])
                count += 1
        print("The Number of Instances created in last 24 hours :", count)
    except Exception as e:
        print(e)


instances_in_last_24_hours()

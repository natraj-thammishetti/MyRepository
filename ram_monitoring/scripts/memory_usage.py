import paramiko
import json
import boto3
import logging
import time
import sys


def get_ram_usage(region, key_name, pem_file_path, exclusion_list, scripts_path):
    EC2 = boto3.client('ec2', region)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    reservations = EC2.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"]
        }
    ]).get("Reservations")
    path = pem_file_path
    privkey = paramiko.RSAKey.from_private_key_file(path)
    for reservation in reservations:
        for instance in reservation["Instances"]:
            ip = instance['PrivateIpAddress']
            instance_id = instance['InstanceId']
            print(ip + ":" + instance_id)
            list = exclusion_list
            if instance_id not in list:
                try:
                    ssh.connect(hostname=ip, username='cloudbreak', pkey=privkey)
                    ftp_client = ssh.open_sftp()
                    ftp_client.put(scripts_path + '/ram_usage.sh', '/tmp/stats.sh')
                    ftp_client.close()
                    stdin, stdout, stderr = ssh.exec_command("bash /tmp/stats.sh")
                except paramiko.AuthenticationException:
                    try:
                        ssh.connect(hostname=ip, username='ec2-user', pkey=privkey)
                        ftp_client = ssh.open_sftp()
                        ftp_client.put(scripts_path + '/ram_usage.sh', '/tmp/stats.sh')
                        ftp_client.close()
                        stdin, stdout, stderr = ssh.exec_command("bash /tmp/stats.sh")
                    except paramiko.AuthenticationException:
                        print('Authentication failed when connecting to' + ip)
                    except TimeoutError:
                        print('Connection timed out for:' + ip + ":" + instance_id)
                except TimeoutError:
                    print('Connection timed out for:' + ip + ":" + instance_id)

                output = stdout.read().decode()
                stdin.close()
                print(output.strip('\n'))
                print("")
                print("----------------------------------------------------------------------------")
                print("")


if __name__ == "__main__":
    print("Opening the variable file...")
    with open(sys.argv[1]) as variable_file:
        variables = json.load(variable_file)

    region = variables['region']
    key_name = variables['key-name']
    pem_file_path = variables['pem-file-path']
    exclusion_list = variables['exclusion-list']
    scripts_path = variables['scripts-path']

    get_ram_usage(region, key_name, pem_file_path, exclusion_list, scripts_path)

    variable_file.close()

from aws.resources import *
import boto3

ec2 = boto3.client("ec2")
s3 = boto3.client("s3")
rds = boto3.client("rds")

def get_all_resources() -> list[AWSResource]:
    """
    Returns a list of all AWS resources in the region: EC2, S3, RDS, EBS, SecurityGroups
    """
    result = []

    # Describe EC2 instances
    ec2_response = ec2.describe_instances()
    for reservation in ec2_response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            result.append(EC2(instance))

    # Describe EBS volumes
    ebs_response = ec2.describe_volumes()
    for volume in ebs_response.get("Volumes", []):
        result.append(EBS(volume))

    # Describe RDS instances
    rds_response = rds.describe_db_instances()
    for db_instance in rds_response.get("DBInstances", []):
        result.append(RDS(db_instance))

    # Describe S3 buckets
    s3_response = s3.list_buckets()
    for bucket in s3_response.get("Buckets", []):
        try:
            tagging_response = s3.get_bucket_tagging(Bucket=bucket["Name"])
        except s3.exceptions.ClientError:
            tagging_response = {"TagSet": []}
        result.append(S3Bucket(bucket, tagging_response))

    # Describe Security Groups
    sg_response = ec2.describe_security_groups()
    for sg in sg_response.get("SecurityGroups", []):
        result.append(SecurityGroup(sg))

    return result

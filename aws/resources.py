# Create an abstract class for AWS resources
class AWSResource:
    def __init__(self):
        self.name = None
        self.id = None
        self.description = None
        self.tags = None
        self.status = "COMPLIANT"
        self.annotations = []

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.id)

    def to_dict(self):
        return {
            "type": self.type,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "status": self.status,
            "annotations": self.annotations,
        }


class EC2(AWSResource):
    type = "EC2"

    # describe_instances: response['Reservations'][]['Instances'][]
    def __init__(self, instance_response):
        super().__init__()
        self.id = instance_response.get("InstanceId", "N/A")
        if "Tags" in instance_response:
            self.tags = {tag["Key"]: tag["Value"] for tag in instance_response["Tags"]}
        else:
            self.tags = {}
        self.name = self.tags.get("Name", "N/A")
        self.description = self.tags.get("Description", "N/A")
        self.instance_type = instance_response.get("InstanceType", "N/A")


class EBS(AWSResource):
    type = "EBS"

    # describe_volumes: response['Volumes'][]
    def __init__(self, volume_response):
        super().__init__()
        self.id = volume_response.get("VolumeId", "N/A")
        if "Tags" in volume_response:
            self.tags = {tag["Key"]: tag["Value"] for tag in volume_response["Tags"]}
        else:
            self.tags = {}
        self.name = self.tags.get("Name", "N/A")
        self.description = self.tags.get("Description", "N/A")


class RDS(AWSResource):
    type = "RDS"

    # describe_db_instances: response['DBInstances'][]
    def __init__(self, db_instance_response):
        super().__init__()
        self.id = db_instance_response.get("DBInstanceIdentifier", "N/A")
        if "TagList" in db_instance_response:
            self.tags = {tag["Key"]: tag["Value"] for tag in db_instance_response["TagList"]}
        else:
            self.tags = {}
        self.name = db_instance_response.get("DBName", "N/A")
        self.description = self.tags.get("Description", "N/A")


class SecurityGroup(AWSResource):
    type = "SecurityGroup"
    ip_permissions = []

    # describe_security_groups: response['SecurityGroups'][]
    def __init__(self, security_group_response):
        super().__init__()
        self.id = security_group_response["GroupId"]
        if "Tags" in security_group_response:
            self.tags = {tag["Key"]: tag["Value"] for tag in security_group_response["Tags"]}
        else:
            self.tags = {}
        self.name = security_group_response.get("GroupName", "N/A")
        self.description = security_group_response.get("Description", "N/A")
        self.ip_permissions = security_group_response.get("IpPermissions", [])

class S3Bucket(AWSResource):
    type = "S3Bucket"

    # list_buckets: response['Buckets'][]
    def __init__(self, list_bucket_response, get_tagging_response):
        super().__init__()
        self.id = list_bucket_response.get("Name", "N/A")
        self.tags = {tag["Key"]: tag["Value"] for tag in get_tagging_response["TagSet"]}
        self.name = list_bucket_response.get("Name", "N/A")
        self.description = self.tags.get("Description", "N/A")

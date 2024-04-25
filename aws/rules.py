from aws.resources import AWSResource, EC2, S3Bucket, SecurityGroup, RDS, EBS
import boto3

s3 = boto3.client("s3")


class Rule:
    resource_types = []
    description = ""

    def evaluate(self, resource: AWSResource) -> bool:
        pass

    def __repr__(self):
        return self.__class__.__name__


class EC2InstanceTypeRule(Rule):
    resource_types = [EC2]
    description = "EC2 instance type must be in t2.micro, t3.small, t3a.medium"

    def evaluate(self, resource: EC2) -> bool:
        if type(resource) not in self.resource_types:
            raise ValueError("Resource type not supported")
        return resource.instance_type in ["t2.micro", "t3.small", "t3a.medium"]


class S3BucketEncryptionRule(Rule):
    resource_types = [S3Bucket]
    description = "S3 bucket must be encrypted with a KMS key"

    def evaluate(self, resource: S3Bucket) -> bool:
        if type(resource) not in self.resource_types:
            raise ValueError("Resource type not supported")

        # Response has KMSMasterKeyID if encrypted
        response = s3.get_bucket_encryption(Bucket=resource.name)
        compliant = False
        for rule in response["ServerSideEncryptionConfiguration"].get("Rules", []):
            if rule.get("ApplyServerSideEncryptionByDefault", {}).get("KMSMasterKeyID"):
                compliant = True
                break
        return compliant


class SGNoUnrestrictedRule(Rule):
    resource_types = [SecurityGroup]
    description = "Security group must not have unrestricted ingress rules (0.0.0.0/0)"

    def evaluate(self, resource: SecurityGroup) -> bool:
        if type(resource) not in self.resource_types:
            raise ValueError("Resource type not supported")

        # Check for CIDR block
        for permission in resource.ip_permissions:
            for ip_range in permission.get("IpRanges", []):
                if ip_range["CidrIp"] == "0.0.0.0/0":
                    return False
        return True


class RequiredTagsRule(Rule):
    resource_types = [EC2, S3Bucket, SecurityGroup, RDS, EBS]
    description = (
        "Resource must have required tags Group:CyberDevOps and Environment:Development"
    )

    def evaluate(self, resource: AWSResource) -> bool:
        if type(resource) not in self.resource_types:
            raise ValueError("Resource type not supported")
        if (
            resource.tags.get("Group") == "CyberDevOps"
            and resource.tags.get("Environment") == "Development"
        ):
            return True
        return False


RULES = [
    EC2InstanceTypeRule(),
    S3BucketEncryptionRule(),
    SGNoUnrestrictedRule(),
    RequiredTagsRule(),
]

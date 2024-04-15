from flask import Blueprint, jsonify
from models import CSV, db
from config import BUCKET_NAME
import boto3
import pandas
from datetime import datetime

security_groups_bp = Blueprint("security_groups", __name__)

s3 = boto3.client("s3")
ec2 = boto3.client("ec2")
config = boto3.client("config")


@security_groups_bp.route("/api/security_groups", methods=["POST"])
def security_groups_check():
    security_groups = ec2.describe_security_groups()["SecurityGroups"]

    for sg in security_groups:
        sg["ComplianceType"] = "COMPLIANT"
        sg["Annotations"] = []

        response = config.get_compliance_details_by_resource(
            ResourceType="AWS::EC2::SecurityGroup",
            ResourceId=sg["GroupId"],
        )

        for result in response["EvaluationResults"]:
            if result["ComplianceType"] == "NON_COMPLIANT":
                sg["ComplianceType"] = "NON_COMPLIANT"
                sg["Annotations"].append(result["Annotation"])

    # Convert the list of security groups to a pandas dataframe
    df = pandas.DataFrame(security_groups)
    ordered_columns = [
        "GroupId",
        "GroupName",
        "Description",
        "VpcId",
        "ComplianceType",
        "Annotations",
    ]
    rest_of_columns = [col for col in df.columns if col not in ordered_columns]
    ordered_columns.extend(rest_of_columns)
    df = df[ordered_columns]
    try:
        timestamp = datetime.now().strftime("%s")
        # Add to csv table
        csv = CSV(
            filename="security_groups/sg-report-{}.csv".format(timestamp),
            generated_at=datetime.now(),
        )
        db.session.add(csv)
        db.session.commit()

        # Upload the dataframe to S3 as csv
        df.to_csv("/tmp/security_groups.csv", index=False)
        s3 = boto3.client("s3")
        s3.upload_file(
            "/tmp/security_groups.csv",
            BUCKET_NAME,
            "security_groups/sg-report-{}.csv".format(timestamp),
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(
        {"status": "success", "csv": csv.to_dict(), "security_groups": security_groups}
    )

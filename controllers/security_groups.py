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
    # Get all the config rules
    config_rules = config.describe_config_rules()["ConfigRules"]

    # Get all the security groups in the region
    security_groups_response = ec2.describe_security_groups()["SecurityGroups"]

    # Initialize compliance information for all security groups and store in a dictionary for quick access
    security_groups = {}
    for sg in security_groups_response:
        sg["ComplianceType"] = "COMPLIANT"
        sg["Annotations"] = []
        security_groups[sg["GroupId"]] = sg

    # Check compliance for each config rule
    for rule in config_rules:
        response = config.get_compliance_details_by_config_rule(
            ConfigRuleName=rule["ConfigRuleName"], ComplianceTypes=["NON_COMPLIANT"]
        )

        for result in response["EvaluationResults"]:
            resource_id = result["EvaluationResultIdentifier"][
                "EvaluationResultQualifier"
            ]["ResourceId"]
            if resource_id in security_groups:
                security_groups[resource_id]["ComplianceType"] = "NON_COMPLIANT"
                security_groups[resource_id]["Annotations"].append(
                    result.get("Annotation", rule["Description"])
                )

    df = pandas.DataFrame(security_groups.values())
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

    # Sort the DataFrame based on the count of annotations in descending order
    df["non_compliant_count"] = df["Annotations"].apply(len)
    df = df.sort_values(by="non_compliant_count", ascending=False)

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
        {
            "status": "success",
            "csv": csv.to_dict(),
            "security_groups": list(security_groups.values()),
        }
    )

from flask import Blueprint, jsonify
from models import CSV, db
from config import BUCKET_NAME, TEMP_FOLDER
import boto3
import pandas
from datetime import datetime
from utils import get_all_resources
from aws.rules import RULES

rules_bp = Blueprint("rules", __name__)

s3 = boto3.client("s3")
ec2 = boto3.client("ec2")
config = boto3.client("config")


@rules_bp.route("/api/rules", methods=["POST"])
def rules_check():
    resources = get_all_resources()
    for resource in resources:
        for rule in RULES:
            if type(resource) in rule.resource_types:
                print(f"Evaluating {resource} for {rule}")
                if not rule.evaluate(resource):
                    resource.status = "NON_COMPLIANT"
                    resource.annotations.append(rule.description)

    df = pandas.DataFrame([resource.to_dict() for resource in resources])

    # Sort the DataFrame based on the count of annotations in descending order
    df["non_compliant_count"] = df["annotations"].apply(len)
    df = df.sort_values(by="non_compliant_count", ascending=False)

    try:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"noncompliant-resources-{timestamp}.csv"
        # Add to csv table
        csv = CSV(
            filename=filename,
            generated_at=datetime.now(),
        )
        db.session.add(csv)

        # Upload the dataframe to S3 as csv
        df.to_csv(f"{TEMP_FOLDER}/check.csv", index=False)
        s3 = boto3.client("s3")
        s3.upload_file(
            f"{TEMP_FOLDER}/check.csv",
            BUCKET_NAME,
            filename,
        )

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(
        {
            "status": "success",
            "csv": csv.to_dict(),
            "resources": resources,
        }
    )

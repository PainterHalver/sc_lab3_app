from flask import Blueprint, jsonify, redirect
from models import CSV, db
from config import BUCKET_NAME
import boto3

s3 = boto3.client("s3")
csv_bp = Blueprint("csv", __name__)


@csv_bp.route("/api/csv", methods=["GET"])
def get_csv():
    csvs = CSV.query.order_by(CSV.id.desc()).all()
    return jsonify([csv.to_dict() for csv in csvs])


@csv_bp.route("/api/csv/<int:id>", methods=["GET"])
def download_csv(id):
    csv = CSV.query.get(id)
    url = s3.generate_presigned_url(
        "get_object", Params={"Bucket": BUCKET_NAME, "Key": csv.filename}, ExpiresIn=43200
    )
    return redirect(url)

import boto3
import os
import glob
import datetime
from dotenv import load_dotenv


load_dotenv()
data_path = glob.glob("../data/dados.*")
data=datetime.datetime.now().strftime("%d%m%Y")

aws_access_key= os.getenv("S3_ACCESS_KEY")
aws_secret_key= os.getenv("S3_SECRET_KEY")
aws_region_name= os.getenv("S3_REGION")
aws_bucket_name= os.getenv("S3_BUCKET_NAME")

def main():
    session = boto3.client(
        service_name="s3",
        region_name=aws_region_name,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )

    for path in data_path:
        file_name = f"{data}/{os.path.basename(path)}"
        response = session.upload_file(path, aws_bucket_name, file_name)

    print(f"uploading {len(data_path)} files to {aws_bucket_name} \nerrors:{response}")
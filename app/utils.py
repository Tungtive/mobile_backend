from werkzeug.utils import secure_filename
import boto3
from flask import current_app
import random
from geopy.distance import geodesic

s3 = boto3.client("s3")


def upload_file_to_s3(file, resource_path):
    filename = secure_filename(file.filename)
    object_name = f"{resource_path}/{filename}"
    s3.upload_fileobj(
        file,
        current_app.config["AWS_BUCKET_NAME"],
        object_name,
        ExtraArgs={"ContentType": file.content_type},
    )
    return object_name


def generate_s3_singed_url(object_name):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": current_app.config["AWS_BUCKET_NAME"], "Key": object_name},
        ExpiresIn=3600,
    )

def generate_randomCode():
 
    checkcode = ""
 
    for i in range(6):
        current = random.randrange(0,9,2)
        if current != i:
            temp = chr(random.randint(65,90))
        else:
            temp = random.randint(0,9)
        checkcode += str(temp)
    return checkcode

def compute_distance(loc1,loc2):
    x1 = loc1[0]
    y1 = loc1[1]
    x2 = loc2[0]
    y2 = loc2[1]
    return geodesic((x1,y1),(x2,y2)).km
import json
import boto3
from datetime import datetime, timezone, timedelta

# define s3 client and s3 resource
s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')


def lambda_handler(event, context):
    count_del = 0
    print("entered Lambda_Handler")

    how_many_days = 1
    today = datetime.now(timezone.utc)  # get the time of today
    date_of_5_days = today - timedelta(days=how_many_days)  # get the date 5 days ago
    print(date_of_5_days)

    objects = s3.list_objects(Bucket='anipoevents')  # get all the objects in the Bucket
    print(len(objects["Contents"]))

    for object in objects["Contents"]:  # iterate over all the objects and check if the modified date pass 5 days if its is del it.
        print("entered for loop")
        if object["LastModified"] <= date_of_5_days:
            print(object["Key"])
            s3_resource.Object('anipoevents', object['Key']).delete()  # del the object from the Bucket
            count_del += 1
            print("del complete")

    print("We delete in total " + str(count_del))

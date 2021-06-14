import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

# upload a new file
data = open("yellowstone.jpeg", "rb")
s3.Bucket('jobsbucket').put_object(Key="yellowstone.jpeg", Body=data)
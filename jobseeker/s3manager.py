import boto3

# file_name = r"C:\Users\NIKHITH_RAJ.K\OneDrive\Desktop\python JD.txt"
bucket_name = "recruiter-finder"
object_name = r"pytho_jd.txt"

aws_access_key_id = 'AKIAUPMYNIJVZ55VKUVJ'#YOUR_AWS_ACCESS_KEY'
aws_secret_access_key = 'RwPYuP28IEnM1Xcv7Epp5AybUSrTdNi6g4yRl74m'#'YOUR_AWS_SECRET_KEY'
aws_region_name = 'eu-north-1'#'YOUR_REGION_NAME' 

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name
)
# s3_client.upload_file(file_name, bucket_name, object_name)
# file_name = r"E:\test\newfile.txt"
# s3_client.download_file(bucket_name, object_name, file_name)
# response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='folder_1')
# s3_client.delete_object(Bucket=bucket_name, Key=object_name )
# print(response)

presigned_url = s3_client.generate_presigned_url('get_object',
 Params={
                'Bucket': bucket_name,
                'Key': object_name,
                'ResponseContentDisposition': 'inline',
                'ResponseContentType': 'text/plain'  # Sets MIME type to plain text
            },ExpiresIn=200, 
    )
print(presigned_url)
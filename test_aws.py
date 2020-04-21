import boto3
client = boto3.client('textract')
#s3 = boto3.resource('s3')
#file_name = input('Enter file name,the file must be in /home/pi/Downloads directory  ')
#s3.meta.client.upload_file('/home/pi/Downloads/' + file_name, 'youcode', 'w1.jpeg')
response = client.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': 'checkyoucode',
            'Name': 'w1.jpeg'
        }
    }
)
#print(file_name)
print('response:',response)

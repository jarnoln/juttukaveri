from boto3 import client, Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys


def text_to_speech(session, text, out_file_path='polly.mp3'):
    polly = session.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(
            Text=text,
            LanguageCode="fi-FI",
            OutputFormat="mp3",
            VoiceId="Suvi",
            Engine="neural"
        )
        print(response)
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            try:
                with open(out_file_path, "wb") as out_file:
                    out_file.write(stream.read())
                return out_file_path
            except IOError as error:
                print(error)
                sys.exit(-1)
    return None


def upload_file_to_s3(session, file_path):
    bucket_name = 'juttukaveri'
    region = 'eu-central-1'
    s3 = session.client('s3', region_name=region)
    response = s3.list_buckets()
    buckets = response['Buckets']
    print('Buckets:')
    found = False
    for bucket in buckets:
        name = bucket['Name']
        print(name)
        if name == bucket_name:
            found = True
            break
    if not found:
        location = {'LocationConstraint': region}
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

    try:
        s3.upload_file(file_path, bucket_name, file_path)
    except ClientError as e:
        print(e)
        sys.exit(-1)
    params = {
        'Bucket': bucket_name,
        'Key': file_path
    }
    response = s3.generate_presigned_url('get_object', Params=params, ExpiresIn=3600)
    print('audio url:')
    print(response)
    return response


if __name__ == "__main__":
    session = Session(profile_name="default")
    file_path = text_to_speech(session, "Hei! Kuka sinä olet?")
    url = upload_file_to_s3(session, file_path)

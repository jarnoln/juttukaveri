from boto3 import client, Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import logging
import sys


def get_voice_for_langauge(language_code: str) -> str:
    # See https: // docs.aws.amazon.com / polly / latest / dg / voicelist.html
    if language_code == 'fi-FI':
        return 'Suvi'
    elif language_code == 'cmn-CN':  # Chinese (Mandarin)
        return 'Zhiyu'
    return 'Kimberly'  # One of female voices for 'en-US'

class AwsApi:
    def __init__(self):
        self.session = Session(profile_name="default")

    def text_to_speech(self, text: str, out_file_path: str = 'polly.mp3', language_code: str = 'fi-FI') -> str:
        logger = logging.getLogger(__name__)
        logger.info('text_to_speech')
        logger.info(text)
        polly = self.session.client("polly")
        voice_id = get_voice_for_langauge(language_code)
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(
                Text=text,
                LanguageCode=language_code,
                OutputFormat="mp3",
                VoiceId=voice_id,
                Engine="neural"
            )
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            logger.error(error)
            sys.exit(-1)

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                with open(out_file_path, "wb") as out_file:
                    out_file.write(stream.read())
                return out_file_path
        return ''

    def upload_file_to_s3(self, file_path: str) -> str:
        bucket_name = 'public-bucket-jk'
        region = 'eu-central-1'
        s3 = self.session.client('s3', region_name=region)
        response = s3.list_buckets()
        buckets = response['Buckets']
        found = False
        for bucket in buckets:
            name = bucket['Name']
            if name == bucket_name:
                found = True
                break
        if not found:
            location = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

        s3.upload_file(file_path, bucket_name, file_path, ExtraArgs={'ACL': 'public-read'})
        params = {
            'Bucket': bucket_name,
            'Key': file_path
        }
        response = s3.generate_presigned_url('get_object', Params=params, ExpiresIn=3600)
        return response


if __name__ == "__main__":
    awsApi = AwsApi()
    local_file_path = awsApi.text_to_speech("Hei! Kuka sinä olet?")
    url = awsApi.upload_file_to_s3(local_file_path)

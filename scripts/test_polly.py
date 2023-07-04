from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys

session = Session(profile_name="default")
polly = session.client("polly")

try:
    # Request speech synthesis
    response = polly.synthesize_speech(
        Text="Odota hetki, kun mietin.",
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
        out_file_name = "odota_hetki_kun_mietin.mp3"
        try:
            with open(out_file_name, "wb") as out_file:
                out_file.write(stream.read())
        except IOError as error:
            print(error)
            sys.exit(-1)

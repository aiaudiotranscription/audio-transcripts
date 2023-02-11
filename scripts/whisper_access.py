import requests
import json


API_URL = "https://transcribe.whisperapi.com"

HEADER = {
'Authorization': 'Bearer ' + json.load(open("/root/Login_details.json"))['api']['key']
}


# read the sound file in input_file and use pipe to transcribe it. Will generate a pipe if none is given
def transcribe_file(input_file, output_file):
    data = {
        "fileType": input_file.split('.')[-1],  # default is wav
        "diarization": "false",
        "task": "transcribe"  # default is transcribe. Other option is "translate"
    }
    response = requests.post(API_URL, headers=HEADER, files={'file': open(input_file, 'rb')}, data=data)
    output = response.json()['text']
    open(output_file, 'w').write(output)

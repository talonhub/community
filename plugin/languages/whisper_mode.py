import json
import requests
from talon import Module

mod = Module()
mod.mode("whisper")


@mod.action_class
class Actions:
    def whisper_start_dictation():
        """Start dictation mode"""
        # Sending a POST request
        response = requests.post('http://pc.local:5006/start')

        # Checking the response
        if response.status_code == 200:
            print("Request was successful")
            print(response.text)
        else:
            print(f"Failed with status code: {response.status_code}")
    
    def whisper_stop_dictation() -> str:
        """Stop dictation mode"""
        # Sending a POST request
        response = requests.post('http://pc.local:5006/stop')
        # Checking the response
        if response.status_code == 200:
            print("Request was successful")
            # decode json
            data = json.loads(response.text)
            if 'transcription' in data:
                print(f"transcript: {data['transcription']}")
                transcription = data['transcription']
                transcription = transcription.rstrip('\n')
                return transcription
                
            # print(response.text)
        else:
            print(f"Failed with status code: {response.status_code}")
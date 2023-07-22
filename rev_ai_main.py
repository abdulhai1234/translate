import speech_recognition as sr
import pyttsx3
import soundfile as sf
import numpy as np
from googletrans import Translator
import pyttsx3
from gtts import gTTS
import threading
import os
from rev_ai import apiclient as api
from rev_ai.models import MediaConfig, CustomVocabulary
from rev_ai.models.customer_url_data import CustomerUrlData
import argparse
import whisper
import warnings 
from typing import IO
import re
warnings.filterwarnings('ignore')
import asyncio
import time
from time import sleep

def translate(text, sr='en', des='ur'):
    translator=  Translator(service_urls=['translate.googleapis.com'])
    result=translator.translate(text,sr=sr, dest=des)
    return result.text

def play(text,lang,model):
    # Specify the language as 'ur' for Urdu
    tts = gTTS(text, lang=lang)

    # Save the speech audio to a file
    audio_file = f"./{str(model)}_output.mp3"
    tts.save(audio_file)
    return audio_file
    # Play the speech audio using the default media player
    # os.system(f"start {audio_file}")
    # Function to play audio and delete file
    # def play_and_delete():
        # Play the speech audio using the default media player
        # os.system(f"start {audio_file}")

        # Wait for a few seconds (adjust as needed)
        # This allows the media player to start playing the audio
        # before the file is deleted
        # threading.Timer(5, delete_file).start()

    # Function to delete the audio file
    # def delete_file():
    #     os.remove(audio_file)

    # Call the function to play audio and delete file
    # play_and_delete()


class RevAI:
    def __init__(self,token,input_lang,output_lang) -> None:
            self.client = api.RevAiAPIClient(token)
            self.text=''
            self.input_lang=input_lang
            self.output_lang=output_lang
    def process_audio(self, audio_file):
        if self.input_lang=="ur":
            self.input_lang="hi"
        try:
            print(self.input_lang)
            job =self.client.submit_job_local_file(audio_file,language=self.input_lang)
            #  Pass the byte stream to the submit_job_bytes method
            # job = self.client.submit_job_bytes(audio_file, content_type="audio/x-wav")
            print("procceding with jod id:",job.id)
            job_id=job.id
            while (job.status.name == 'IN_PROGRESS'):
                details = self.client.get_job_details(job_id)
                print("Job status: " + details.status.name)
                # if successful, print result
                if (details.status.name == 'TRANSCRIBED'):
                    self.text=self.client.get_transcript_text(job_id)
                    print("done TRANSCRIBED")
                    break
                # if unsuccessful, print error
                if (details.status.name == 'FAILED'):
                    print("Job failed: " + details.failure_detail)
                    break
        except Exception as e:
            print(f"Error occurred: {e}")
        text_without_double_spaces = re.sub(r'\s+', ' ', self.text)
        pattern = r"Speaker \d+ \d{2}:\d{2}:\d{2} "
        # Use re.sub to remove the matched pattern
        result_text = re.sub(pattern, "", text_without_double_spaces.strip())
        translated_chunks = []
        for x in result_text.split("."):
            translated= translate(x,sr=self.input_lang,des=self.output_lang)
            translated_chunks.append(translated)
        result_text = '.'.join(translated_chunks)

        return play(result_text,self.output_lang,"rev_ai")



# if __name__=="__main__":
#     rev_ai=RevAI()
#     start_time = time.time()
#     result=rev_ai.process_audio(audio)
#     end_time = time.time()
#     count(start_time,end_time)
#     print("reuslt:", result)
        
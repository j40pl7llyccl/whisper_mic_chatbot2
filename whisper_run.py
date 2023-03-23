import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import queue
import tempfile
import os
import threading
import click
import torch
import numpy as np
import json
from gtts import gTTS
import pygame
import openai

class SpeechToText:
    

    def __init__(self, model):
        self.model = model
        self.audio_model = whisper.load_model(self.model)
        
    def record_audio(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            if True:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source)
            else:
                pass

            with tempfile.NamedTemporaryFile(delete=True) as fp:
                try:
                    # Assume that audio.get_wav_data() returns the WAV data as a bytes object
                    wav_data = audio.get_wav_data()
                    # Convert the bytes object to an in-memory file object
                    wav_file = io.BytesIO(wav_data)
                    # Create an AudioSegment object from the in-memory file object
                    audio_segment = AudioSegment.from_wav(wav_file)
                    #将音频剪辑导出为 WAV 格式，并保存为指定的文件名
                    audio_file = f"{fp.name}.wav"
                    print('audio_file ',  audio_file)
                    print('[recording:]')
                    audio_segment.export(audio_file, format="wav")

                except sr.UnknownValueError:
                    print("can't not recognize of the sentence")
                except sr.RequestError as e:
                    print("get some error：", e)
        return audio_file, audio
    
    def transcribe(self, audio_model, audio_file, audio):
        #audio_data = np.frombuffer(audio_file.raw_data, dtype=np.int16)
        result = audio_model.transcribe(audio_file)
        predicted_text = result["text"]

        try:
            if predicted_text:
                print("listen to your sentence: " + predicted_text)
                return predicted_text
                os.remove(audio_file)
                
        except Exception as e:
            print("An error occurred:", str(e))

            
if __name__ == '__main__':

    model = "small.en"
    st = SpeechToText(model)
    audio_model = whisper.load_model(model)
    while True:
        audio_file, audio = st.record_audio()
        predicted_text = st.transcribe(audio_model, audio_file, audio)
        predicted_text = str(predicted_text)
        if predicted_text.lower().replace(" ", "").replace(".", "") == "go":
            print('[finish-------------]')
            break
        else:
            pass
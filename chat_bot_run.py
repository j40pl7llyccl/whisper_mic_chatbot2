import argparse
import io
import os
import speech_recognition as sr
import json
import openai
import pygame
import tempfile
from gtts import gTTS


class Chat_bot():

    def __init__(self, openai_key):
        self.openai_key = openai_key
        
    def listenTo(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language='en-US')
                print("[result---------]：" + text)
                return text
            except Exception as e:
                print("the error：", e)

                
    def speak(self, sentence, lang):
        pygame.init()
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts = gTTS(text=sentence, lang=lang)
            tts.save("{}.mp3".format(fp.name))
            pygame.mixer.music.load('{}.mp3'.format(fp.name))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
            
    def run(self):
        
        os.environ['OPENAI_Key']=self.openai_key
        openai.api_key=os.environ['OPENAI_Key']
        keep_prompting=True
        while keep_prompting:
            print('----------------------------------------------------------------------------------------------------')
            prompt=self.listenTo()
            if prompt=='exit':
                keep_prompting=False
            else:
                response=openai.Completion.create(engine='text-davinci-003',prompt=prompt,max_tokens=200)
                response_sentence = response['choices'][0]['text']
                self.speak(response_sentence, "en-US")
                #print(response_sentence)
        


if __name__ == "__main__":
    json_file = open('config.json')
    print(json_file)
    config = json.load(json_file)
    openai_key = config['API_KEY']    
    chat_bot = Chat_bot(openai_key)
    chat_bot.run()
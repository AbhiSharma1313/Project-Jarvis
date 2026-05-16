from google import genai
import speech_recognition as sr
import webbrowser  # Built-in module
import pyttsx3
import musicLib
import requests


recognizer = sr.Recognizer()  #Helps u to use recognition speech functionality
#engine = pyttsx3.init()   # Initialize pyttsx3
newsapi = "YOUR-NEWS-API-KEY"


def speak(text):
    engine = pyttsx3.init()  #Initialize the speak function every single time, don't use this outside the function
    engine.say(text)
    engine.runAndWait()


def aiprocess(command):
    client = genai.Client(api_key="YOUR-API-KEY")
    completion = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=command
    )
    return completion.text

    

    

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLib.music[song]
        webbrowser.open(link)

    elif "tell news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR-API-KEY")
        if r.status_code == 200:
            data = r.json()   # Convert response to dictionary
    
            articles = data.get("articles", [])

            for article in articles:
                speak(article['title'])


    else:
        #Gemini will handle the request
        output =aiprocess(c)
        print(output)
        speak(output)
       
    

        

if __name__== "__main__":
    speak("Initializing Jarvis......")

    while True:

# Listen wake word Jarvis

        r = sr.Recognizer()
        print("Recognizing.....")
        
        # recognize speech using Sphinx but we are using google(accurate)
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit= 1) 

            word = r.recognize_google(audio)        
            if(word.lower()== "jarvis"):
                speak("Yes Boss")
                

                #Listen for command
                with sr.Microphone() as source:
                    print("Tell....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processcommand(command)

                    
        except Exception as e:
            print("Error; {0}".format(e))




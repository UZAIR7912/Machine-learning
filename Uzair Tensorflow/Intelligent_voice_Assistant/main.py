from neuralintents import BasicAssistant
import speech_recognition as sr
import pyttsx3 as tts
import sys
recognizer =sr.Recognizer()
speaker = tts.init()
speaker.setProperty("rate",150)
todo_list = []
def create_note():
    global recognizer
    speaker.say("what do you want to add ")
    speaker.runAndWait()
    print("done")
    done = False
    while not done:
        try:
            micro = sr.Microphone()
            with micro as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio =recognizer.listen(mic)
                note = recognizer.recognize_google(audio)
                note = note.lower()
                
                speaker.say("Choose a file name")
                speaker.runAndWait()
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio =recognizer.listen(mic)
                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(f"{filename}.txt","w") as f:
                f.write(note)
                done = True
                speaker.say(f"i successfully created the note {filename}")
                speaker.runAndWait
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("Sorry! I did not understand you! Please Try Again")
            speaker.runAndWait()

def add_todo():
    global recognizer
    speaker.say("what do you want to add to your list?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio =recognizer.listen(mic)
                item = recognizer.recognize_google(audio)
                item = item.lower()
                todo_list.append(item)
                done = True
                speaker.say(f"I have successfully added {item} to your list")
                speaker.runAndWait()
        except sr.UnknownValueError:
            speaker.say("Sorry! I did not understand you! Please Try Again")
            speaker.runAndWait()

def show_todo():
        if not todo_list == []:
            speaker.say("Here are the items on your list:")
            for item in todo_list:
                speaker.say(f"number {(item.index())+1} :       {item}")
            speaker.runAndWait()
        else:
            speaker.say("Dear, you don't have anything in your list!")
            speaker.runAndWait()

def remove_todo():
    global recognizer
    if not todo_list == []:
        speaker.say("What do you want to remove")
        speaker.runAndWait()
        done = False
    else:
        speaker.say("There is nothing in your list to remove")
        speaker.runAndWait()
    while not done:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio =recognizer.listen(mic)
                item = recognizer.recognize_google(audio)
                item = item.lower()
                try:    
                    todo_list.remove(item)
                except ValueError:
                    speaker.say("Sorry! The item you are trying to remove does not exist")
                    speaker.runAndWait()
                done = True
                speaker.say(f"I have successfully added {item} to your list")
                speaker.runAndWait()
        except sr.UnknownValueError:
            speaker.say("Sorry! I did not understand you! Please Try Again")
            speaker.runAndWait()

def greeting():
    speaker.say("Hello! How can i assist you today?")
    speaker.runAndWait()

def exiting():
    speaker.say("goodbye! Have a nice day!")
    speaker.runAndWait()
    sys.exit(0)

mappings = {"greeting": greeting,
            "add_todo": add_todo,
            "create_note": create_note,
            "remove_todo":remove_todo,
            "show_todos":show_todo,
            "exit":exiting}
assistant = BasicAssistant("intents.json",mappings)
assistant.load_model()
while True:
    try:
        micro = sr.Microphone()
        with micro as mic:
            recognizer.adjust_for_ambient_noise(mic,duration=0.2)
            audio = recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            assistant.process_input(message)
    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
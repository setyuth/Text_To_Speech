import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed (words per minute)
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
# engine.say("សួស្តី! នេះជាការធ្វើតេស្ត អក្សរទៅជាសម្លេង!")
engine.say("Hello, this is a test!")
engine.runAndWait()
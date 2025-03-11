from gtts import gTTS
import os

# text = "Hello, this is a test!"
# tts = gTTS(text=text, lang='en')
text = "ទីតាំង​ប្រព្រឹត្ត​បទ​ល្មើស​ឆបោក​តាម​អនឡាញ​ប្រព្រឹត្ត​ដោយ​ជន​បរទេស បាន​ទៅ​ដល់​ខេត្ត​មណ្ឌល​គិរី។ នៅ​ថ្ងៃទី៦​ ខែមីនា កម្លាំង​នគរបាល​នៃ​អគ្គស្នងការដ្ឋាន​នគរ​បាល​ជាតិ បាន​បើក​ប្រតិបត្តិការ​បង្ក្រាប​នៅ​អគារ​មេគង្គ៧៤ ​ក្រុង​សែនមនោរម្យ ខេត្តមណ្ឌលគិរី ​ឃាត់​ខ្លួន​ជនបរទេស​២៥៨​នាក់។"
tts = gTTS(text=text, lang='km')
tts.save("output.mp3")
os.system("start output.mp3")  # 'start' for Windows, use 'open' for macOS or 'xdg-open' for Linux
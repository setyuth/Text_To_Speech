# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "27d8bc824e97439b8afdd3f9a6372604"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("output.mp3")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)
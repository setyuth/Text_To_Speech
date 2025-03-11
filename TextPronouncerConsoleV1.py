import PyPDF2
import docx
from gtts import gTTS
import pyglet
import os
import time
import uuid
import threading
import sys

def read_pdf(file_path):
    """Reads PDF content with error handling."""
    try:
        with open(file_path, 'rb') as file:
            return "".join(page.extract_text() for page in PyPDF2.PdfReader(file).pages)
    except Exception as e:
        print(f"PDF Error: {e}")
        return ""

def read_docx(file_path):
    """Reads DOCX content with error handling."""
    try:
        doc = docx.Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception as e:
        print(f"DOCX Error: {e}")
        return ""

def play_audio(text, lang, filename, audio_finished):
    """Plays audio and sets a flag after completion."""
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        sound = pyglet.media.load(filename)
        player = sound.play()
        audio_duration = sound.duration or 5
        timeout = max(audio_duration + 2, 5)
        start_time = time.time()
        while player.playing and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        player.delete()
        time.sleep(2)  # Wait 2 seconds after audio finishes
        audio_finished[0] = True  # Set flag to True
    except Exception as e:
        print(f"Audio Error (Thread): {e}")
    finally:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

def text_to_speech(text, lang, audio_finished):
    """Initiates audio playback in a separate thread."""
    try:
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        thread = threading.Thread(target=play_audio, args=(text, lang, filename, audio_finished))
        thread.start()
    except Exception as e:
        print(f"Audio Error (Main): {e}")

def process_text(text, lang, audio_finished):
    """Processes text for TTS or displays options if empty."""
    if text.strip():
        print(f"Processing: '{text[:50]}...' ({lang})")
        text_to_speech(text, lang, audio_finished)
    else:
        print("Empty text to process.")
        time.sleep(3)
        display_options()

def get_language_choice():
    """Gets language choice from user, defaults to Khmer."""
    languages = {
        "1": ("km", "Khmer"),
        "2": ("zh-CN", "Chinese"),
        "3": ("en", "English"),
        "4": ("th", "Thai"),
        "5": ("vi", "Vietnamese"),
        "6": ("ko", "Korean"),
    }
    print("\nSelect Language:")
    for key, (code, name) in languages.items():
        print(f"{key}. {name}")
    while True:
        choice = input("Enter choice (default Khmer): ").strip()
        if not choice:
            return "km"
        if choice in languages:
            return languages[choice][0]
        else:
            print("Invalid choice, using Khmer (default).")
            return "km"

def clear_input_buffer():
    """Clears the input buffer."""
    try:
        if sys.platform.startswith('win'):
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            try:
                import termios
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            except ModuleNotFoundError:
                pass  # termios not available, do nothing
    except Exception as e:
        print(f"Error clearing input buffer: {e}")

def display_options():
    """Displays selection options."""
    print("\n1. Input text\n2. PDF file\n3. DOCX file\n4. Exit")

def main():
    """Main application loop."""
    print("Text Pronouncer - Supports PDF/DOCX/Text")
    while True:
        try:
            display_options()
            choice = input("Choose: ").strip()

            if choice == '4':
                print("Goodbye!")
                break

            if choice == '1':
                text = input("Enter text: ")
            elif choice == '2':
                text = read_pdf(input("PDF path: "))
            elif choice == '3':
                text = read_docx(input("DOCX path: "))
            else:
                print("Invalid choice")
                clear_input_buffer()
                continue

            if text:
                audio_finished = [False]  # Flag to track audio completion
                lang = get_language_choice()
                process_text(text, lang, audio_finished)
                clear_input_buffer()
                while not audio_finished[0]:
                    time.sleep(0.1)  # Wait for audio to finish
            else:
                print("No text found")
                process_text("", "en", [True])  # Trigger display options for empty text.

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
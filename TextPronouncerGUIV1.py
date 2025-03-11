import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
from docx import Document
from gtts import gTTS
import pyglet
import os
import time
import uuid
import threading

# File reading functions
def read_pdf(file_path):
    """Read text from a PDF file."""
    try:
        with open(file_path, 'rb') as file:
            return "".join(page.extract_text() for page in PyPDF2.PdfReader(file).pages)
    except Exception as e:
        update_status(f"Error reading PDF: {e}", "red")
        return ""

def read_docx(file_path):
    """Read text from a DOCX file."""
    try:
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception as e:
        update_status(f"Error reading DOCX: {e}", "red")
        return ""

# Global variables for audio control
player = None
playing = False

def play_audio(text, lang, filename):
    """Play audio from text using gTTS and pyglet."""
    global player, playing
    try:
        # Safely update status in the main thread
        root.after(0, lambda: update_status("Processing audio...", "orange"))
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        sound = pyglet.media.load(filename)
        player = sound.play()
        playing = True
        audio_duration = sound.duration or 5
        timeout = max(audio_duration + 2, 5)
        start_time = time.time()
        while player.playing and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        player.delete()
        playing = False
    except Exception as e:
        root.after(0, lambda err=e: update_status(f"Error playing audio: {err}", "red"))
    finally:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        playing = False
        root.after(0, lambda: update_status("Ready", "green"))

# GUI Functions
def load_pdf():
    """Load a PDF file into the text widget."""
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        text = read_pdf(file_path)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, text)

def load_docx():
    """Load a DOCX file into the text widget."""
    file_path = filedialog.askopenfilename(filetypes=[("DOCX files", "*.docx")])
    if file_path:
        text = read_docx(file_path)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, text)

def start_tts():
    """Start text-to-speech playback."""
    global player, playing
    if playing:
        update_status("Audio is already playing. Stop it first.", "orange")
        return
    text = text_widget.get(1.0, tk.END).strip()
    if not text:
        update_status("No text to process.", "orange")
        return
    selected_lang = lang_var.get()
    lang = languages[selected_lang]
    filename = f"tts_{uuid.uuid4().hex}.mp3"
    threading.Thread(target=play_audio, args=(text, lang, filename), daemon=True).start()

def stop_tts():
    """Stop the current audio playback."""
    global player, playing
    if player and player.playing:
        player.pause()
        player.delete()
        playing = False
        update_status("Audio stopped", "green")

def clear_text():
    """Clear the text widget."""
    text_widget.delete(1.0, tk.END)
    update_status("Text cleared", "green")

def show_language_menu():
    """Show the language selection dropdown menu."""
    lang_menu = tk.Menu(root, tearoff=0)
    for lang in languages.keys():
        lang_menu.add_radiobutton(label=lang, variable=lang_var, value=lang)
    lang_menu.post(lang_button.winfo_rootx(), lang_button.winfo_rooty() + lang_button.winfo_height())

def update_status(message, color):
    """Update the status label with a message and color."""
    status_label.config(text=message, fg=color)

# Create the main window
root = tk.Tk()
root.title("Text Pronouncer")

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window dimensions
window_width = 900
window_height = 600

# Calculate position to center the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Lock window size to prevent resizing
root.resizable(False, False)

# Set background color
root.configure(bg="#f0f0f0")

# Text widget with scrollbar
text_frame = tk.Frame(root, bg="#f0f0f0")
text_frame.pack(expand=True, fill='both', padx=10, pady=10)
text_widget = tk.Text(text_frame, wrap=tk.WORD, height=15, bg="white", font=("Khmer OS", 10))
text_widget.pack(side="left", expand=True, fill='both')
scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
scrollbar.pack(side="right", fill="y")
text_widget.config(yscrollcommand=scrollbar.set)

# Control frame for buttons
control_frame = tk.Frame(root, bg="#f0f0f0")
control_frame.pack(fill='x', padx=10, pady=5)

# Language selection with dropdown symbol
languages = {
    "Khmer": "km",
    "Chinese": "zh-CN",
    "English": "en",
    "Thai": "th",
    "Vietnamese": "vi",
    "Korean": "ko",
}
lang_var = tk.StringVar(value="Khmer")
lang_button = tk.Button(control_frame, text="Select Language ▼", command=show_language_menu,
                        bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                        padx=15, pady=8, width=12)
lang_button.pack(side="left", padx=5)

# Load buttons with symbols
load_pdf_btn = tk.Button(control_frame, text="Load PDF", command=load_pdf,
                         bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                         padx=15, pady=8, width=12)
load_pdf_btn.pack(side="left", padx=5)
load_docx_btn = tk.Button(control_frame, text="Load DOCX", command=load_docx,
                          bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                          padx=15, pady=8, width=12)
load_docx_btn.pack(side="left", padx=5)

# Playback buttons with symbols
speak_btn = tk.Button(control_frame, text="Speak", command=start_tts,
                      bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                      padx=15, pady=8, width=12)
speak_btn.pack(side="left", padx=5)
stop_btn = tk.Button(control_frame, text="Stop", command=stop_tts,
                     bg="#F44336", fg="white", font=("Arial", 10, "bold"),
                     padx=15, pady=8, width=12)
stop_btn.pack(side="left", padx=5)

# Clear button with symbol
clear_btn = tk.Button(control_frame, text="Clear", command=clear_text,
                      bg="#9E9E9E", fg="white", font=("Arial", 10, "bold"),
                      padx=15, pady=8, width=12)
clear_btn.pack(side="left", padx=5)

# Status frame with fixed height
status_frame = tk.Frame(root, bg="#f0f0f0", height=20)
status_frame.pack(fill='x', padx=10, pady=5)
status_frame.pack_propagate(False)  # Lock frame size

# Status label inside the frame
status_label = tk.Label(status_frame, text="Ready", fg="green", anchor='w', bg="#f0f0f0", font=("Arial", 10))
status_label.pack(fill='x')

# Start the main event loop
root.mainloop()
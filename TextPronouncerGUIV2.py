import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
from docx import Document
from gtts import gTTS
import pyglet
import os
import uuid
import threading

# Global variables for audio control
player = None
playing = False
current_filename = None

# File reading functions
def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            return "".join(page.extract_text() for page in PyPDF2.PdfReader(file).pages)
    except Exception as e:
        update_status(f"Error reading PDF: {e}", "red")
        return ""

def read_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception as e:
        update_status(f"Error reading DOCX: {e}", "red")
        return ""

# Audio playback function
def play_audio(text, lang, filename):
    global player, playing, current_filename
    try:
        root.after(0, lambda: update_status("Generating audio...", "orange"))
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        sound = pyglet.media.load(filename)
        player = sound.play()
        current_filename = filename
        def on_eos():
            global player, playing, current_filename
            player = None
            playing = False
            if current_filename and os.path.exists(current_filename):
                os.remove(current_filename)
            current_filename = None
            root.after(0, lambda: update_status("Ready", "green"))
        player.on_eos = on_eos
        playing = True
        root.after(0, lambda: update_status("Playing", "green"))
    except Exception as e:
        root.after(0, lambda err=e: update_status(f"Error playing audio: {err}", "red"))
        playing = False

# GUI Functions
def load_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        text = read_pdf(file_path)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, text)

def load_docx():
    file_path = filedialog.askopenfilename(filetypes=[("DOCX files", "*.docx")])
    if file_path:
        text = read_docx(file_path)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, text)

def start_tts():
    global player, playing, current_filename
    if player:  # Stop any existing playback
        player.pause()
        player.delete()
        player = None
        if current_filename and os.path.exists(current_filename):
            os.remove(current_filename)
        current_filename = None
    playing = False
    text = text_widget.get(1.0, tk.END).strip()
    if not text:
        update_status("No text to process.", "orange")
        return
    selected_lang = lang_var.get()
    lang = languages[selected_lang]
    filename = f"tts_{uuid.uuid4().hex}.mp3"
    threading.Thread(target=play_audio, args=(text, lang, filename), daemon=True).start()

def pause_tts():
    global player, playing
    if player and playing:
        player.pause()
        playing = False
        update_status("Paused", "orange")

def resume_tts():
    global player, playing
    if player and not playing:
        player.play()
        playing = True
        update_status("Playing", "green")

def stop_tts():
    global player, playing, current_filename
    if player:
        player.pause()  # Pause first to stop playback
        player.delete()
        player = None
        playing = False
        if current_filename and os.path.exists(current_filename):
            os.remove(current_filename)
            current_filename = None
        update_status("Stopped", "red")

def clear_text():
    text_widget.delete(1.0, tk.END)
    update_status("Text cleared", "green")

def show_language_menu():
    lang_menu = tk.Menu(root, tearoff=0)
    for lang in languages.keys():
        lang_menu.add_radiobutton(label=lang, variable=lang_var, value=lang)
    lang_menu.post(lang_button.winfo_rootx(), lang_button.winfo_rooty() + lang_button.winfo_height())

def update_status(message, color):
    status_label.config(text=message, fg=color)

# Create the main window
root = tk.Tk()
root.title("Text Pronouncer")

# Center the window with initial size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 900
window_height = 600
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.minsize(600, 400)  # Minimum size for responsiveness
root.configure(bg="#f0f0f0")

# Use grid for fully responsive layout
root.grid_rowconfigure(0, weight=1)  # Text area expands vertically
root.grid_rowconfigure(1, weight=0)  # Buttons stay fixed height
root.grid_rowconfigure(2, weight=0)  # Status bar stays fixed height
root.grid_columnconfigure(0, weight=1)  # Everything expands horizontally

# Text widget with scrollbar
text_frame = tk.Frame(root, bg="#f0f0f0")
text_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_columnconfigure(0, weight=1)
text_frame.grid_columnconfigure(1, weight=0)
text_widget = tk.Text(text_frame, wrap="word", bg="white", font=("Khmer OS", 12))
text_widget.grid(row=0, column=0, sticky="nsew")
scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
text_widget.config(yscrollcommand=scrollbar.set)

# Control frame for buttons
control_frame = tk.Frame(root, bg="#f0f0f0")
control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
control_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)  # Equal width for buttons

# Language selection
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
                        bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=15, pady=8)
lang_button.grid(row=0, column=0, sticky="ew", padx=2)

# Load buttons
load_pdf_btn = tk.Button(control_frame, text="Load PDF", command=load_pdf,
                         bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=15, pady=8)
load_pdf_btn.grid(row=0, column=1, sticky="ew", padx=2)
load_docx_btn = tk.Button(control_frame, text="Load DOCX", command=load_docx,
                          bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=15, pady=8)
load_docx_btn.grid(row=0, column=2, sticky="ew", padx=2)

# Playback buttons
speak_btn = tk.Button(control_frame, text="Speak", command=start_tts,
                      bg="#4527a0", fg="white", font=("Arial", 10, "bold"), padx=15, pady=8)
speak_btn.grid(row=0, column=3, sticky="ew", padx=2)
pause_btn = tk.Button(control_frame, text="Pause", command=pause_tts,
                      bg="#ffa000", fg="white", font=("Arial", 10, "bold"), padx=15, pady=8)
pause_btn.grid(row=0, column=4, sticky="ew", padx=2)
resume_btn = tk.Button(control_frame, text="Resume", command=resume_tts,
                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=15, pady=8)
resume_btn.grid(row=0, column=5, sticky="ew", padx=2)
stop_btn = tk.Button(control_frame, text="Stop", command=stop_tts,
                     bg="#F44336", fg="white", font=("Arial", 10, "bold"), padx=15, pady=8)
stop_btn.grid(row=0, column=6, sticky="ew", padx=2)

# Clear button
clear_btn = tk.Button(control_frame, text="Clear", command=clear_text,
                      bg="#607D8B", fg="white", font=("Arial", 10, "bold"), padx=15, pady=8)
clear_btn.grid(row=0, column=7, sticky="ew", padx=2)

# Status frame
status_frame = tk.Frame(root, bg="#f0f0f0")
status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
status_frame.grid_columnconfigure(0, weight=1)
status_label = tk.Label(status_frame, text="Ready", fg="green", anchor='w', bg="#f0f0f0", font=("Arial", 10))
status_label.grid(row=0, column=0, sticky="ew")

# Start the main event loop
root.mainloop()
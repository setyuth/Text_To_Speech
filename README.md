I. Text Pronouncer User Manual
Welcome to Text Pronouncer, a simple application that converts text from PDFs, DOCX files, or manual input into spoken audio in multiple languages. 
This manual will guide you through setting up, running, and using the application step by step.

1. System Requirements
Before you begin, ensure your system meets these requirements:
- Operating System: Windows, macOS, or Linux.
- Python: Version 3.6 or higher installed.
- Internet Connection: Required for initial setup (to download libraries) and text-to-speech conversion.
- Speakers/Headphones: Needed to hear the audio output.

2. Setup Instructions
Follow these steps to set up the application on your computer.

Step 1: Install Python: 
1. Check if Python is installed:
- Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux).
- Type python --version or python3 --version and press Enter.
- If you see a version number (e.g., "Python 3.8.5"), Python is installed. Skip to Step 2.

2. If not installed:
- Download Python from python.org.
- Run the installer, ensuring you check "Add Python to PATH" during installation.
- Verify installation by typing python --version again in the terminal.

Step 2: Install Required Libraries
The application needs several Python libraries. Install them using pip, Python’s package manager.
1. Open a terminal.
2. Run the following commands one by one:
   pip install PyPDF2
   pip install python-docx
   pip install gtts
   pip install pyglet

- PyPDF2: Reads PDF files.
- python-docx: Reads DOCX files.
- gtts: Converts text to speech (Google Text-to-Speech).
- pyglet: Plays audio files.
3. Wait for each command to complete. You’ll see download and installation messages.

Step 3: Download the Application Code
1. Copy the provided Python code (from the latest version) into a text editor (e.g., Notepad, VS Code, or IDLE).
2. Save the file with a .py extension, e.g., text_pronouncer.py, in a folder of your choice
  (e.g., C:\TextPronouncer on Windows or ~/Documents/TextPronouncer on macOS/Linux).

II. Running the Application
Once set up, running the application is straightforward.

Step 1: Open the Terminal
- Windows: Press Win + R, type cmd, and press Enter.
- macOS/Linux: Open Terminal from your applications menu.

Step 2: Navigate to the Folder
1. Use the cd command to go to the folder where you saved text_pronouncer.py.
- Example (Windows): cd C:\TextPronouncer
- Example (macOS/Linux): cd ~/Documents/TextPronouncer
2. Press Enter.

Step 3: Run the Program
1. Type the following command and press Enter: python text_pronouncer.py
- On some systems, you might need python3 text_pronouncer.py.
2. The application window titled "Text Pronouncer" will open, centered on your screen.

III. How to Use the Application
Here’s how to use the features of Text Pronouncer.

Step 1: Open the Application
- Follow the "Running the Application" steps above. You’ll see a window with:
  - A large text box (for text input/output).
  - Buttons: "Select Language ▼", "📄 Load PDF", "📝 Load DOCX", "🔊 Speak", "⏸ Pause", "⏯ Resume", "⏹ Stop", "🗑 Clear".
  - A status bar at the bottom (initially says "Ready" in green).

Step 2: Load Text
You can load text from files or type it manually.
- From a PDF File:
1. Click the "📄 Load PDF" button.
2. In the file dialog, navigate to a PDF file, select it, and click "Open."
3. The text from the PDF will appear in the text box.

- From a DOCX File:
1. Click the "📝 Load DOCX" button.
2. Select a DOCX file and click "Open."
3. The text will appear in the text box.

- Manual Input:
1. Click inside the text box.
2. Type or paste your text.

Step 3: Choose a Language
1. Click the "Select Language ▼" button.
2. A dropdown menu will appear with options: Khmer, Chinese, English, Thai, Vietnamese, Korean.
3. Click your desired language (e.g., "English").
  - The default is "Khmer."

Step 4: Play the Audio
1. Ensure you have text in the text box and a language selected.
2. Click the "🔊 Speak" button.
3. The status bar will show "Generating audio..." (orange), then "Playing" (green) as the audio plays through your speakers/headphones.
  - If there’s no text, it’ll say "No text to process" (orange).

Step 5: Control Playback
- Pause:
  1. While audio is playing, click "⏸ Pause."
  2. The audio will pause, and the status will change to "Paused" (orange).

- Resume:
  1. After pausing, click "⏯ Resume."
  2. The audio will continue from where it paused, and the status will return to "Playing" (green).

- Stop:
  1. Click "⏹ Stop" at any time.
  2. The audio will stop completely, and the status will show "Stopped" (red).
    - You can start again with "Speak," but "Resume" won’t work after "Stop."

Step 6: Clear the Text
1. Click the "🗑 Clear" button.
2. The text box will empty, and the status will show "Text cleared" (green).

Step 7: Resize the Window (Optional)
- Drag the window edges or corners to resize it.
- The text box will expand or shrink, buttons will stretch horizontally, and the status bar will adjust to fit the new size.

Step 8: Close the Application
- Click the window’s close button (X) in the top-right corner (Windows) or top-left (macOS).

IV. Troubleshooting
- No Sound:
  - Check your speakers/headphones are connected and turned on.
  - Ensure your internet is working (needed for gTTS).

- Error Messages:
  - If the status shows "Error playing audio..." (red), check your internet or file permissions.
  - For "Error reading PDF/DOCX," ensure the file isn’t corrupted or locked.

- Program Won’t Start:
  - Verify Python and all libraries are installed (re-run pip install commands).
  - Check the terminal for error messages and ensure you’re in the correct folder.

- Font Issues:
  - The text box uses "Khmer OS" at 12pt. If it looks odd, your system might not have this font; it’ll fall back to a default font.

V. Enjoy Using Text Pronouncer!
With this application, you can easily convert text to speech in multiple languages. If you encounter issues or need help, refer to the troubleshooting section or contact support (if provided by your source).

Happy pronouncing! 🎙️

import webbrowser
import os
import pyautogui
import datetime
from urllib.parse import quote

def search_youtube(query):
    """Search YouTube for a query."""
    if not query:
        return "No search term provided"
    search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
    webbrowser.open(search_url)
    return f"Searching YouTube for {query}"

def run_automation(command):

    # 🌐 Websites
    if "youtube" in command:
        webbrowser.open("https://youtube.com")
        return "YOUTUBE_OPENED"  # Special signal for main.py

    if "google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"

    if "chatgpt" in command or "talk to llama" in command or "ask llama" in command:
        return "TALK_TO_LLAMA"  # Special signal for main.py

    # 💻 Apps
    if "notepad" in command:
        os.system("notepad")
        return "Opening Notepad"

    if "calculator" in command:
        os.system("calc")
        return "Opening Calculator"

    # ⏰ Time
    if "time" in command:
        return datetime.datetime.now().strftime("%H:%M:%S")

    # 🎵 Media control (basic)
    if "play music" in command:
        pyautogui.press("playpause")
        return "Playing music"

    # 🖥 System control
    if "close tab" in command:
        pyautogui.hotkey("ctrl", "w")
        return "Closing tab"

    if "switch tab" in command:
        pyautogui.hotkey("ctrl", "tab")
        return "Switching tab"

    return None
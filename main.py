from modules.listen import listen
from modules.speak import speak
from modules.brain import ask_ai
from modules.automation import run_automation, search_youtube

def wait_for_yes():
    """Keep asking until user says yes."""
    while True:
        speak("Do you want to continue?")
        response = listen()
        
        if "yes" in response or "yeah" in response or "yep" in response or "continue" in response:
            return True
        elif response:
            speak("Please say yes or no")

speak("Jarvis online")

while True:
    command = listen()

    if not command:
        continue

    # ⚙️ Try automation first
    result = run_automation(command)

    if result == "YOUTUBE_OPENED":
        speak("Opening YouTube")
        speak("What do you want to search?")
        search_query = listen()
        
        if search_query:
            search_result = search_youtube(search_query)
            speak(search_result)
        else:
            speak("No search query provided")
    elif result == "TALK_TO_LLAMA":
        speak("I am listening. Ask me anything. Say done to exit")
        
        # Continuous Llama conversation loop
        while True:
            print("\n[Listening for question...]")
            question = listen()
            
            if not question:
                speak("I did not hear that. Please ask again")
                continue
            
            print(f"[Question: {question}]")
            
            # Check for exit commands
            if "exit" in question or "quit" in question or "stop" in question or "done" in question or "bye" in question:
                speak("Exiting Llama conversation. Goodbye")
                break
            
            # Ask Llama and reply in voice
            print("[Processing with Llama...]")
            ai_response = ask_ai(question)
            if ai_response:
                print(f"[Response: {ai_response}]")
                speak(ai_response)
            else:
                speak("I could not generate a response. Try again")
            
            print("[Waiting for next question...]")
    elif result:
        speak(result)
    else:
        # 🧠 fallback to AI
        response = ask_ai(command)
        speak(response)

    # ❓ Wait for yes to continue
    wait_for_yes()
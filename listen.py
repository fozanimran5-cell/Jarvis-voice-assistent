import queue

import numpy as np
import sounddevice as sd
import speech_recognition as sr

recognizer = sr.Recognizer()
MAX_RECORD_SECONDS = 5
SILENCE_THRESHOLD = 600
SILENCE_DURATION = 1.0
CHUNK_DURATION = 0.1


def listen():
    """Listen for a single command and stop early when silence is detected."""
    try:
        print("Listening for a command... (speak now)")
        sample_rate = 16000
        channel_count = 1
        audio_queue = queue.Queue()

        def callback(indata, frames, time_info, status):
            if status:
                print(f"Audio input status: {status}")
            audio_queue.put(indata.copy())

        with sd.InputStream(samplerate=sample_rate, channels=channel_count, dtype='int16', callback=callback, blocksize=int(CHUNK_DURATION * sample_rate)):
            silent_chunks = 0
            max_chunks = int(MAX_RECORD_SECONDS / CHUNK_DURATION)
            recorded_chunks = []
            started_speaking = False

            for i in range(max_chunks):
                try:
                    chunk = audio_queue.get(timeout=CHUNK_DURATION + 0.2)
                except queue.Empty:
                    continue

                recorded_chunks.append(chunk)
                volume = np.abs(chunk).mean()

                if volume > SILENCE_THRESHOLD:
                    started_speaking = True
                    silent_chunks = 0
                elif started_speaking:
                    silent_chunks += 1

                if started_speaking and silent_chunks * CHUNK_DURATION >= SILENCE_DURATION and len(recorded_chunks) > 5:
                    print("Stopped listening.")
                    break

        if not recorded_chunks:
            print("No audio detected")
            return ""

        audio_data = np.concatenate(recorded_chunks, axis=0)
        audio_bytes = audio_data.tobytes()
        audio = sr.AudioData(audio_bytes, sample_rate, 2)

        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Error with speech recognition: {e}")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""
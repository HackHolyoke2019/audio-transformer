#!/usr/bin/env python3
import sys
import wave
import numpy as np
import uuid

target_snippet_size = 14
n_frames = 1
channels = 1
sample_rate = 180000
sample_width = 2 # 16 bits
read_size = n_frames * channels * sample_width * sample_rate # Read 1 second at a time

def open_wav_f():
    name = 'snippets/' + str(uuid.uuid4()) + '.wav'

    wavf = wave.open(name, 'wb')
    wavf.setnchannels(channels)
    wavf.setsampwidth(sample_width)
    wavf.setframerate(sample_rate)
    return wavf, name

with open('/dev/stdin', 'rb') as stdin:
    snippet_size = 0
    current_snippet, snippet_name = open_wav_f()
    print("new snippet", snippet_name)
    
    while True:
        frame = stdin.read(read_size)

        # Finish when audio is done
        if not frame:
            break

        volume = np.average(np.absolute(np.fromstring(frame, np.int16)))

        if volume < 1000 or snippet_size >= target_snippet_size:
            current_snippet.close()
            current_snippet, snippet_name = open_wav_f()
            snippet_size = 0
            print("new snippet", snippet_name)
        else:
            current_snippet.writeframes(frame)
            snippet_size += 1
            
"""
        if volume > 0: # Add frames with sound to snippet
            print(volume, "+", snippet_name)
            current_snippet.writeframes(frame)
        else: # If no sound end current snippet and make a new one
            print(volume, "new snippet")
            current_snippet.close()
            current_snippet = open_wav_f()
"""

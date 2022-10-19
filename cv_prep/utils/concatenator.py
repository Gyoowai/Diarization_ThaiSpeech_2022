import numpy as np
import os
from .preprocessor import *

"""
1. read audio file as an array
2. concatenate array iteratively 
3. until satisfing the required duration
"""
def concatenator(client_id, speaker_id, paths, outputName, refill_callback, metadata, age_gender_keys):
    outputPath = f"cv_wav/{outputName}.wav"

    # init variables
    wanted_duration = 1200
    duration = 0
    arr=[]
    rttm = ""
    row=""
    last_speaker = -1

    while duration < wanted_duration:
        speaker_index = np.random.choice(4)
        speaker_change = (last_speaker != speaker_index)

        audio_path = paths[client_id[speaker_index]].pop(0)
        audio_name = audio_path.split("/")[-1].split(".")[0]
        wav_path="wav_pool/"+audio_name+".wav"
        wav, turn_duration = preprocessor(
            inputFile = audio_path,
            outputFile= wav_path,
            target_dBFS = -20,
            silence_threshold=-40,
        ) 
        arr.append(wav)

        # write rttm
        if speaker_change: # add rttm row
            rttm+=row
            row = f"SPEAKER {outputName} 1 {duration} {turn_duration} <NA> <NA> {speaker_id[speaker_index]} <NA> <NA>\n"
            startTime = duration
            cumulativeDuration = turn_duration
        else: # update rttm row
            cumulativeDuration += turn_duration
            row = f"SPEAKER {outputName} 1 {startTime} {cumulativeDuration} <NA> <NA> {speaker_id[speaker_index]} <NA> <NA>\n"
            
        duration += turn_duration
        last_speaker = speaker_index

        # fill used up path
        if(len(paths[client_id[speaker_index]])==0):
            refill_callback(id = client_id[speaker_index])

        # Metadata
        metadata.append([
            outputName, 
            client_id[speaker_index], 
            age_gender_keys[speaker_index][0],
            age_gender_keys[speaker_index][1],
            audio_name,
            turn_duration
        ])
        
    sum(arr).export(outputPath, format="wav")
    return rttm + row, wanted_duration, metadata
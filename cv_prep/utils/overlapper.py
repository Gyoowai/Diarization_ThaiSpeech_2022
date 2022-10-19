import numpy as np
from .preprocessor import *
from .downmixer import *

"""
1 batch = Overlapped 1-min wav/nparray
Concat all batches in overlapper
"""
def overlap_batch(client_id, speaker_id, paths, outputName, onset, wanted_duration, refill_callback, metadata, age_gender_keys):
    outputPath = f"cv_wav/{outputName}.wav"
    
    # init wav file
    speaker_index = np.random.choice(4)
    audio_path = paths[client_id[speaker_index]].pop(0)
    audio_name = audio_path.split("/")[-1].split(".")[0]
    wav, batchDuration = preprocessor(
        inputFile=audio_path,
        outputFile=outputPath,
        target_dBFS=-20,
        silence_threshold=-40,
    )
    row = f"SPEAKER {outputName} 1 {onset} {batchDuration} <NA> <NA> {speaker_id[speaker_index]} <NA> <NA>\n"
    onBuffer = False
    startTime = 0
    delayTime = batchDuration
    cumulativeDuration = batchDuration
    last_speaker = speaker_index
    rttm = ""

    # fill empty path
    if(len(paths[client_id[speaker_index]]) == 0):
        refill_callback(client_id[speaker_index])

    # Metadata
    metadata.append([
        outputName,
        client_id[speaker_index],
        age_gender_keys[speaker_index][0],
        age_gender_keys[speaker_index][1],
        audio_name,
        batchDuration
    ])

    while (batchDuration < wanted_duration) or onBuffer:
        speaker_index = np.random.choice(3)
        speaker_change = (last_speaker != speaker_index)

        audio_path = paths[client_id[speaker_index]].pop(0)
        audio_name = audio_path.split("/")[-1].split(".")[0]
        wav_path = "wav_pool/"+audio_name+".wav"
        wav, turn_duration = preprocessor(
            inputFile=audio_path,
            outputFile=wav_path,
            target_dBFS=-20,
            silence_threshold=-40,
        )

        # prevent same speaker overlap himself
        if (not speaker_change) or (batchDuration < 1.5) or (turn_duration <= 3):
            delayTime = batchDuration
        else:
            delayTime = batchDuration - 1.5

        downmixer(
            inputFile=wav_path,
            targetFile=outputPath,
            onBuffer=onBuffer,
            delayTime=delayTime*1000,  # millisec
        )

        # write rttm
        if speaker_change:  # add rttm row
            rttm += row
            row = f"SPEAKER {outputName} 1 {onset+delayTime} {turn_duration} <NA> <NA> {speaker_id[speaker_index]} <NA> <NA>\n"
            startTime = delayTime
            cumulativeDuration = turn_duration
        else:  # update rttm row
            cumulativeDuration += turn_duration
            row = f"SPEAKER {outputName} 1 {onset+startTime} {cumulativeDuration} <NA> <NA> {speaker_id[speaker_index]} <NA> <NA>\n"
            
        batchDuration = delayTime + turn_duration
        onBuffer = not onBuffer
        last_speaker = speaker_index

        # fill empty path
        if(len(paths[client_id[speaker_index]])==0):
            refill_callback(client_id[speaker_index])

        # Metadata
        metadata.append([
            outputName,
            client_id[speaker_index],
            age_gender_keys[speaker_index][0],
            age_gender_keys[speaker_index][1],
            audio_name,
            turn_duration
        ])

    return rttm+row, batchDuration, metadata

"""
read audio file as an array and concatenate array iteratively until satisfing the required duration
"""
def overlapper(client_id, speaker_id, paths, outputName, refill_callback, metadata, age_gender_keys):
    outputPath = f"cv_wav/{outputName}.wav"

    # init variables
    wanted_duration = 1200
    rttm = ""
    duration = 0
    arr=[]

    while duration < wanted_duration:
        rttm_batch, batchDuration, metadata = overlap_batch(
            client_id=client_id,
            speaker_id = speaker_id,
            paths = paths,
            outputName = outputName, 
            onset = duration, 
            wanted_duration = 60, 
            refill_callback = refill_callback, 
            metadata = metadata, 
            age_gender_keys = age_gender_keys
        )
        wav = AudioSegment.from_wav(outputPath) # 
        arr.append(wav)
        
        rttm += rttm_batch
        duration += batchDuration
    
    sum(arr).export(outputPath, format="wav")
    
    return rttm, wanted_duration, metadata
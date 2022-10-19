from .audioProcessor import *

# preprocess each audio with volume normalization, silence trimming, and pitch shifting
# return Audiosegment and Duration of audio after process 
def preprocessor(
    inputFile,
    outputFile,
    target_dBFS = -20,
    silence_threshold = -40.0,
    octaves = 0,
):
    if inputFile.endswith(".mp3"): 
        sound = AudioSegment.from_mp3(inputFile)
    elif inputFile.endswith(".wav"): 
        sound = AudioSegment.from_wav(inputFile)

    sound = set_loudness(sound, target_dBFS)
    sound = trim_silence(sound, silence_threshold)
    sound = shift_pitch(sound,octaves) # For Augmentation
    
    sound.export(outputFile, format="wav")
    return sound, len(sound)/1000 # return AudioSegment and Duration(s)
from pydub import AudioSegment
from pydub.utils import make_chunks
from pydub.playback import play

def detect_leading_silence(sound, silence_threshold, chunk_size=200):
    trim_ms = 0 # ms
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size
    return trim_ms

def trim_silence(sound, silence_threshold):
    start_trim = detect_leading_silence(sound,silence_threshold,)
    end_trim = detect_leading_silence(sound.reverse(),silence_threshold)   
    return sound[start_trim: len(sound)-end_trim]

def get_loudness(sound, slice_size=200):
    return max(chunk.dBFS for chunk in make_chunks(sound, slice_size))

def set_loudness(sound, target_dBFS):
    loudness_difference = target_dBFS - get_loudness(sound)
    return sound.apply_gain(loudness_difference)

def shift_pitch(sound, octaves):
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    pitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    pitch_sound = pitch_sound.set_frame_rate(sound.frame_rate)
    return pitch_sound

def playwav(wavfile):
    wav = AudioSegment.from_wav(wavfile)
    play(wav)

def playmp3(mp3file):
    mp3 = AudioSegment.from_mp3(mp3file)
    play(mp3)
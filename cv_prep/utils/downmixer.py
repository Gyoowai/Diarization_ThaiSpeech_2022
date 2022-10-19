from pydub import AudioSegment
import subprocess

# Volume normalization after downmixing 
# TODO: find formula for gain factor
def volumeNormalization(file, factor = -0.24):
    sound = AudioSegment.from_file(file, "wav")
    change_in_dBFS = factor*sound.dBFS
    sound.apply_gain(change_in_dBFS).export(file, format="wav")

# Downmix 2 audios (overlapping by delay time) using ffmpeg
# https://superuser.com/questions/1509582/ffmpeg-merge-two-audio-file-with-defined-overlapping-time
def downmixer(
    inputFile,
    targetFile,
    onBuffer,
    delayTime,
):
    if onBuffer:
        cmd = f'ffmpeg -y -i cv_wav/buffer.wav -i {inputFile} -filter_complex "[1]adelay={delayTime}|{delayTime}[a1];[0:a][a1]amix=inputs=2[a]" -map "[a]" -ac 2 {targetFile}'
        subprocess.run(cmd)
        volumeNormalization(targetFile)
    else: # onTargetFile
        cmd = f'ffmpeg -y -i {targetFile} -i {inputFile} -filter_complex "[1]adelay={delayTime}|{delayTime}[a1];[0:a][a1]amix=inputs=2[a]" -map "[a]" -ac 2 cv_wav/buffer.wav'
        subprocess.run(cmd)
        volumeNormalization("cv_wav/buffer.wav")
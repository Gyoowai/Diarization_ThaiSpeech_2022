# Speaker Diarization for Thai Speech

## What is Speaker Diarization?
Speaker diarization is the speech processing tasks which takes the input of speech with different speakers then identify which speaker is speaking and how long the speech occurs (The question of "who spoke when?").

The example below show the results of speaker diarization in the case of 3 speakers
```
Speaker_00 start speaking at 10.9s with total speech length of 5.2s
Speaker_02 start speaking at 17.9s with total speech length of 1.4s
Speaker_02 start speaking at 18.9s with total speech length of 2.4s
Speaker_01 start speaking at 22.3s with total speech length of 10.7s
```

## Methods
### Experiment Setting
The model is based on research and code from [pyannote](https://pyannote.github.io/). The progress that did the best at improving model's performance was to fine-tune the pretrained model with Thai diarization dataset which I synthesize from public speech dataset along with the scraped data. Also, the hyperparameter tuning were performed.

## Results
Improve the Diarization error rate by 4x compared to the pretrained model of pyannote (From ~20% to ~5%)
  
### Example
This visualization represents each speakers in different colors and the line as length of their speech.

The test data are from Parliament meeting: [Youtube link](https://www.youtube.com/watch?v=xQKT66VMZeQ&t=4539s)

Ground truth:
![groundtruth_demo_result](https://github.com/Gyoowai/2022_Diarization_forThai/blob/master/pictures/groundtruth_demo_result.png)

Pretrain Result (DER = 19.19):
![pretrain_demo_result](https://github.com/Gyoowai/2022_Diarization_forThai/blob/master/pictures/pretrain_demo_result.png)

My Result (DER = 3.9):
![demo_result](https://github.com/Gyoowai/2022_Diarization_forThai/blob/master/pictures/demo_result.png)

## What does output look like?
rttm files format
```
SPEAKER {file_name} 1 {start_time} {duration} <NA> <NA> {speaker_name} <NA> <NA>
```
example:

SPEAKER ES2011a 1 58.56 5.72 <NA> <NA> FEE041 <NA> <NA>

SPEAKER ES2011a 1 65.0 12.78 <NA> <NA> FEE044 <NA> <NA>

## Datasets
### AMI Corpus
Downloads: https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/

Description: https://groups.inf.ed.ac.uk/ami/corpus/

Metadata: http://shachi.org/resources/5073
### Common Voice
Version: cv-corpus-9.0-2022-04-27

Downloads: https://commonvoice.mozilla.org/th/datasets

Description: https://www.kaggle.com/datasets/mozillaorg/common-voice
### Clips from Parliament Meeting
Scraping from youtube clips

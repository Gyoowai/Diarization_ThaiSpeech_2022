﻿# Speaker Diarization for Thai Speech

## What is Speaker Diarization?
Speaker diarization คือ กระบวนการประมวลผลข้อมูลเสียงที่มีผู้พูดหลายคน เพื่อแยกแยะว่าในข้อมูลเสียงนั้นมีผู้พูดกี่คน และแต่ละคนได้พูดในช่วงเวลาไหน เป็นระยะเวลาเท่าใด
ตัวอย่าง	ผลลัพธ์ที่ได้จากกระบวนการ speaker diarization ในกรณีที่มีผู้พูดจำนวน 3 คน

```
Speaker_00 เริ่มพูด ณ เวลา 10.9s ใช้เวลาพูดรวม 5.2s
Speaker_02 เริ่มพูด ณ เวลา 17.9s ใช้เวลาพูดรวม 1.4s
Speaker_02 เริ่มพูด ณ เวลา 18.9s ใช้เวลาพูดรวม 2.4s
Speaker_01 เริ่มพูด ณ เวลา 22.3s ใช้เวลาพูดรวม 10.7s
```

## Methods
### Experiment Setting
นำโมเดลจาก [pyannote](https://pyannote.github.io/) มาทำการ Fine-tuning หรือเทรนเพิ่มเติมด้วย Dataset ของข้อมูลการประชุมที่ได้เตรียมไว้เพื่อเพิ่มขอบเขตความรู้ของโมเดลให้รู้จักข้อมูลที่มีลักษณะเป็นการประชุมและข้อมูลภาษาไทย จากนั้นนำโมเดลที่ได้มาปรับปรุงค่า Hyperparameters เพื่อให้เหมาะสมกับลักษณะของอินพุตที่กำหนดไว้

## Results
Improve the Diarization error rate by 4x compared to the pretrained model of pyannote (From ~20% to ~5%)
  
### Example
This visualization represents each speakers in different colors and the line as length of their speech.

The test data are from Parliament meeting: [Youtube link](https://www.youtube.com/watch?v=xQKT66VMZeQ&t=4539s)

Ground truth:

Pretrain Result (DER = 19.19):
  
My Result (DER = 3.9):

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
  

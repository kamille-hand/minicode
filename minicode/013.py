import soundfile as sf
import os

os.chdir("G:/tmp_nova7/lab-26p-test-concate")

sumt = 0

for filename in os.listdir():
    sumt += sf.info(filename).duration

print(sumt / 60)

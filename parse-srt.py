import srt
import sys
import os
import subprocess
import datetime

if len(sys.argv) < 4:
    print('args not enough')
    print(r'usage: python .\parse-srt.py srtFile keyword offset(s,optional)')
    exit()

fileVideo = sys.argv[1]
fileSrt = sys.argv[2]
keyword = sys.argv[3]
offset = int(sys.argv[4]) if len(sys.argv) >= 5 else 0

outputDir = './cuts'

if not os.path.exists(outputDir):
    os.mkdir(outputDir)

file = open(fileSrt, 'r')  # 创建的这个文件，也是一个可迭代对象
srtContent = None
try:
    srtContent = file.read()  # 结果为str类型
finally:
    file.close()
if srtContent is None:
    print('read srt file err')
subtitle_generator = srt.parse(srtContent)
subtitles = list(subtitle_generator)

filteredSubtitles = list(x for x in subtitles if keyword in x.content)

print('keyword: %s' % keyword)
print('offset: %s' % offset)
print('results: %d' % len(filteredSubtitles))
for idx, x in enumerate(filteredSubtitles):
    print('%d. %s~%s: %s' % (idx + 1, x.start, x.end, x.content))
    outputFileName = '%s/%s_%s_%d.mp4' % (outputDir, fileVideo, keyword,
                                          idx + 1)
    cutmp4 = 'ffmpeg -i %s -ss %s -c copy -t %s -loglevel error -y %s' % (
        fileVideo, x.start + datetime.timedelta(seconds=offset),
        x.end - x.start, outputFileName)
    returncut = subprocess.call(cutmp4, shell=True)
print('done')
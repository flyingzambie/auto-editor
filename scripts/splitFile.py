#This file is currently unused, it will be used to implement multiprocessing. 

import os
from subprocess import call
import multiprocessing
import tempfile
from shutil import rmtree

def splitFile(videoFile, filetype, TEMP):
  # splitting
  splitDuration = 1800
  splitVideo = 'ffmpeg -i "{}" -acodec copy -f segment -segment_time {} -vcodec copy -reset_timestamps 1 -map 0 {}/%d{}'.format(
      videoFile, splitDuration, TEMP, filetype
  )
  call(splitVideo, shell=True)

def combineFile(filename, TEMP):
  # mergeing
  generateFile = "for f in ./{}/*.mp4; do echo \"file '$f'\" >> mylist.txt; done".format(
      TEMP
  )
  call(generateFile, shell=True)

  concatVideo = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "mylist.txt"]
  concatVideo.extend(["-c", "copy", filename + "_faster.mp4"])

  call(concatVideo)

  os.remove("mylist.txt")

def multiProcessVideo(videoFile):
  filename, filetype = os.path.splitext(videoFile)
  TEMP = tempfile.mkdtemp()
  splitFile(videoFile, filetype, TEMP)
  combineFile(filename, TEMP)


  rmtree(TEMP)
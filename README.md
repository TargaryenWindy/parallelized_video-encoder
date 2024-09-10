# parallelized_video-encoder
Usage:
First download the x265 binary, rename it only as 'x265' (it will work with any encoder as long as its named as x265) and put in the PATH on your system

windows download: http://www.msystem.waw.pl/x265/

Also make sure to have ffmpeg and mkvmerge on PATH

ffmpeg: https://www.ffmpeg.org/download.html

mkvmerge: https://mkvtoolnix.download/downloads.html

#running

Put it in the same folders as your video files are and double click to run, or open the terminal in the same folder and "python ./enconder.py"

#editing

Open the file and edit the encoder arguments with your own arguments

on the "parallel_encodings = 3" variable, edit it for how many instaces of the encoder with be open and encoding at the same time 




	


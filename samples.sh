# mts to mp4
ffmpeg -i source/00001.MTS -c:v copy -c:a aac -b:a 256k 00001.mp4
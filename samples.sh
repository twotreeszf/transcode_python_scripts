# split file
ffmpeg -v quiet -y -i input.ts -vcodec copy -acodec copy -ss 00:05:20 -t 00:01:32 -sn test1.mkv

ffmpeg -v quiet -y -i input.ts -vcodec copy -acodec copy -ss 00:00:00 -t 00:30:00 \
  -sn test3.mkv -vcodec copy -acodec copy -ss 00:30:00 -t 01:00:00 -sn test4.mkv
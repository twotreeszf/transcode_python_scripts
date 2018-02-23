#!/bin/bash
 
# Created by Håvard Fossli <hfossli@gmail.com> in 2013
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <http://unlicense.org/>
#
# Description
# A bash script for reversing videos using ffmpeg and sox.
#
# Keywords
# Terminal, bash, unix, mac, shell, script, video, movie, reverse, inverse, audio, video, ffmpeg, sox.
#
# Usefull links when working with ffmpeg
# - https://sites.google.com/site/linuxencoding/ffmpeg-tips
# - http://pvdm.xs4all.nl/wiki/index.php/Convert_an_AVCHD_/_MTS_file_to_MP4_using_ffmpeg
# - http://rodrigopolo.com/ffmpeg/cheats.php
# - http://www.catswhocode.com/blog/19-ffmpeg-commands-for-all-needs
#

# arg1: name of program
function assert_program_exists() {
	command -v $1 >/dev/null 2>&1 || { 
		echo >&2 "You must have $1 installed in order to run this script. Try:"; 
		echo "\$ brew install $1"
		exit 1; 
	}
}

# arg1: path to input file / source
function fallback_output_path() {
	if [[ -z "$1" ]] ; then
		echo "Bad input to get_video_duration_in_seconds_from_ffmpeg_info()"
		echo "Input givven $1"
		exit 1
	else
		__FILE_NAME=`rev <<< "$1" | cut -d"." -f2- | rev`
		__FILE_EXT=`rev <<< "$1" | cut -d"." -f1 | rev`
		__OUT_FILE_FORMAT="${__FILE_NAME}-reversed.mp4"	
		echo $__OUT_FILE_FORMAT
		exit 1
	fi	
}

function echo_variables {
	echo 
	echo "### Variables ###"
	echo 
}

function usage {
	echo "For help and detailed guide type:"
	echo "\$ $0 -h"
}

function detailed_guide {
	echo "
Example: 
\$ $0 input.file output-filename

Info:
- input file may be any kind of file reconginzed by ffmpeg

Flags: 
-i	Path to input (string)

-o	Path to output (string)

-o	Path to output (string)

-o	Path to output (string)

-o	Path to output (string)

	"
}

# Allow to be terminated with ctrl + c
trap "exit" INT

# Assert ffmpeg is installed
assert_program_exists "ffmpeg"

# Set variables and default values
typeset -i CHUNK_LEN
INPUT_PATH=''
OUTPUT_PATH=''
INCLUDE_AUDIO_STREAM=true
VERBOSE=false
PLAY_SOUND=false
HELP=false
DEINTERLACE=false
FFMPEG_IN_PARAMS=''
FFMPEG_OUT_PARAMS='-c:a aac -async 1 -c:v libx264 -profile:v high422 -preset veryslow -pix_fmt yuv420p -q:a 0 -sn -threads 8 -y'

# Grab input arguments
while getopts “i:o:dvip:q:sh” OPTION
do
     case $OPTION in
         i) INPUT_PATH=$(echo "$OPTARG" | sed 's/ /\\ /g' ) ;;
         o)	OUTPUT_PATH=$(echo "$OPTARG" | sed 's/ /\\ /g' ) ;;
         d)	DEINTERLACE=true ;;
         v)	VERBOSE=true ;;
         a)	INCLUDE_AUDIO_STREAM=false ;;
         p)	FFMPEG_IN_PARAMS="$OPTARG" ;;
         q)	FFMPEG_OUT_PARAMS="$OPTARG" ;;
         s)	PLAY_SOUND=true ;;
         h)	HELP=true ;;
         ?)	usage
			exit 1
			;;
     esac
done

if $HELP ; then
	detailed_guide
	exit 1
fi

if [[ -z $INPUT_PATH ]] ; then
	echo "Invalid source"
    usage
    exit 1
fi
 
if [ -z "$OUTPUT_PATH" ] ; then
	OUTPUT_PATH=$(fallback_output_path $INPUT_PATH)
fi


TMP_DIR=$(mktemp -dt "test")
AUDIO_PATH=${TMP_DIR}/backwards.wav
AUDIO_PARAMS=''

if $VERBOSE ; then
	echo "Created empty directory $TMP_DIR"
	ls -la $TMP_DIR
fi


if $DEINTERLACE ; then
	./ffmpeg -i $INPUT_PATH -an -qscale 1 -vf yadif $FFMPEG_IN_PARAMS ${TMP_DIR}/%06d.jpg
else
	./ffmpeg -i $INPUT_PATH -an -qscale 1 $FFMPEG_IN_PARAMS ${TMP_DIR}/%06d.jpg
fi

if $INCLUDE_AUDIO_STREAM ; then
	assert_program_exists "sox"

	./ffmpeg -i $INPUT_PATH -vn -ac 2 ${TMP_DIR}/audio.wav
	sox -V ${TMP_DIR}/audio.wav ${TMP_DIR}/audio_reverse.wav reverse
	AUDIO_PARAMS="-i ${TMP_DIR}/audio_reverse.wav"
fi

cat $(ls -r $TMP_DIR/*jpg) | ./ffmpeg -f image2pipe -vcodec mjpeg -r 25 -i - -i $TMP_DIR/audio_reverse.wav $FFMPEG_OUT_PARAMS $OUTPUT_PATH


if $VERBOSE ; then
	echo 
	echo "Will  $TMP_DIR"
	ls -la $TMP_DIR
fi

echo "Done!"

exit 1

rm -rf $TMP_DIR


if $PLAY_SOUND ; then
	# & means async
	say "Done! ." &
fi
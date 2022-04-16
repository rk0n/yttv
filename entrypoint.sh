pulseaudio -D --exit-idle-time=-1 -vvvv --log-time=1 --log-target=file:/pulseverbose.log
pacmd load-module module-native-protocol-unix
pacmd load-module module-pipe-sink file=/tmp/sink.audio sink_name=sink.audio
pacmd set-default-sink sink.audio
python -u yttv.py

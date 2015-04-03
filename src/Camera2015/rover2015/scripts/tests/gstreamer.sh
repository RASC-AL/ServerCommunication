#!/usr/bin/env sh

gst-launch-0.10 -evt souphttpsrc location='http://127.0.0.1:8080/stream?topic=/chatter' is_live=true timeout=5 ! multipartdemux ! image/jpeg, width=640, height=480, framerate=15/1 ! ffdec_mjpeg ! x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink host=128.205.54.9 port=1234 &

rostopic pub -1 /configCam std_msgs/String -- 1,0,2,3
rostopic pub -1 /config std_msgs/String -- 1,

udevadm info /dev/video0
udevadm info --query=all --name=/dev/video0
sudo lsusb -v > a.txt
sudo udevadm test `udevadm info --query=path --name=/dev/video0`

http://localhost:8080/stream?topic=/chatter

gst-launch-0.10 -evt souphttpsrc location='http://127.0.0.1:8080/stream?topic=/chatter' is_live=true timeout=5 ! multipartdemux ! image/jpeg ! ffdec_mjpeg ! x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink host=127.0.0.1 port=1234

gst-launch udpsrc port=1234 ! "application/x-rtp, payload=96" ! rtph264depay ! ffdec_h264 !  ffmpegcolorspace ! autovideosink sync=false


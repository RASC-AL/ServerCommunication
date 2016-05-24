import socket

LOCAL_IP = '127.0.0.1'
ROVER_IP = '127.0.0.1'
#HOME_IP =  socket.gethostbyname('sblinux.eng.buffalo.edu')
# HOME_IP = '127.0.0.1'
HOME_IP = '128.205.55.104'

COMM_FILE = '/tmp/ros_comm'

camList = [7,6,5,4]
#camList = [0,1,2,3]
audioList = ["alsa_input.pci-0000_00_14.2.analog-stereo"]
#audioList = ["alsa_input.usb-046d_Logitech_Webcam_C930e_57DEB4FE-02-C930e.analog-stereo", "alsa_input.usb-046d_Logitech_Webcam_C930e_C9CEA4FE-02-C930e_1.analog-stereo"]
#audioList = ["alsa_input.usb-046d_0821_2B127E90-00-U0x46d0x821_1.analog-stereo", "alsa_input.usb-046d_0821_B5713800-00-U0x46d0x821.analog-stereo", "alsa_input.usb-KYE_Systems_Corp._USB_Camera_200901010001-02-USBCamera_1.analog-stereo", "alsa_input.usb-KYE_Systems_Corp._USB_Camera_200901010001-02-USBCamera.analog-stereo"]



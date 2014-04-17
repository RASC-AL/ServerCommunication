ServerCommunication
===================

Booting Ubuntu in cmdline mode:  
    - Open `/etc/default/grub`  
    - Set `GRUB_CMDLINE_LINUX_DEFAULT="text"`  
    - In the command line type "grub-update"

Booting Ubuntu in GUI mode(X server):  
    - Open `/etc/default/grub`  
    - Set `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
    - In the command line type "grub-update"`  

Obtaining temperature information  
    - `sudo apt-get install lm-sensors`  
    - `sensors`  


Rover

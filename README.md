ServerCommunication
===================

Booting Ubuntu in cmdline mode:  
    - Open `/etc/default/grub`  
    - set `GRUB_CMDLINE_LINUX_DEFAULT="text"`  

Booting Ubuntu in GUI mode(X server):  
    - Open `/etc/default/grub`  
    - set `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"`  

Obtaining temperature information
    - `sudo apt-get install lm-sensors`  
    - `sensors`  


Rover

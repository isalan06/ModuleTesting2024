# ModuleTesting2024
This is a project for testing modules.

//---------------------------------------------------

#Real VNC

Reference#1: https://help.realvnc.com/hc/en-us/articles/360002253218-Starting-and-Stopping-VNC-Connect#operating-vnc-server-at-the-command-line-0-6
Reference#2: https://help.realvnc.com/hc/en-us/articles/360006823572-How-do-I-re-join-a-RealVNC-Server-to-the-cloud-or-change-which-team-RealVNC-Server-belongs-to

install: sudo apt install realvnc-vnc-server
uninstall: sudo apt purge realvnc-vnc-server
start service: systemctl start vncserver-x11-serviced.service
start service at every boot: systemctl enable vncserver-x11-serviced.service

logout: sudo rm /root/.vnc/config.d/vncserver-x11.d/CloudCredentials.bed

//---------------------------------------------------

#Git Hub

Reference#1: https://raspberrypi.club/285.html


//---------------------------------------------------

# drive-recorder

## Description 説明  
2011年製webカメラを車載カメラとして使用するプロジェクト  
Project to use web camera released in 2011 as in-vehicle camera

衝動買いしたが使用していないパーツで実装したので性能はあまり良くない  
There is no performance because it was Impulse buying by parts purchased dynamically and not used

電源ON後に自動的に録画を開始。LAN環境にてブラウザから録画内容を取得、カメラの向きをブラウザから操作も可能  
Recording starts automatically after power on. Acquire the recording content from the browser in the LAN environment, you can also operate the orientation of the camera from the browser

車での運用はスマートフォンのBlue Toothテザリングでネットワーク接続する想定。  
Operation by car is assumed to be network connection by blue tooth tethering of smartphone
転送速度に不満がある場合は、シャットダウン後SDカードから直接データを取得する  
If you are not satisfied with the transfer speed, Acquire data directly from the SD card after shutdown

電源切断時に録画中のデータは破損するが、ある程度修復する機能を追加  
If you turn off the power, the data being recorded will be broken,  
Added the ability to repair to some extent


## Requirement
・ソフト software  
Raspbian GNU/Linux 9.4  
python3  
Aache2  
bt-pan  
ffmpeg version 3.2.12-1  
motion4.0 バージョンは多分4  

・ハード hardware  
Raspberry Pi Zero W  
BSWHD05HSBK web Cmera  
TA7291P モータドライバ Motor driver  
ストリップボード Strip board  
半可変抵抗器 Semi-variable resistor  
タミヤのギアボックス2つ Tamiya gearboxes x2  
USBケーブルモータ(ドライバ電源用 加工が必要) USB cable For motor driver power supply  


## Install  
・ソフト software
visudo  
管理者権限を使用するコマンドの許可を行う  
Permit commands that use administrator privileges  
$ sudo visudo  
以下を追記  
Add the following  
---
www-data ALL=(ALL) NOPASSWD: /bin/systemctl stop drive_recorder.service
www-data ALL=(ALL) NOPASSWD: /bin/systemctl start drive_recorder.service
www-data ALL=(ALL) NOPASSWD: /usr/bin/motion -b
www-data ALL=(ALL) NOPASSWD: /sbin/shutdown
www-data ALL=(ALL) NOPASSWD: /sbin/reboot
---

Apache2  
/etc/apache2/sites-available/less 000-default.conf  
有効にする  
To enable  
---
Include conf-available/serve-cgi-bin.conf  
---

/etc/apache2/mods-available/mime.conf

AddHandler cgi-script .cgi .py


bt-pan 

motion  

本ソースコード Source code  

service  

・ハード hardware  
TA7291P  

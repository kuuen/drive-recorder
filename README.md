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

## Usage
ブラウザでアクセス。スマホのBlueToothテザリングではIPは192.168.44.122固定となる。変更方法は不明  
IP is fixed at 192.168.44.122 in BlueTooth tethering of the smartphone. Unknown change method  

映像一覧はOptions FollowSymLinks を使用  
Video list uses Options FollowSymLinks  

映像修正 破損した動画ファイルの修復を試みる。やってることはffmpegでコピーしてるだけ  
Video Fix Attempt to repair corrupted video files. All I do is copy it with ffmpeg  

statusモーションを記録中か実行中かを確認します。両方が同時に実行されることはありません  
status Check if motion is being recorded or running. Both will never run at the same time  

各機能のON,OFFボタン ON / OFF button of each function  

motion display画面  
矢印キーでカメラの向きを変更 Change direction of camera with arrow key  

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
インストールや設定 Installation and configuration  
・ソフト software
### visudo  
管理者権限を使用するコマンドの許可を行う Permit commands that use administrator privileges  
$ sudo visudo  
~~~
# 以下を追記 Add the following
www-data ALL=(ALL) NOPASSWD: /bin/systemctl stop drive_recorder.service
www-data ALL=(ALL) NOPASSWD: /bin/systemctl start drive_recorder.service
www-data ALL=(ALL) NOPASSWD: /usr/bin/motion -b
www-data ALL=(ALL) NOPASSWD: /sbin/shutdown
www-data ALL=(ALL) NOPASSWD: /sbin/reboot
~~~

### 動画保存領域確保
別マシンでラズベリーパイのsdカードをGparted等でfat32の領域を作成する Create a fat32 area with Gparted etc.  
Windowsで確認する場合はfatの領域が先頭になっていないと読めないらしいので注意  
In case of confirmation with Windows, it seems that it can not be read unless the area of fat32 is at the beginning  

作成したデバイス名を確認 Confirm the created device name  
~~~
$ sudo fdisk -l
...
Device         Boot    Start      End  Sectors  Size Id Type
/dev/mmcblk0p1          8192  3294921  3286730  1.6G  e W95 FAT16 (LBA)
/dev/mmcblk0p2       3294922 60637183 57342262 27.4G  5 Extended
/dev/mmcblk0p5       3301376  3366909    65534   32M 83 Linux
/dev/mmcblk0p6       3366912  3508223   141312   69M  c W95 FAT32 (LBA)
/dev/mmcblk0p7       3514368 19677183 16162816  7.7G 83 Linux
/dev/mmcblk0p8      19679232 60637183 40957952 19.5G  b W95 FAT32  ←　★これ
~~~

自動マウントするように編集 Edit to automount  
/etc/fstab  
追記する Append  
~~~
/dev/mmcblk0p8  /media/data    vfat    auto,rw,user,users,exec,noatime,uid=1000,gid=1000,umask=000    0    0
~~~

### Apache2
~~~
$ sudo apt-get install apache2
~~~
/etc/apache2/sites-available/less 000-default.conf  
有効にする To enable  
~~~
# Include conf-available/serve-cgi-bin.conf
Include conf-available/serve-cgi-bin.conf
~~~

/etc/apache2/mods-available/mime.conf  
.piを追記する Append
~~~
# AddHandler cgi-script .cgi
AddHandler cgi-script .cgi .py
~~~
/etc/apache2/conf-available/serve-cgi-bin.conf
cgiを動かすディレクトリを指定 Specify the directory to run cgi
~~~
        <IfDefine ENABLE_USR_LIB_CGI_BIN>
#               ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
                ScriptAlias /cgi-bin/ /home/pi/work/DriveRecoder/cgi-bin/
#               <Directory "/usr/lib/cgi-bin">
                <Directory "/home/pi/work/DriveRecoder/cgi-bin">
                        AllowOverride None
                        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
                        Require all granted
                        SetEnv PYTHONIOENCODING utf-8
                </Directory>
~~~

編集後にApache2を再起動 Restart Apache 2  

### motion
~~~
$ sudo apt-get install motion
~~~
設定ファイルの修正 Modify configuration file  
詳しく把握していない。とりあえず動いている I do not know in detail but　It is moving now  
リポジトリのファイルを参照 Browse files in repository  
/etc/motion/motion.conf  

### 本ソースコード Source code  
ソースコードを/home/pi/work/DriveRecoder/に設置する想定  
Assume that source code is installed in /home/pi/work/DriveRecoder/  

apache2のドキュメントルートにシンボリックリンクを貼る  
Paste symbolic link to document root of apache2  
~~~
sudo ln -s /home/pi/work/DriveRecoder/html/ /var/www/
~~~
動画保存領域を参照する Refer to movie storage area  
~~~
sudo ln -s /media/data/driveRecoder/ /home/pi/work/DriveRecoder/html/drive/
~~~
serviceを登録 Register service   
シンボリックリンクで貼り付ける Paste with symbolic link  
~~~
$ sudo ln -s /home/pi/work/DriveRecoder/service/drive_recorder.service /etc/systemd/system/
~~~

serviceを有効にする Enable service   
~~~
$ sudo systemctl enable drive_recorder
~~~
サービスを起動してsyslogやsystemctl status 等を参照して正常かを確認する  
Start the service and check whether it is normal by referring to syslog, systemctl status etc.

### bt-pan 
OS起動時にBlueToothテザリングで親機に接続するように設定。以下の設定では再接続機能は持ってない  
Set to connect to the parent device with BlueTooth tethering at OS startup. The following settings do not have the reconnection function  
ペアリングする  
親機のBlutToothテザリング機能をONにする。記述ははXperia X Performanceで行ったもの  
Turn on the BlutTooth tethering function of the parent machine. Description is made by Xperia X Performance  

親機の設定 Host setting  
設定-ネットワークとインターネット-テザリング-BluetoothテザリングをOn  
Menu  
Settings-Network and Internet-Tethering-Bluetooth Tethering On  

ラズベリーパイ側で親機のmacアドレスを確認 Confirm the master's mac address on the raspberry pi side  
~~~
pi@raspi-zero2:~ $ hcitool scan
Scanning ...
	FF:FF:FF:FF:FF:FA	Xperia X Performance
pi@raspi-zero2:~ $ bluetoothctl
[bluetooth]# scan on
No default controller available
[bluetooth]# exit
~~~
ペアリング設定 Pairing setting  
確認した親機のmacアドレスを指定する  Specify the confirmed mac address of the parent device
~~~
$ sudo bluetoothctl
[NEW] Controller B8:27:EB:6A:70:D1 raspi-zero2 [default]
[bluetooth]# scan on
Discovery started
[CHG] Controller B8:27:EB:6A:70:D1 Discovering: yes
[NEW] Device FF:FF:FF:FF:FF:FA Xperia X Performance
[bluetooth]# pair FF:FF:FF:FF:FF:FA
Attempting to pair with FF:FF:FF:FF:FF:FA
...
...
[CHG] Device FF:FF:FF:FF:FF:FA ServicesResolved: yes
[CHG] Device FF:FF:FF:FF:FF:FA Paired: yes
Pairing successful

[bluetooth]# exit
~~~

bt-panを使用。これを使用すればもしかしたら上記の設定は必要ないかも  
Use bt-pan. If you use this you may not need the above settings  
~~~
$ cd /home/pi/work/bt-pan/
$ wget https://raw.githubusercontent.com/mk-fg/fgtk/master/bt-pan
$ chmod +x bt-pan
~~~
OS起動時に接続するように、serviceを作成 Create a service to connect at OS startup  
(これもgitに上げるか？)

/home/pi/work/bt-pan/bt-pan-client-start.sh
~~~
#!/bin/sh

sudo /home/pi/work/bt-pan/bt-pan client FF:FF:FF:FF:FF:FA
~~~

/home/pi/work/bt-pan/bt-pan-client-start.service
~~~
[Unit]
Description=RFCOMM service
After=bluetooth.service
Requires=bluetooth.service

[Service]
ExecStart=/home/pi/work/bt-pan/bt-pan-client-start.sh
#ExecStop=/home/pi/work/bt-pan/bt-pan-client-end.sh

[Install]
WantedBy=multi-user.target
~~~

シンボリックリンクで貼り付ける Paste with symbolic link
~~~
$ sudo ln -s /home/pi/work/bt-pan/bt-pan-client-start.service /etc/systemd/system/
~~~

serviceを有効にする Enable service   
~~~
$ sudo systemctl enable bt-pan-client-start
~~~

・ハード hardware  
TA7291P  
[TA7291Pの概要](https://toshiba.semicon-storage.com/jp/product/linear/motordriver/detail.TA7291P.html)  
モータドライバは2つ使用して２つのギアボックスを制御  
Two motor drivers control two gearboxes  
ギアボックスはカメラを上下、左右に向きを変えるように固定する  
The gearbox will lock the camera up and down, turn it sideways  
モータドライバのPIN5,6をそれぞれGPIO17，27と22，23と接続(17,27は上下、22と23は左右の動き)  
Connect PINs 5 and 6 of the motor driver to GPIO 17, 27 and 22 and 23, respectively (17 and 27 move up and down, 22 and 23 move left and right)  
モータドライバのPIN7はラスベリーパイの3.3ｖに接続  
Motor driver PIN7 connected to 3.3v of Rathberry pi  
モータドライバのPIN8はUSBから5.5vを受ける  
Motor driver PIN 8 receives 5.5v from USB  
モータードライバーPIN4は、USB電源の5.5ｖから半可変抵抗器で3.0Vに調整  
Motor driver PIN4 is adjusted from 5.5v to 3.0v with semi variable resistor from USB  
モータドライバのPIN1はラズベリーパイ、USBのGNDに接続  
Motor driver PIN1 connected to raspberry pi, USB GND  
図にしたほうがわかりやすいか？




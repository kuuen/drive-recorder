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
Windowsでの確認する場合はfatの領域が先頭になっていないと読めないらしいので注意  
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

シンボリックリンクで貼り付ける Paste with symbolic link
~~~
$ sudo ln -s /home/pi/work/bt-pan/bt-pan-client-start.service /etc/systemd/system/
~~~


・ハード hardware  
TA7291P  

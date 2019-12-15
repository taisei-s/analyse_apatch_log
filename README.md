ripository
==========
    analyse_apache_log.py
Apache HTTP サーバのアクセスログを解析するプログラム。  
アクセスログから以下2点のアクセス件数を取得し、コマンドラインで表示する。  
　ー各時間帯毎のアクセス件数  
　ーリモートホスト別のアクセス件数  

Dependency
==========
    python version:
        python3.6.9
    libraries:
        apache-log-parser==1.7.0
        user-agents==2.0

Usage
=====
    >>> python3 analyse_apache_log.py [-f file*] [-t date1 date2] [--logformat format]
デフォルトのファイルパスは/var/log/httpd/access_log  
-f　ファイルの指定。複数指定、ワイルドカードも使用可能。オプションなしは/var/log/httpd/access_log  
-t　期間の指定。date1~date2の期間内でアクセス件数を取得。オプションなしははすべての期間で取得  
    date format：%Y/%m/%d  
--logformat　アクセスログのフォーマットの指定。オプションなしは'%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'  

Author
======
佐藤太清
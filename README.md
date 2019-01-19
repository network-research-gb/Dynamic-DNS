# Dynamic-DNS
A small [No-IP](https://en.wikipedia.org/wiki/No-IP) services

Dynamic DNS system using [dnspython](http://www.dnspython.org/)

### Install: 
+ Install [dnspython](http://www.dnspython.org/)
  + `sudo apt-get install python-dnspython` 
  + Download: http://www.dnspython.org/kits/, extract it and run `python setup.py install`
+ Install [Gunicorn](https://gunicorn.org/): Là một **[Web Server Gateway Interface (WSGI)](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface)** trong Python. 
 
   ```py
    pip install gunicorn
    cat myapp.py
      def app(environ, start_response):
          data = b"Hello, World!\n"
          start_response("200 OK", [
              ("Content-Type", "text/plain"),
              ("Content-Length", str(len(data)))
          ])
          return iter([data])
    gunicorn -w 4 myapp:app
    ```

  WSGI, khác với HTTP, CGI và FCGI, **không phải là chuẩn giao thức liên lạc (communication protocol) mà là chuẩn giao tiếp (standard interface) giữa ứng dụng máy chủ (server) và các khung xương (framework) hay các ứng dụng web (web application)**. Lớp WSGI giúp lớp ứng dụng trao đổi với lớp máy chủ theo một cách khả chuyển, tức là một ứng dụng WSGI server có thể chạy giống nhau trên máy chủ khác nhau như Apache, NGINX, hay Lighttpd.
### Usage:
+ Step 1: [ddns.py](/ddns.py) is served by gunicorn
  + `gunicorn file_name:app`
  + `gunicorn ddns:app`
+ Step 2: Configure nginx as reverse proxy:
  
  ```
  location /dyndns/ {
    auth_basic "booh.";
    auth_basic_user_file /etc/nginx/htpasswd;
    proxy_pass http://localhost:8000/;
  }
  ```
+ Step 3: Use [crontab](https://en.wikipedia.org/wiki/Cron) to automate the script [client_side](/client_side.sh) every 5 minutes.

  ```
  chmod u+x backup.sh
  sudo ./backup.sh
  ```
  
  + Install crontab: 
  
    ```
    apt-get update && apt-get upgrade
    dpkg -l cron
    apt-get install cron
    systemctl status cron
    ```
  
  + Crontab syntax : 
  
    ```
    *      *    *    *    *           <user>  <command>
    minute hour day month day_of_week <user>  <command>
    
    # .---------------- minute (0 - 59)
    # | .------------- hour (0 - 23)
    # | | .---------- day of month (1 - 31)
    # | | | .------- month (1 - 12) OR jan,feb,mar,apr ...
    # | | | | .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat

    ```
  + Crontab special syntax:
    
    ```
    @hourly  - Shorthand for 0 * * * *
    @daily   - Shorthand for 0 0 * * *
    @weekly  - Shorthand for 0 0 * * 0
    @monthly - Shorthand for 0 0 1 * *
    @yearly  - Shorthand for 0 0 1 1 *
    @reboot  - Runs the command once at startup
    ```
    
  + Crontab example
    
    ```
    # Run a command every minute
    * * * * * 
    # Run a command every 12th minute on the hour
    12 * * * *
    # Run a command every 15 minutes
    0,15,30,45 * * * *
    # Run a command every day at 4:00am
    0 4 * * *
    # Run a command every Tuesday at 4:00am
    0 4 * * 2
    # Run the command every 15 minutes and between the hours of 2:00am and 6:00am
    */4 2-6 * * *

    ```
  + Configure cron jobs to schedule on Ubuntu
    + Open terminal 
    + First, let’s edit the crontab the following command:  
      
      ```
      crontab -e
      ```
      
      Hiện ra một khung như hình dưới:
      
      ![](https://lh3.googleusercontent.com/9o4Ldu3KpSWw8e6QiCjwZY9SrGE2CcPziWGU6mmB53cMXnBBi2qA7MTTBS8gXNS1tq3DQ9pGSAsFLl0PeHtZPzVctauqfqQg5AyFCh394BypQW4288hG4wy6NWEQCJYzEP4gK5mwbj0aWXemmftBRZfR-oRTbPX-tspIN6CWo7sTlp6scp76HQhbQcunoWkYx8gq5n6srx4nN-nT7Har8vfyWT7sQF15TtrzJXsv0EmY0Yw1P0T8Ge-vQneifLkSZPld3g53Byu05NgVquFSJ-yXvTCPxxdl-G92diB-ZqTFYmhMlNtmVdPEz3ytTj8FvdDdIFGu6wDvsZzQrXu60pi2vaNoQ-juHAkqXZ_QdoJbafxTTsKR00i34ATgMOKPui8BURznpZQOKMd00n3JW-CPACTQ16RhwrhBr_nnLEvw4x9EofMucngLqN7cUxdE3ppQl0zrHUDjTWaMeKOZceYUmtHrnoU6e1ofTC-7GhbF6PgksKZ1-cj0a1FXMnYOhs9zQDhM9BW1dUbI1C8epq0uo_kSVS_cCy3W2eUxR61I5p0C0CQ5Kt8tbgikuDaEabCzXwh_E7G1pW9_VXC4RiObY5LMajCjAOsx-5G-2yu6ZY3ifWDkHulKYA5etMLIAvUZ4TPtZ2YBz7xKWIqNQpRVSJCNV8M-jgZ7nYSMuKeb0Svy9gRIFg-wcY08TuJ61w3eE-LBrDE7YIFXHA=w565-h389-no)
    + Input:
      
      ```
      SHELL=/bin/bash
      PATH=/sbin:/bin:/usr/sbin:/usr/bin
      MAILTO=root
      
      #This is a comment
      * * * * * echo 'Run this command every minute' >> file.log
      ```
      
      Trong project, dynamic DNS update 5 phút 1 lần:
      
      ```
      SHELL=/bin/bash
      PATH=/sbin:/bin:/usr/sbin:/usr/bin
      MAILTO=root
      
      #This is a comment
      5 * * * * /bin/bash /home/flightstar/client_side.sh
      5 * * * * /home/flightstar/client_side.sh
      ```

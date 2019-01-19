# Dynamic-DNS
A small No-IP services

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

  WSGI, khác với HTTP, CGI và FCGI, **không phải là chuẩn giao thức liên lạc (communication protocol) mà là chuẩn giao tiếp (standard interface) giữa ứng dụng máy chủ (server) và các khung xương (framework) hay các ứng dụng web (web application)**. Lớp WSGI giúp lớp ứng dụng trao đổi với lớp máy chủ theo một cách khả chuyển, tức là một ứng dụng WSGI server có thể chạy giống nhau trên máy chủ khác nhau như Apache, NGINX, hay Lighttpd, sử dụng các giao thức khác nhau như CGI, FCGI, SCGI, hay AJP. 
### Usage:

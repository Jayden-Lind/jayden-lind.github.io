---
layout: post
title: Creating Certificate for EdgeMAX device
#subtitle: Excerpt from Soulshaping by Jeff Brown
#cover-img: /assets/img/path.jpg
#thumbnail-img: /assets/img/thumb.png
tags: [homelab]
---
<p>Creating an internal CA (certificate authority), has saved the annoyance of having to click "Proceed Anyway" through Chrome or Internet Explorer every time I open up a HTTPS enabled web interface for one of my devices. It also has enabled me to learn more about certificate process.</p>

<p>Today I'm going to create a SSL certificate signed by my internal CA (linds-CA) that will allow all my domain joined computers (and all other devices that have trusted my CA) to be able to access these devices without an issue, as well as adding an extra layer of security.</p>

<p>First I will need to create a CSR (Certificate Signing Request) from my EdgeMAX device.<br>I can do this by using OpenSSL on the device. An easy way to get the command needed to create this, is using a generator like <a rel="noreferrer noopener" href="https://www.digicert.com/easy-csr/openssl.htm" target="_blank">so</a>. I ran into issues doing this, as the OpenSSL request with the generator, doesn't include any subject alternative names, or SAN.</p>

<p>Instead I created the request from my desktop, using a Custom Request...<br>TAKE NOTE: Where you requested it from, I requested it from my PC, under Local Computer -&gt; Personal -&gt; Certificates</p>

![image](/img/2020/04/image-20.png)

<p>I chose to use my Active Directory Enrollment Policy, and chose my Web Server template to speed things up. Once you are onto Certificate Information, click properties and enter the details that are relevant to you</p>

![image](/img/2020/04/image-21.png)

![image](/img/2020/04/image-22.png)

<p>In Extensions tab, under Extended Key Usage, Select Client Authentication option, as well as in the Private Key tab, under Key options, make sure "Make private key exportable" is selected. <br>Once done, click OK, and then click Next<br>Save the file somewhere safe.</p>

<p>With this file, I can submit it directly to the CA through MMC, or I can submit it through Certificate Authority Web Enrollment.<br>I'm going to do this through my CA Web Enrollment, as it's quicker.<br>Head to your web enrollment page, and select "Request a certificate"</p>

![image](/img/2020/04/image-15.png)

<p>Then click "Or, submit an advanced certificate request"</p>

![image](/img/2020/04/image-16.png)

<p>Copy and paste the contents of the CSR or output of using <em>cat</em> on the file into the Saved Request: textbox. Choose a Certificate Template of Web Server, and click submit.</p>

![image](/img/2020/04/image-17.png)

<p>You will need to approve this request, which can be done by opening up the Certificate Authority console, expanding your CA server, and then going to Pending certificates. Right click your request, All Tasks -&gt; Issue</p>

![image](/img/2020/04/image-18.png)

<p>Open Issued Certificates under your CA server, find your newly issued certificate, double click and head to the Details tab. <br>Click "Copy to File..."</p>

![image](/img/2020/04/image-19.png)

<p>Click Next, select "Base-64 encoded X.509 (.CER)". Store this file somewhere easy to access.</p>

<p>Install this certificate in the same location that you requested it on the computer you requested it from. For example back into my local PC Certificates -&gt; Personal -&gt; Certificates. <br>Open the certificate up through the console, and you will now see that you have the Private Key with that certificate.<br></p>


![image](/img/2020/04/image-23.png)

<p>We now need to extract this Private Key and combine it with the certificate to use on our EdgeMAX device.</p>

<p>Go to the Details Tab of your certificate, click "Copy to File...", click Next, select Yes, export the private key, click Next. Click Next again and you will be forced to include a password. Use a password you can remember. Click Next, and save to a location that is safe.</p>

![image](/img/2020/04/image-24.png)

<p>Jump back to the SSH console, and copy across your newly exported .pfx and the CA certificate through SSH to a folder, such as /config/auth.</p>

<p>We now need to extract the .key and .crt, we can do this using OpenSSL on the EdgeMAX. While still in the SSH session use the command below, it will ask you to enter the password you used above, as the Import Password.<br>It will now ask you for a password to protect the .key file, enter another password and keep that one safe</p>

```openssl pkcs12 -in ubnt.pfx -nocerts -out ubnt.key```

<p>I now have the private key by itself encrypted by the passphrase I just gave it. Run the below command (with your file names) to decrypt the private key.</p>

```openssl rsa -in ubnt.key -out ubnt-decrypted.key```

<p>Now we need to extract the actual certificate that goes along with that private key, and we can achieve this, by running the below command</p>

```openssl pkcs12 -in ubnt.pfx -clcerts -nokeys - out ubnt.crt```

<p>If we cat ubnt.crt, we are presented with the below</p>

```
Bag Attributes
localKeyID: 01 00 00 00
friendlyName: LINDS-ERX
subject=/C=AU/ST=VIC/L=Langy/O=LINDS/CN=linds-erx
issuer=/DC=au/DC=com/DC=linds/CN=linds-CA
-----BEGIN CERTIFICATE-----
MIIFnjCCBIagAwIBAgITRQAAADDBVvjt5tSiJQAAAAAAMDANBgkqhkiG9w0BAQsF
ADBTMRIwEAYKCZImiZPyLGQBGRYCYXUxEzARBgoJkiaJk/IsZAEZFgNjb20xFTAT
BgoJkiaJk/IsZAEZFgVsaW5kczERMA8GA1UEAxMIbGluZHMtQ0EwHhcNMjAwNDIy
MDk1MDIwWhcNMjIwNDIyMDk1MDIwWjBPMQswCQYDVQQGEwJBVTEMMAoGA1UECBMD
VklDMQ4wDAYDVQQHEwVMYW5neTEOMAwGA1UEChMFTElORFMxEjAQBgNVBAMTCWxp
bmRzLWVyeDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALzkxxUsPbNY
0BHjwWXlIjf39a2/Kfl82yxaaE9cuJU3A6aSaSx66Vj8ujBWGlY39zUhsOnYwSdo
5pMzNnXgXj+cDm8ZzPzUzbeka6EU1NiwVSDXcd36CPyB0l+UcquhchhAm+brf6Qa
g0u5awPnkMxA+SLl4LOveNQyQ39Q528UNjXNgwP7OeWxB+ePpUdyK7wnLFcOsjNG
T45zwPrn4W0p9n2ZFFHmQo2mC4EGlEBU0Ew05DuZ8MlUIrvW5cId/u/t0um6g/7/
KKiO39gF6vNA5XqR5/n4azb80SlXAzB5rDD35QFCcmQrmezNz2/Yqv8vYd1loZJJ
9Xke/QLz3UUCAwEAAaOCAm0wggJpMCEGCSsGAQQBgjcUAgQUHhIAVwBlAGIAUwBl
AHIAdgBlAHIwDgYDVR0PAQH/BAQDAgWgMBMGA1UdJQQMMAoGCCsGAQUFBwMBMCcG
CSsGAQQBgjcVCgQaMBgwCgYIKwYBBQUHAwEwCgYIKwYBBQUHAwIwHQYDVR0OBBYE
FBlMCORAvbWozlDl90a/8gq4QSm8MCcGA1UdEQQgMB6CFmxpbmRzLWVyeC5saW5k
cy5jb20uYXWHBMCoBgEwHwYDVR0jBBgwFoAUY9vCKW1+0y1E+DCrVqvqYbZH2+ww
gcsGA1UdHwSBwzCBwDCBvaCBuqCBt4aBtGxkYXA6Ly8vQ049bGluZHMtQ0EsQ049
TElORFMtREMsQ049Q0RQLENOPVB1YmxpYyUyMEtleSUyMFNlcnZpY2VzLENOPVNl
cnZpY2VzLENOPUNvbmZpZ3VyYXRpb24sREM9bGluZHMsREM9Y29tLERDPWF1P2Nl
cnRpZmljYXRlUmV2b2NhdGlvbkxpc3Q/YmFzZT9vYmplY3RDbGFzcz1jUkxEaXN0
cmlidXRpb25Qb2ludDCBvgYIKwYBBQUHAQEEgbEwga4wgasGCCsGAQUFBzAChoGe
bGRhcDovLy9DTj1saW5kcy1DQSxDTj1BSUEsQ049UHVibGljJTIwS2V5JTIwU2Vy
dmljZXMsQ049U2VydmljZXMsQ049Q29uZmlndXJhdGlvbixEQz1saW5kcyxEQz1j
b20sREM9YXU/Y0FDZXJ0aWZpY2F0ZT9iYXNlP29iamVjdENsYXNzPWNlcnRpZmlj
YXRpb25BdXRob3JpdHkwDQYJKoZIhvcNAQELBQADggEBANDR3v39SrI6hFjiyDHw
hgErmsAIRYtVzN7GDFarLLTizX+kL/z0vDOAQ49ZdXPSoY1fskY0fjTk4VtDWIDz
o4rSXxQgovSusKxYSHbb/pQhY4gDF9Xn2snxt7mvORdemrC+AAVcgJEYwx/oSDXz
hevxYiIEx8+TRudZFdf3iR/kNZJTPW6gh5w64Lox6juN0uFOKczEGOXqfBFA0bLz
F1VRHOdSn3pR9v5UV5ykHA+O0bGIEbXNvzHc1F6qKLCYLG/d4Teil3ao40RiAIo1
7woCJpsMnZsXcPiRxoAVIWq0o7fNrF/afcJJ4+xMBetEl+eAvPNn6Cb+upnlnkeL
QOE=
-----END CERTIFICATE-----
```

<p>If we remove the top, before ----BEGIN CERTIFICATE----, and change the file extension to .cer, we can combine the private key (.key) and certificate (.cer) for use with out EdgeMAX device.</p>

<p>After doing that, I will combine them, by using cat, like below,</p>

```cat ubnt-decrypted.key ubnt.cer &gt; ubnt-signed.cer```

<p>Once we have ubnt-signed.cer, we can use <em>cat</em> to have a look at it, and you shall see something like this.</p>

```
-----BEGIN RSA PRIVATE KEY-----
MIIE.......
-----END RSA PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIIFIW.....
-----END CERTIFICATE-----
```

To set this on the EdgeMAX device, open/resume a SSH session.<br>Enter configure mode, by entering 

```
configure
set service gui cert-file /config/auth/<cer file>;
set service gui ca-file /config/auth/<ca file>;
commit 
```

Open up a web browser and head towards your EdgeMAX devices web interface

![image](/img/2020/04/image-25.png)

<p>As long as your computer trusts your CA, you will not be prompted, and immediately greeted with your login page.</p>

![image](/img/2020/04/image-27.png)

<p></p>

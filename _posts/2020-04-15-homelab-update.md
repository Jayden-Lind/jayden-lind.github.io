---
layout: post
title: Homelab Update 15/04/2020
#subtitle: Excerpt from Soulshaping by Jeff Brown
#cover-img: /assets/img/path.jpg
#thumbnail-img: /assets/img/thumb.png
tags: [homelab]
---

<p>It has been a while since my last post. I have completed some updates over the past few months to my Homelab. The biggest addition is using Docker, which was a challenging but rewarding experience. I also changed from Hyper-V back to ESXi, while also running vCenter Server, upgraded the RAM from 48GB to 64GB, which allowed me to have more VM’s running. Docker My Docker instance is running on a Red Hat Enterprise Linux VM, which gave me a chance to learn more about Linux.</p>

![image](/img/2020/04/LINDs-Network-6.jpg)

<h2>Docker</h2>

<p>My Docker instance is running on a Red Hat Enterprise Linux VM, which initially started out as something to learn more about Linux. Transforming it to Docker allowed me to learn even more about Linux.</p>

<p>I currently have UNMS (Ubiquiti Network Management System) and the UniFi controller running to actively configure and monitor my network, I also have the entire Monolithic Lancache set up, that receives forwarded DNS requests from Pi-Hole when the DNS requests are Steam, Blizzard, Riot, Origin etc CDN's, and it caches all the downloads, including updates to the 12TB storage through SMB.</p>

<p>The PostgreSQL server was used when I was developing a web application using Django (Python) to learn Python.</p>

<p>The speedtest container, is a simple HTM5 web instance, that will allow me to perform quick speed test on any device internally.</p>

<p>Watchtower is a great addition, as it automates image updates for my running containers, which requires no administrative effort.</p>

<h2>Hyper-V to ESXi</h2>

<p>I moved to ESXi, as Hyper-V was becoming less of a challenge. I couldn't utilise SCSI Bus Sharing, which gave me another reason to switch Hyper Visors. It was simple to do, I used Starwind V2V to convert the VHDX's to VMDK's and then used VMWare standalone converter to reduce the size of the VMDK's from 127GB each to their respective sizes.</p>

<p>I installed the vCenter server appliance to try and setup an LACP group, which took a lot longer than expected, but I eventually sorted that out, and now have an active LACP connection up and running with 2x1Gbps ethernet connections.</p>

<h2>Automation</h2>

<p>Previously I was using a VM with Backblaze to backup my 12TB of data, and it would require me to turn the VM on when I know my network was not being used. I have now moved to installing PowerCLI, which is VMWare's PowerShell modules to connect and interact with VMWare servers. I wrote a couple of PowerShell scripts to automatically turn on the backup server and then turn it off again at specific times using Task Scheduler on LINDS-DC2. An example script is below.</p>
![image](/img/2020/04/image.png)
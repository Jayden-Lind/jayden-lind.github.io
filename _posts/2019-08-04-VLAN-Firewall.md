---
layout: post
title: VLAN And Firewall Rules – DMZ
#subtitle: Each post also has a subtitle
tags: [homelab]
#comments: true
---
<p>The website you are currently on, is located on my server at home. Having this hosted at home can bring some security issues. Having no firewall rules, can allow a compromised machine (Web Server) unfiltered access to the other networks, which could result in damage. I want to prevent this, and one of the best ways to achieve this, is by setting up firewall rules between the networks.</p>

<p>The EdgeRouterX-SFP, has a nice GUI to implement these rules, but is a stateful firewall, which is a different approach compared to traditional firewalls I've used before.</p>

![image](/img/2019/08/ac3e4fab-ac45-4e42-b8b3-d6a22e7bdd7f.png)
<a href="https://community.ui.com/questions/Laymans-firewall-explanation/2dafa379-3269-4749-b224-0dee15374de9"></a><figcaption>Explanation of Rules<br>Posted by BranoB on Ubiquiti Community Forums</figcaption></figure>

![image](/img/2019/08/LINDs-Network-2.png)

<p>I've created 3 separate rules, VLAN20-IN, VLAN20-LOCAL, VLAN20-OUT</p>
![image](/img/2019/08/image.png)

<h2>Creating the Rules</h2>

<p><strong>VLAN20 - IN</strong><br>This as the traffic from VLAN20 into the routing, before it is routed to different interfaces etc. Since I want to block traffic from VLAN20 to VLAN1, my rule needs to drop traffic with a destination of VLAN20 and VLAN1 addresses. I want to be able to access these servers, but only from my personal computer (IP: 192.168.6.128). The rules below meet this requirement</p>
![image](/img/2019/08/image-1.png)

<p><strong>Explanation:</strong><br>Rule 1. If the destination of the traffic is to 192.168.6.128, accept the traffic and forward it.<br>Rule 2. If the destination of the traffic is to the 192.168.6.1/24 subnet, drop the traffic.<br>Rule 3. If the destination of the traffic is to the 192.168.1.1/24 subnet, drop the traffic.</p>

<p><strong>Verification:</strong><br>1. If my IP is 192.168.6.128 and I ping anything in VLAN20, I should receive a response.</p>
![image](/img/2019/08/image-3.png)

<p>2. If my IP is not 192.168.6.128, but in the 192.168.6.1/24 subnet, I will not receive a ping response.</p>
![image](/img/2019/08/image-4.png)

<p><strong>VLAN20 - LOCAL</strong><br>VLAN20 - LOCAL is the traffic direction towards the router itself. Here you can limit what the devices on this VLAN can get from the router. This is useful for blocking administration access to the router (ie HTTP, HTTPS, SSH). My goal was to block everything except DHCP traffic, and include 1.1.1.1 as the DNS in the DHCP scope.</p>
![image](/img/2019/08/image-5.png)

<p><strong>Verification:</strong><br>This is easily verified by trying to access the router on 10.1.1.1 which is defined in the DHCP Scope.</p>
![image](/img/2019/08/image-9.png)

<p><strong>VLAN20 - OUT</strong><br>VLAN20 - OUT is the traffic leaving the router. I obviously want the HTTP, HTTPS and DNS traffic leaving VLAN20, as it currently hosts the website and the DNS. I also want to be able to connect to the VM to add/edit posts on the website.</p>
![image](/img/2019/08/image-6.png)

<p><strong>Verification:</strong><br>From a device/VM inside VLAN20, I should be able to ping 192.168.6.128.</p>
![image](/img/2019/08/image-7.png)

<p>From a device in VLAN20, I should only be able to browse HTTP/HTTPS traffic, but not ping the host.</p>
![image](/img/2019/08/image-8.png)

<h2>Additional</h2>

<p>Running these VM's in a Hyper-V environment, means different measures also need to be taken. Since the VM Switch is on the Hyper-V host, and was created with the defaults, the Hyper-V host is connected to that VLAN, and if somehow someone was able to gain access to a VM on VLAN20, they might be able to get their way through to the Hyper-V host and take over the network.</p>

<p>To prevent this, we need to turn off management OS on the VM Switch. We can do this by running a simple PowerShell command, "Get-VMSwitch | fl"</p>
![image](/img/2019/08/image-10.png)

<p>We can see that the "AllowManagementOS" option is set to "True". We can disbale this with "Set-VMSwitch -Name "DMZ Switch" -AllowManagementOS $false", which will remove the vSwitch adapter from the Hyper-V host and remove the ability for the VM's inside that vSwitch to connect to the Hyper-V host and potentially jeopardising the network.</p>

<h2>Conclusion</h2>

<p>From these rules and testing with verification, I can now sleep better with some extra added security to my network.</p>

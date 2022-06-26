---
layout: page
title: My Homelab
#subtitle: Excerpt from Soulshaping by Jeff Brown
#cover-img: /assets/img/path.jpg
#thumbnail-img: /assets/img/thumb.png
icon: fas fa-info-circle
tags: [homelab]
---

# 2022 Half Year Update:

<a target="_blank" href="/img/LINDS-Network%202022.png" onClick='test(this)'>
![image](/img/LINDS-Network%202022.png){:target="_blank"}
</a>

There is a number of changes here, upgraded server, Dell R710 -> Dell T630, a new physical server, HPE DL360 G9, in a new location.

Changelog:

<ul> &#43; LINDS-OPNSense-01 (OPNSense 22.1)

<ul> &#43; HPE OfficeConnect 1920s

<ul> &#43; LINDS-ESXi-02 (Dell T630)

<ul> &#43; JD-ESXi-01 (HPE DL360 G9)

<ul> &#43; &#43; JD-DC-01 (Windows Server 2019)

<ul> &#43; &#43; JD-Dev-01 (CentOS 9 Stream)

<ul> &#43; &#43; JD-Zabbix-01 (CentOS 8 Stream)

<ul> &#43; &#43; JD-Plex-01 (CentOS 9 Stream)

<ul> &#43; &#43; JD-Docker-01 (CentOS 9 Stream)

<ul> &#43; &#43; JD-Torrent-01 (CentOS 8 Stream)

<ul> &#43; &#43; JD-VSCA-01 (vSphere Photon OS)

<ul> &#43; &#43; JD-Docker-01 (CentOS 9 Stream)

<ul> &#43; &#43; JD-OPNSense-01 (OPNSense 22.1)

<ul> &#43; &#43; JD-GitLab-01 (CentOS 8 Stream)

<ul> &#43; &#43; JD-GitLab-R01 (CentOS 8 Stream)

<ul> &#43; &#43; KUBE-ADM (CentOS 8 Stream)

<ul> &#43; &#43; KUBE-01 (CentOS 8 Stream)

<ul> &#43; &#43; KUBE-02 (CentOS 8 Stream)

<ul> &#45; LINDS-PiHole

<ul> &#45; LINDS-ERx (UBIQUITI EDGEROUTER X)

<ul> &#45; LINDS-Plex (Windows Server 2019)

<ul> &#45; LINDS-Veeam (Windows Server 2019)

<ul> &#45; LINDS-Web (Windows Server 2019)

<ul> &#45; LINDS-MineOS (Turnkey MineOS)

<ul> &#45; Dell PowerConnect 6248

<ul> &#45; LINDS-VSCA (vSphere Photon OS)


# 2020 Update:

<h2>Virtual Machines</h2>

![homelab](/img/LINDs-Network.jpg)

<p class="has-small-font-size"><strong>LINDS-DC</strong> - Domain Controller, DNS, File Shares, Certificate Authority - Server 2016<br><strong>LINDS-DC2</strong> - Domain Controller, DNS, Windows Deployment Services - Server 2019<br><strong>LINDS-PLEX</strong> - Plex Server - Server 2019<br><strong>LINDS-PiHole</strong> - DNS, Adblocking - CentOS 7<br><strong>LINDS-Backup</strong> - Backblaze client to backup the 12TB stored on LINDS-DC - Windows 10<br><strong>LINDS-MineOS</strong> - 4 Minecraft servers- Turnkey Linux<br><strong>LINDS-WEB</strong> - IIS (hosting this website) - Server 2019<br><strong>LINDS-Docker</strong> - Docker host that runs around 20 containers, which include UniFi controller, UNMS, Monolithic LanCache, PostgreSQL server - Red Hat Enterprise Linux<br><strong>LINDS-VEEAM</strong> - Veeam server, backups all servers except LINDS-DC due to RDM (Raw Device Mapping) being utilised<br><strong>VCSA</strong> - vCenter Server Appliance 6.7</p>
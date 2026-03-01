---
layout: page
title: Homelab
subtitle: Updates and diagrams of my homelab setup
icon: fas fa-info-circle
tags: [homelab]
order: 1
---
# 2026 Update:

![image](/img/2026/homelab.svg)

A lot has changed. New Server hardware, new virtualization platform, hardcore into Kubernetes, and a lot of automation.

### Infrastructure Updates
- **Hardware Upgrade**: Swapped the HPE DL360 G9 for a Lenovo SR655 (EPYC 3rd gen 64-core CPU, 256GB RAM).
- **Virtualization**: Migrated both server nodes to Proxmox and using ZFS.
- **IaC**: Upgraded from Puppet to Ansible, Terraform, and Packer for automated VM provisioning.
- **Routing**: Upgraded routing to VyOS (replacing OPNSense).

### Kubernetes & Automation
- **Advanced Networking**: Extended Kubernetes cluster to use eBPF and established direct BGP peering with VyOS routers.
- **Consolidation**: The Majority of services have been consolidated onto the Kubernetes cluster, reducing number of VM's and improving manageability.

## Changelog - 2023-2026
### Added to JD Site
- JD-proxmox-01 (LENOVO-SR655 - Proxmox VE 9.1.4)<br>
- JS-VyOS-01 (VyOS 1.5 rolling)<br>
- talos-cp-01 (Talos OS)<br>
- talos-worker-01 (Talos OS)<br>
- talos-worker-02 (Talos OS)<br>
- talos-worker-03 (Talos OS)<br>
- USW-Enterprise-24-PoE (Ubiquiti UniFi Switch Enterprise 24 PoE)<br>
- USW-Enterprise-8-PoE (Ubiquiti UniFi Switch Enterprise 8 PoE)<br>
- 2x Unifi-7-Pro-AP (Ubiquiti UniFi 7 Pro Access Point)<br>
- 3x Unifi G5 Flex Camera
- 1x Unifi G6 Turrent Camera
- Unifi Cloud Key Gen 2 Plus

### Added to LINDS Site
- LINDS-proxmox-01 (Dell T630 - Proxmox VE 9.1.4)<br>
- LINDS-VyOS-01 (VyOS 1.5 rolling)<br>
- talos-linds-worker-01 (Talos OS)<br>
- talos-linds-worker-02 (Talos OS)<br>
- 2x Unifi-6-AP (Ubiquiti UniFi 6 Access Point)<br>
- 3x Unifi G5 Flex Camera
- Unifi Cloud Key Gen 2 Plus

# 2022 Half Year Update:

![image](/img/LINDS-Network%202022.png)

There is a number of changes here, upgraded server, Dell R710 -> Dell T630, a new physical server, HPE DL360 G9, in a new location.

## Changelog - 2022 H2

### Added \>

- LINDS-OPNSense-01 (OPNSense 22.1)<br>
- HPE OfficeConnect 1920s<br>
- LINDS-ESXi-02 (Dell T630)<br>
- JD-ESXi-01 (HPE DL360 G9)<br>
- \> JD-DC-01 (Windows Server 2019)<br>
- \> JD-Dev-01 (CentOS 9 Stream)<br>
- \> JD-Zabbix-01 (CentOS 8 Stream)<br>
- \> JD-Plex-01 (CentOS 9 Stream)<br>
- \> JD-Docker-01 (CentOS 9 Stream)<br>
- \> JD-Torrent-01 (CentOS 8 Stream)<br>
- \> JD-VSCA-01 (vSphere Photon OS)<br>
- \> JD-Docker-01 (CentOS 9 Stream)<br>
- \> JD-OPNSense-01 (OPNSense 22.1)<br>
- \> JD-GitLab-01 (CentOS 8 Stream)<br>
- \> JD-GitLab-R01 (CentOS 8 Stream)<br>
- \> KUBE-ADM (CentOS 8 Stream)<br>
- \> KUBE-01 (CentOS 8 Stream)<br>
- \> KUBE-02 (CentOS 8 Stream)<br>

### Removed \<

-  \< LINDS-PiHole<br>
-  \< LINDS-ERx (UBIQUITI EDGEROUTER X)<br>
-  \< LINDS-Plex (Windows Server 2019)<br>
-  \< LINDS-Veeam (Windows Server 2019)<br>
-  \< LINDS-Web (Windows Server 2019)<br>
-  \< LINDS-MineOS (Turnkey MineOS)<br>
-  \< Dell PowerConnect 6248<br>
-  \< LINDS-VSCA (vSphere Photon OS)<br>


# 2020 Update:

<h2>Virtual Machines</h2>

![homelab](/img/LINDs-Network.jpg)

<p class="has-small-font-size"><strong>LINDS-DC</strong> - Domain Controller, DNS, File Shares, Certificate Authority - Server 2016<br><strong>LINDS-DC2</strong> - Domain Controller, DNS, Windows Deployment Services - Server 2019<br><strong>LINDS-PLEX</strong> - Plex Server - Server 2019<br><strong>LINDS-PiHole</strong> - DNS, Adblocking - CentOS 7<br><strong>LINDS-Backup</strong> - Backblaze client to backup the 12TB stored on LINDS-DC - Windows 10<br><strong>LINDS-MineOS</strong> - 4 Minecraft servers- Turnkey Linux<br><strong>LINDS-WEB</strong> - IIS (hosting this website) - Server 2019<br><strong>LINDS-Docker</strong> - Docker host that runs around 20 containers, which include UniFi controller, UNMS, Monolithic LanCache, PostgreSQL server - Red Hat Enterprise Linux<br><strong>LINDS-VEEAM</strong> - Veeam server, backups all servers except LINDS-DC due to RDM (Raw Device Mapping) being utilised<br><strong>VCSA</strong> - vCenter Server Appliance 6.7</p>

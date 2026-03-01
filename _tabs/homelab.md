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

A lot has changed since 2022 - new hardware, a new virtualisation platform, a fully declarative Kubernetes stack, and everything managed as code. Full write-up: [Homelab 2026: Rebuilding the Stack from Bare Metal Up]({% post_url 2026-03-01-homelab-update-2026 %})

### Hardware & Virtualisation
- **New Server**: Lenovo SR655 with a 3rd-gen AMD EPYC (64 cores) and 256GB RAM, replacing the HPE DL360 G9. Single-socket design eliminates cross-NUMA latency; significant improvement across all workloads.
- **Proxmox VE**: Replaced ESXi on both nodes following VMware's licensing changes. Running ZFS for storage - transparent compression, checksumming, and no hardware RAID controller required.

### Kubernetes
- **Talos Linux**: Migrated Kubernetes nodes from Ubuntu + kubeadm to Talos - a minimal, immutable, SSH-less OS managed entirely through a declarative API. Eliminated an entire class of configuration drift and kernel upgrade fragility.
- **Cilium + eBPF**: Replaced kube-proxy and Flannel with Cilium as the CNI. eBPF-based datapath does O(1) service lookups via kernel hash maps, removing the IPTables rule-chain overhead that grows linearly with service count.
- **BGP peering**: Cilium's BGP control plane peers directly with VyOS, advertising `LoadBalancer` IPs across the network. No MetalLB required; node failure triggers automatic route withdrawal and instant failover.
- **GitOps with ArgoCD**: All workloads managed via Helm charts and ArgoCD. Cluster state is fully reproducible from Git - blowing up a namespace and reconciling back takes minutes.
- **Service consolidation**: Home automation, media, game servers, dev tooling, and infrastructure services all running on Kubernetes, managed uniformly via Helm and ArgoCD.

### Routing & Automation
- **VyOS**: Replaced OPNsense. Ansible-native CLI, Linux-based forwarding plane, and measurably lower CPU utilisation (20–30% on OPNsense → low single digits on VyOS).
- **Full IaC**: Packer builds golden VM images, Terraform provisions VMs and bootstraps the Talos cluster, Ansible handles post-provision config and VyOS management. Everything is version-controlled and reproducible.

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

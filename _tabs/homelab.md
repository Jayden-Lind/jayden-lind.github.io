---
layout: page
title: Homelab
subtitle: Updates and diagrams of my homelab setup
icon: fas fa-info-circle
tags: [homelab]
order: 1
---
# 2026 Update

![image](/img/2026/homelab.svg)

Full write-up: [Homelab 2026: Rebuilding the Stack from Bare Metal Up]({% post_url 2026-03-01-homelab-update-2026 %})

### Hardware

Two physical sites running as a single Kubernetes cluster.

**JD site:** Lenovo ThinkSystem SR655, AMD EPYC 7B13 (64 cores / 128 threads), 256GB Samsung DDR4 ECC @ 2933 MT/s, Proxmox VE 9.2.3. Single-socket design with a single NUMA domain eliminates cross-socket memory latency entirely.

Storage (ZFS):
- `NAS-SSD`: RAIDZ1 across 5x Samsung 870 EVO 4TB SSDs (18.2TB usable, 11TB used). NFS/iSCSI backing for Kubernetes PVs.
- `VM`: RAIDZ1 across 3x mixed SSDs (1.62TB usable). VM disk pool.
- `HDD-20T`: Mirrored pair of 20TB Seagate enterprise HDDs (20TB usable, 8TB used). Cold and bulk storage.

**LINDS site:** Dell PowerEdge T630, 2x Intel Xeon E5-2640 v4 (20 cores / 40 threads, dual-socket NUMA), 128GB RAM, Proxmox VE 9.2.3. Storage via PERC H730 hardware RAID controller.

Both sites run Ubiquiti UniFi switching and APs, with VyOS 1.5 (rolling) handling routing, BGP, RA VPN, DNS/DHCP, and site-to-site IPSec.

### Terraform ([LINDS-Terraform](https://github.com/Jayden-Lind/LINDS-Terraform))

Terraform provisions everything from bare Proxmox hosts to a running Kubernetes cluster.

- **VM provisioning**: Uses the [bpg/proxmox](https://registry.terraform.io/providers/bpg/proxmox/latest) provider to create VMs across both sites. Packer builds golden images (Ubuntu 24.04, CentOS 9) that Terraform clones per host.
- **Talos cluster bootstrap**: Generates Talos machine secrets, applies node configs to each control plane and worker, bootstraps etcd, and writes `kubeconfig` + `talosconfig` locally. The cluster is 1 control plane + 3 workers at JD (AMD EPYC), 2 workers at LINDS (Intel Xeon), all running Talos v1.13.2 and Kubernetes v1.36.0.
- **Per-arch kernel tuning**: AMD and Intel nodes get separate Talos schematics with architecture-specific flags. Both disable all CPU vulnerability mitigations, set `transparent_hugepage=always`, pin the governor to `performance` (`amd_pstate=active` / `intel_pstate=active`), enable BBR congestion control, isolate RCU callbacks (`nohz_full`, `rcu_nocbs`), and apply tuned TCP buffer / conntrack sysctls.
- **Cilium via Helm**: Cilium is deployed into `kube-system` directly from Terraform after bootstrap. kube-proxy is disabled; Cilium's eBPF datapath handles all service routing with O(1) kernel hash map lookups.
- **BGP wiring**: Terraform applies `CiliumBGPClusterConfig` and `CiliumBGPPeerConfig` CRDs post-Cilium. JD nodes peer with VyOS at ASN 64512/64550; LINDS nodes at ASN 64513/64551. Cilium advertises the `172.16.1.0/24` LoadBalancer IP pool and pod CIDRs to VyOS, which redistributes them across both sites. No MetalLB.

### Ansible ([LINDS-Ansible](https://github.com/Jayden-Lind/LINDS-Ansible))

Handles all post-Terraform configuration for non-Talos hosts. 14 playbooks and roles:

- **VyOS**: Full router config via `vyos.vyos` collection. BGP peering, IPSec site-to-site VPN, RA VPN, DNS/DHCP, NAT, firewall. VyOS itself gets kernel-level tuning (`disable-mitigations`, `network-throughput` mode, TCP buffer sysctls).
- **TrueNAS**: NFS/iSCSI configuration for Kubernetes persistent volume backing.
- **General services**: Plex, Minecraft, torrent hosts, dev VMs, WSL setup.
- **Common baseline**: NTP, auto-updates, logrotate applied uniformly.

### Kubernetes ([LINDS-Kubernetes](https://github.com/Jayden-Lind/LINDS-Kubernetes))

All workloads managed via ArgoCD and Helm. The repo is ArgoCD `Application` manifests; reconciliation is fully automated. Rebuilding from scratch: `./app-deployment.sh` bootstraps ArgoCD, then it self-heals to the desired state.

**Cluster:** 6 nodes (1 control plane + 5 workers), Talos v1.13.2, Kubernetes v1.36.0, all nodes `Ready` for 157 days.

**Infrastructure layer**

| Component | Details |
|---|---|
| Cilium 1.19 | CNI, kube-proxy replacement, eBPF datapath, BGP control plane, Hubble flow observability |
| ArgoCD + image-updater | GitOps reconciliation; image-updater auto-bumps tags on new pushes |
| cert-manager | Automatic TLS via Let's Encrypt |
| Vault + external-secrets | Secrets management; external-secrets syncs Vault secrets into Kubernetes |
| external-dns | Syncs LoadBalancer/Ingress hostnames to internal DNS automatically |
| nginx-ingress | Ingress controller, running as a DaemonSet across all nodes |
| kube-prometheus stack | Prometheus, Grafana, AlertManager, node-exporter on all 6 nodes |
| Loki + Grafana Alloy | Log aggregation with pod log collection via Alloy |
| OpenTelemetry (OBI) | eBPF-based auto-instrumentation DaemonSet; traces service calls without code changes |
| CloudNativePG | PostgreSQL operator with barman-cloud continuous WAL archiving |
| csi-nfs + csi-smb | NFS/SMB CSI drivers backed by TrueNAS |
| GitHub Actions runners | Self-hosted runner controller (ARC) for homelab CI pipelines |
| kube-descheduler | Periodic pod rebalancing across nodes |

**Applications**

| App | Notes |
|---|---|
| Immich | Self-hosted photo management, 3 ML inference replicas with GPU acceleration |
| Home Assistant | Home automation |
| Plex | Media server |
| Factorio | Game server |
| Mumble | Self-hosted voice server |
| Catcrawl | Supermarket price scraper (personal project, runs CI via self-hosted runners) |
| Stirling PDF | Self-hosted PDF tooling |
| Zabbix | Infrastructure monitoring (server, web, Java gateway, agent on all nodes) |

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

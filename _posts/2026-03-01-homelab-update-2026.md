---
layout: post
title: "Homelab 2026: Rebuilding the Stack from Bare Metal Up"
tags: [Kubernetes, Homelab, Terraform, Ansible, eBPF]
gh-repo: Jayden-Lind/LINDS-Kubernetes
---

It's been a while since I last wrote about the homelab, and a lot has changed. What started as a few CentOS VMs running Docker containers has evolved into a fully declarative, IaC-managed stack across two physical sites. New hardware, a purpose-built Kubernetes OS, eBPF-powered networking, BGP routing, and everything managed as code. This post covers what changed, why each decision was made, and what I learned along the way.

---

## Hardware

### JD Site: Lenovo ThinkSystem SR655 (EPYC 7B13, 256GB RAM)

The HPE DL360 G9 had served well, but its age was showing. Memory-heavy workloads - databases, Kubernetes, anything with working sets that didn't fit in L3 cache - were sluggish. The dual-socket design meant workloads spread across two NUMA nodes experienced noticeable inter-socket latency, and the 2x Intel Xeon E5-2660 v4 (28 cores total) wasn't power-efficient.

I replaced it with a **Lenovo ThinkSystem SR655** running an AMD EPYC 7B13 (64 cores / 128 threads) and 256GB Samsung DDR4 ECC at 2933 MT/s. The jump in core count, L3 cache size, and memory bandwidth is significant - all workloads are faster, game servers sustain higher tick rates consistently, and the single-socket EPYC design means everything runs on a single NUMA domain with no cross-socket latency.

Storage is three ZFS pools:
- `NAS-SSD`: RAIDZ1 across 5x Samsung 870 EVO 4TB SSDs (18.2TB usable). NFS/iSCSI backing for Kubernetes PVs.
- `VM`: RAIDZ1 across 3x SSDs (1.62TB usable). VM disk storage.
- `HDD-20T`: Mirrored pair of 20TB Seagate enterprise HDDs. Cold and bulk storage.

**Learning:** The single-socket EPYC design eliminates cross-socket latency entirely. ZFS should've been the choice from day one - the CPU overhead on a 64-core EPYC is negligible, and transparent compression and checksumming for free is worth it.

### LINDS Site: Dell PowerEdge T630

The second site runs a Dell PowerEdge T630 with 2x Intel Xeon E5-2640 v4 (20 cores / 40 threads, dual-socket), 128GB RAM, and Proxmox VE 9.2.3. Storage is handled by the PERC H730 hardware RAID controller. It runs two Talos Kubernetes workers and a set of site-local VMs (VyOS, TrueNAS, domain controller, Plex).

The two sites are interconnected via site-to-site IPSec VPN, BGP peering at the VyOS layer, and a shared Kubernetes cluster that spans both.

---

## Proxmox VE: Replacing ESXi

VMware's post-Broadcom licensing changes made ESXi increasingly unviable for homelab use. I migrated both sites to **Proxmox VE**, which is Debian-based, runs a recent Linux kernel, and has excellent hardware support, flexible networking, and no licensing overhead.

**Challenges:** Without shared storage between the old and new hypervisors, every VM migration required a full snapshot, OVF export, import, validate, and decommission cycle. Time-consuming and downtime-heavy.

**Learning:** ZFS on Proxmox is a solid combination. The flexibility over hardware RAID is worth the CPU cost - checksumming and transparent compression run at negligible overhead on modern hardware.

---

## Talos Linux: A Purpose-Built Kubernetes OS

My Kubernetes nodes were previously running Ubuntu with Ansible managing `kubeadm` bootstrapping. It worked, but it was fragile - kernel updates would occasionally leave nodes in a broken state, and eBPF-dependent features were sensitive to kernel version changes.

I migrated to **[Talos Linux](https://www.talos.dev/)**, an OS built exclusively for running Kubernetes. There's no SSH, no package manager, no shell - the entire OS is managed through a declarative API via [LINDS-Terraform](https://github.com/Jayden-Lind/LINDS-Terraform).

The cluster currently runs **Talos v1.13.2** and **Kubernetes v1.36.0** across 6 nodes: one control plane and three workers at the JD site, two workers at the LINDS site. All nodes have been `Ready` continuously.

Every kernel parameter is set declaratively in Terraform. AMD (EPYC) and Intel (Broadwell) nodes get separate schematics with architecture-specific tuning:
- CPU vulnerability mitigations disabled (`mitigations=off`, spectre/meltdown variants)
- `transparent_hugepage=always`
- Governor set to `performance` via `amd_pstate=active` / `intel_pstate=active`
- BBR congestion control
- `nohz_full` and `rcu_nocbs` for reduced kernel interrupt overhead on worker CPUs
- Tuned TCP socket buffers and conntrack table sizes via sysctls

**Challenges:** No shell makes initial troubleshooting unintuitive. Diagnosing issues requires `talosctl` exclusively, which has a learning curve. Integrating Talos bootstrapping into Terraform took a few iterations.

**Learning:** A minimal, immutable, API-driven OS removes an entire class of configuration drift. The stability improvement over Ubuntu + kubeadm was immediate.

---

## ArgoCD and Helm: GitOps for the Cluster

I was previously managing Kubernetes workloads with raw manifests and ad-hoc scripts. Rebuilding after a cluster failure was slow and not reproducible. I adopted **[ArgoCD](https://argo-cd.readthedocs.io/en/stable/)** for GitOps-driven delivery and migrated all manifests to **[Helm charts](https://helm.sh/)**.

All workloads live in [LINDS-Kubernetes](https://github.com/Jayden-Lind/LINDS-Kubernetes) as ArgoCD `Application` manifests. Bootstrapping is a single script that initialises ArgoCD, after which it self-heals the cluster to the desired state. The full workload list, as of now:

| Category | Services |
|---|---|
| Home automation | Home Assistant |
| Media | Plex |
| Game servers | Factorio |
| Communication | Mumble |
| Photos | Immich (3 ML inference replicas, GPU-accelerated) |
| Dev tools | GitHub Actions self-hosted runners (ARC), Catcrawl |
| Utilities | Stirling PDF |
| Monitoring | Prometheus, Grafana, AlertManager, Loki, Grafana Alloy, Zabbix |
| Infrastructure | ArgoCD, cert-manager, Vault, external-secrets, external-dns, nginx-ingress, CloudNativePG |
| Observability | OpenTelemetry eBPF auto-instrumentation (OBI) on all nodes |

**Challenges:** Finding or building the right Helm chart for each service takes time. Getting every ArgoCD application to a healthy sync state during the initial migration required careful attention to resource ordering.

**Learning:** The GitOps model pays off when things break. Blowing up a namespace and letting ArgoCD reconcile it back in minutes removes a lot of operational stress.

---

## Cilium and eBPF: Replacing kube-proxy

The original cluster used Flannel for networking and kube-proxy for service routing. I trialled Calico in eBPF mode before ultimately switching to **[Cilium](https://cilium.io/)** when rebuilding on Talos. Cilium has first-class eBPF support, is the default CNI in several major managed Kubernetes offerings, and replaces kube-proxy entirely.

Currently running **Cilium 1.19** with:
- kube-proxy disabled; Cilium's eBPF datapath handles all service routing with O(1) kernel hash map lookups
- BGP control plane for LoadBalancer IP advertisement
- Hubble for real-time network flow observability
- Gateway API with ALPN and AppProtocol support

Why eBPF matters: traditional kube-proxy rewrites iptables rules for every service and endpoint, and each packet traverses a sequential chain that grows with cluster size. Cilium's eBPF datapath uses kernel-resident hash maps for O(1) lookups regardless of service count, with no netfilter traversal.

Cilium is deployed directly from Terraform via Helm immediately after the Talos cluster bootstraps. BGP configuration (CiliumBGPClusterConfig, CiliumBGPPeerConfig, CiliumBGPAdvertisement CRDs) is also applied from Terraform, which avoids manual post-bootstrap steps and keeps the full cluster state reproducible.

**Challenges:** Migrating from Calico to Cilium required a clean rebuild. Cilium's feature surface is large, and getting BGP peering configured correctly between Cilium and VyOS took a few iterations.

**Learning:** Cilium is a full networking platform, not just a CNI. Understanding how it replaces each layer of the traditional Kubernetes networking stack gave me a much better mental model of how production Kubernetes networking works at the kernel level.

---

## VyOS and BGP Peering with Kubernetes

I moved from OPNsense to **[VyOS](https://vyos.io/)** for routing. The primary driver was Ansible integration - OPNsense has no real automation story, whereas VyOS is structured around a CLI that maps cleanly to Ansible playbooks. VyOS's Linux-based forwarding plane is also measurably more efficient: CPU utilisation dropped from 20-30% on OPNsense to low single digits on VyOS under equivalent load.

The Kubernetes cluster [peers directly with VyOS over BGP](https://github.com/Jayden-Lind/LINDS-Terraform/blob/main/proxmox/talos.tf). Cilium's BGP control plane advertises `LoadBalancer` service IPs and pod CIDRs to VyOS, which redistributes them across the network:

- No MetalLB required; Cilium handles LoadBalancer IP advertisement natively
- LoadBalancer IPs are reachable anywhere on the network without static routes
- Node failure triggers automatic BGP route withdrawal; traffic reroutes instantly
- JD site peers at ASN 64512/64550, LINDS site at ASN 64513/64551
- `172.16.1.0/24` is the LoadBalancer IP pool advertised to both sites

**Challenges:** Getting ASN configuration and route filters aligned between Cilium and VyOS took a few iterations. VyOS's BGP config (FRR under the hood) is verbose, but behaves exactly as expected once the model is clear.

**Learning:** Running BGP at home makes production routing concepts concrete. Watching routes appear and disappear in real time - and seeing failover happen automatically - is the best way to understand path selection, route withdrawal, and graceful restart.

---

## OpenTelemetry eBPF Auto-Instrumentation

One of the more interesting additions is the [OpenTelemetry eBPF Instrumentation](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation) (OBI) running as a DaemonSet across all 6 nodes. It hooks into the kernel via eBPF to automatically generate traces and metrics for HTTP, gRPC, SQL, and other protocol traffic without any code changes or sidecar injection.

This is the same approach used in production observability platforms. Running it at home means every service in the cluster gets distributed tracing for free.

---

## Full IaC: Terraform, Ansible, and Packer

The previous setup was a patchwork of manually created VMs, partial Terraform coverage, and Puppet. I've replaced it with a clean three-tool stack:

- **[Packer](https://github.com/Jayden-Lind/LINDS-Terraform/tree/main/packer):** Builds golden VM images for Proxmox (Ubuntu 24.04, CentOS 9). Images are templated per site (JD and LINDS) and cloned by Terraform.
- **[Terraform](https://github.com/Jayden-Lind/LINDS-Terraform):** Provisions VMs, generates Talos node configuration, bootstraps the cluster, deploys Cilium via Helm, and wires up BGP via CRDs. State stored in MinIO (S3-compatible) on TrueNAS.
- **[Ansible](https://github.com/Jayden-Lind/LINDS-Ansible):** Post-provision configuration for non-Talos hosts. Full VyOS management (BGP, VPN, DNS, firewall), TrueNAS, Plex, Minecraft, and a common baseline role applied uniformly.

Everything is version-controlled. Rebuilding any component from scratch is a `terraform apply` and `ansible-playbook` away.

**Learning:** IaC pays for itself the first time something breaks. Being able to diff desired state against actual state, or tear down and redeploy a node cleanly, removes operational anxiety from the whole system.

---

## What's Next

- **Cluster API + Proxmox provider:** Allow Kubernetes to provision its own worker nodes on demand, removing the need for manual Terraform runs when scaling.
- **Tighter network segmentation:** VLAN separation between workload classes, enforced at both the VyOS layer and via Cilium network policy.
- **Hubble flow dashboards:** The data is being collected; now to build useful Grafana dashboards on top of Hubble's flow metrics.

---

This covers the major changes. In practice there have been dozens of smaller iterations, fixes, and experiments that didn't make the cut here. The homelab is a living system - something is always being tweaked, broken, and improved.

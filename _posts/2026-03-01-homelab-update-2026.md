---
layout: post
title: "Homelab 2026: Rebuilding the Stack from Bare Metal Up"
tags: [Kubernetes, Homelab, Terraform, Ansible, eBPF]
gh-repo: Jayden-Lind/LINDS-Kubernetes
---

It's been a while since I last wrote about the homelab, and a lot has changed. What started as a few CentOS VMs running Docker containers has evolved into a fully declarative, IaC-managed stack - new hardware, a purpose-built Kubernetes OS, eBPF-powered networking, BGP routing, and everything managed as code. This post covers what changed, why each decision was made, and what I learned along the way.

---

## New Hardware - Lenovo SR655 (EPYC 7B13, 256GB RAM)

The HPE DL360 G9 had served well, but its age was showing. Memory-heavy workloads - databases, Kubernetes, anything with working sets that didn't fit in L3 cache - were sluggish. The dual-socket design meant workloads spread across two NUMA nodes experienced noticeable inter-socket latency, and the 2× Intel Xeon E5-2660 v4 (28 cores total) wasn't exactly power-efficient.

I replaced it with a **Lenovo ThinkSystem SR655** running a 3rd-gen AMD EPYC (64 cores) and 256GB RAM. The jump in core count, L3 cache size, and memory bandwidth has been significant across the board - all workloads are faster and more responsive, and game servers now sustain higher tick rates consistently.

**Challenges:** The migration itself was straightforward - the main effort was safely moving data across.

**Learning:** The single-socket EPYC design eliminates cross-socket latency entirely. Further gains are possible by pinning VMs to a single EPYC chiplet to avoid cross-chiplet memory accesses.

---

## Proxmox VE - Replacing ESXi

VMware's post-Broadcom licensing changes made ESXi increasingly unviable for homelab use. I migrated to **Proxmox VE**, which is Debian-based, runs a recent Linux kernel, and has excellent hardware support, flexible networking, and no licensing overhead.

I also took the opportunity to ditch the hardware RAID controller in favour of **ZFS** directly on the host. ZFS gives me transparent compression, checksumming, and data integrity verification.

**Challenges:** Without shared storage between the old and new hypervisors, every VM migration required a full snapshot → OVF export → import → validate → decommission cycle. Time-consuming and downtime-heavy.

**Learning:** ZFS should've been the choice from day one. The CPU overhead on a 64-core EPYC is negligible, and getting data integrity and compression for free is a no-brainer. The Proxmox + ZFS combination is a win-win choice.

---

## Talos Linux - A Purpose-Built Kubernetes OS

My Kubernetes nodes were previously running Ubuntu, with Ansible managing `kubeadm` bootstrapping. It worked, but it was fragile - kernel updates would occasionally leave nodes in a broken state requiring manual intervention, and eBPF-dependent features were especially sensitive to kernel version changes.

I migrated to **[Talos Linux](https://www.talos.dev/)**, an OS built exclusively for running Kubernetes. There's no SSH, no package manager, no shell - the entire OS is managed through a declarative API, with every change applied via [LINDS-Terraform](https://github.com/Jayden-Lind/LINDS-Terraform).

**Challenges:** The lack of a shell makes initial troubleshooting unintuitive. You have to rely entirely on `talosctl` for diagnostics, which has a learning curve. Integrating Talos into Terraform for cluster bootstrapping also took some iteration to get right.

**Learning:** Not every workload needs a general-purpose OS. A minimal, immutable, API-driven OS removes an entire class of configuration drift and upgrade risk. The stability improvement over Ubuntu + kubeadm was immediate and obvious.

---

## ArgoCD & Helm - GitOps for the Cluster

I was previously managing Kubernetes workloads with raw manifests and some ad-hoc scripts. It worked, but rebuilding after a cluster failure was a slow, manual process and not reproducible. I adopted **[ArgoCD](https://argo-cd.readthedocs.io/en/stable/)** for GitOps-driven continuous delivery, and migrated all manifests to **[Helm charts](https://helm.sh/)** to handle templating and manage growing complexity.

**Challenges:** Finding or building the right Helm chart for each service took time. Getting every ArgoCD application to a healthy sync state - especially during the initial migration - required careful attention to resource ordering and dependencies.

**Learning:** The GitOps model pays dividends when things break. Being able to blow up a namespace and let ArgoCD reconcile it back to the desired state in minutes removes a huge amount of stress from cluster operations. It also makes experimentation much lower risk.

---

## Cilium & eBPF - Replacing kube-proxy

The original cluster used [Flannel](https://github.com/flannel-io/flannel) for networking and kube-proxy for service routing. With growing service counts, the IPTables-based service routing was becoming a bottleneck - every packet traverses a linear chain of rules, and that chain grows with every service and endpoint.

I trialled Calico in eBPF mode before ultimately switching to **[Cilium](https://cilium.io/)** when rebuilding on Talos. Cilium has first-class eBPF support, is the default CNI in several major managed Kubernetes offerings, and replaces kube-proxy entirely.

**Why eBPF matters:** Traditional kube-proxy rewrites iptables rules for every service and endpoint. With many services, each packet traverses a long sequential chain of rules. Cilium's eBPF datapath uses kernel-resident hash maps for O(1) service lookups regardless of cluster size - no netfilter traversal, no user-space involvement.

**Challenges:** Migrating from Calico to Cilium required a clean rebuild rather than an in-place swap. Cilium's feature surface is large, and getting BGP peering configured correctly between Cilium and VyOS took a few iterations.

**Learning:** Cilium isn't just a CNI - it's a full networking platform covering service routing, load balancing, network policy, and BGP. Understanding how it replaces each layer of the traditional Kubernetes networking stack deepened my understanding of how production Kubernetes networking actually works at the kernel level.

---

## VyOS & BGP Peering with Kubernetes

I moved from OPNsense to **[VyOS](https://vyos.io/)** for routing. The primary driver was Ansible integration - OPNsense has no real automation story, whereas VyOS is structured around a CLI that maps cleanly to Ansible playbooks. As a bonus, VyOS's Linux-based forwarding plane was measurably more efficient: CPU utilisation dropped from 20–30% on OPNsense to low single digits on VyOS under equivalent load.

The Kubernetes cluster [now peers directly with VyOS over BGP](https://github.com/Jayden-Lind/LINDS-Terraform/blob/main/proxmox/talos.tf#L362). Cilium's BGP control plane advertises `LoadBalancer` service IPs to VyOS, which redistributes them across the network. The result:

- No MetalLB required - Cilium handles load balancer IP advertisement natively
- LoadBalancer IPs are reachable anywhere on the network without static routes
- Node failure triggers automatic BGP route withdrawal and traffic reroutes instantly
- External DNAT routing only needs to touch LoadBalancer IPs - internal service resolution stays within the cluster

**Challenges:** Getting ASN configuration and route filters aligned between Cilium and VyOS took a few iterations. VyOS's BGP config (via FRR under the hood) is verbose, but behaves exactly as expected once the model is clear.

**Learning:** Running BGP at home makes production routing concepts concrete. Watching routes appear and disappear in real time - and seeing failover happen automatically - is the best way to understand path selection, route withdrawal, and graceful restart in practice.

---

## Kubernetes Service Consolidation

With a stable cluster and solid networking in place, I migrated a range of workloads off standalone VMs and Docker hosts:

| Category | Services |
|---|---|
| **Home automation** | Home Assistant, Mitsubishi heat pump integration |
| **Media** | Plex, *arr stack |
| **Game servers** | Factorio, Valheim, Satisfactory, Minecraft |
| **Dev** | GitHub Actions runners, PostgreSQL |
| **Infrastructure** | Internal DNS, monitoring, cert management, secrets management |

Consolidating onto Kubernetes reduced VM sprawl, centralised observability, and made updates consistent across all services via Helm and ArgoCD.

---

## Full IaC - Terraform, Ansible & Packer

The previous setup was a patchwork of manually created VMs, partial Terraform coverage, and Puppet. I've replaced this with a clean three-tool stack:

- **[Packer](https://github.com/Jayden-Lind/LINDS-Terraform/tree/main/packer)** - builds golden VM images for Proxmox
- **[Terraform](https://github.com/Jayden-Lind/LINDS-Terraform)** - provisions VMs, Talos node configuration, and cluster bootstrapping
- **[Ansible](https://github.com/Jayden-Lind/LINDS-Ansible)** - post-provision configuration for non-Talos VMs and VyOS management

Everything is version-controlled. Rebuilding any component from scratch is a `terraform apply` and `ansible-playbook` away.

**Challenges:** Ansible's syntax and best practices have a learning curve, particularly for idempotency and role structure.

**Learning:** IaC pays for itself the first time something breaks. Being able to diff desired state against actual state, or simply tear down and redeploy a node cleanly, removes operational anxiety and makes the whole system easier to reason about.

---


## What's Next

- **Cluster API + Proxmox provider** - Allow Kubernetes to provision its own worker nodes on demand, rather than requiring manual Terraform runs for scaling.
- **Tighter network segmentation** - VLAN separation between workload classes, enforced at both the VyOS layer and via Cilium network policy.
- **Observability improvements** - Expanding eBPF-based metrics and flow visibility with Hubble to get deeper insight into service-to-service traffic patterns.

---

This covers the major changes I can recall - realistically there have been dozens of smaller iterations, fixes, and experiments along the way that didn't make the cut here. The homelab is a living system; something is always being tweaked, broken, and improved.


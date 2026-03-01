---
layout: post
title: "Homelab Update 2026: Talos, Cilium, VyOS, and a New Beast of a Server"
tags: [Kubernetes, Homelab, Terraform, Ansible, eBPF]
gh-repo: Jayden-Lind/LINDS-Kubernetes
---

It's been a while since I last wrote about the homelab, and a lot has changed. What started as a few CentOS VMs running Docker containers has evolved into a fully declarative, IaC-managed stack with a proper BGP routing topology, eBPF-powered networking, and a serious hardware upgrade. This post covers everything that's changed, why I made each decision, and what I ran into along the way.

---

## New Hardware - Lenovo SR655 (EPYC 7B13, 256GB RAM)

The HPE DL360 G9 had served well, but it was starting to show some limitations and performance concerns. Performance woes with memory heavy workloads, like databases and running Kubernetes, not to mention the Dual CPU design, having latency impacts for workloads spread out across the 2 NUMA nodes. The 2x Intel Xeon E5-2660 v4 (28 cores total) was also a bit power inefficient. 

I replaced it with a **Lenovo ThinkSystem SR655** equipped with a 3rd gen AMD EPYC (64-core) and 256GB RAM. The jump in core count, L3 cache, memory bandwidth & channels has been significant, all workloads are significantly faster, more responsive, allowing my game servers to run at higher tick rates  more consistently.

**Challenges:** The only challenges I had when migrating to this new server was migrating data.

**Learning:** The per-core performance is excellent, but further optimisations can be done by ensuring VM's land only on a single AMD EPYC chiplet to avoid cross-chiplet accesses, which would result in higher latency.

---

## Proxmox VE - Replacing ESXi

With VMware's licensing changes making ESXi increasingly unviable for homelab use, I migrated to **Proxmox VE**. Since it is based on Debian, and uses KVM/QEMU, with a more recent version of the Linux Kernel, it has better hardware support, more modern features, and a much more flexible storage and networking stack compared to ESXi.

I also setup the new Lenovo EPYC server to use **ZFS**, instead of relying on the hardware RAID controller. ZFS gives me compression and data integrity checking. I also was running into some performance issues with the HPE RAID controller.

**Challenges:** Migrating live VMs off ESXi without a shared storage layer between hypervisors meant careful sequencing - snapshot, export OVF, import, validate, decommission. Doing this for every VM was time-consuming and lead to lots of downtime.

**Learning:** ZFS on Proxmox has been fantastic. The performance is excellent, I should've used ZFS from the start, instead of using the hardware RAID card. There is a slight CPU cost to ZFS, but on my EPYC 3rd Gen 64 core, it's negligible and the benefits of compression and data integrity are worth it.

---

## Talos Linux — Rethinking the Kubernetes OS

My Kubernetes nodes were previously running Ubuntu, with ansible managing the configuration of kubeadm bootstrapping. This was flakey and was causing issues. Especially with eBPF and kernel updates, which would cause nodes to go into a bad state and require manual intervention. This lead to a lot of downtime and frustration.

I decided to migrate to **[Talos Linux](https://www.talos.dev/)**, an OS purpose-built for running Kubernetes. There's no SSH, no package manager, no shell - the entire OS is configured through a declarative API and every change is applied via `talosctl` or through [LINDS-Terraform](https://github.com/Jayden-Lind/LINDS-Terraform).

**Challenges:** Difficult to troubleshoot at first, since you can't just SSH in and poke around. You have to rely on `talosctl` for everything, which has a learning curve. Also, the initial setup of the cluster with Talos was a bit more complex than kubeadm, especially with integrating it into Terraform.

**Learning:** I don't need to run everything on Ubuntu VM's. If there is a more specialised solution, like Talos for Kubernetes, it's worth the effort to migrate. The stability and security benefits of a minimal, immutable OS are significant, and the declarative configuration model fits well with my overall IaC approach.

---

## Migrating to ArgoCD and Helm charts for GitOps

I was originally using raw manifests and some bash scripts to provision my Kubernetes cluster, which worked but was a bit clunky. I wanted a more Kubernetes-native way to manage my cluster configuration, and after some research decided upon **[ArgoCD](https://argo-cd.readthedocs.io/en/stable/)**. Upon implementing ArgoCD, I also migrated all my Kubernetes manifests into **[Helm charts](https://helm.sh/)** to take advantage of templating and better manage complexity as the number of services grew.

**Challenges:** Migrating the services I currently had deployed to Helm was a long battle of trying to find a chart that already existed for the service I wanted to host. Another challenge was ensuring ArgoCD sync statuses were all green.

**Learning:** The GitOps workflow with ArgoCD has made it so much easier to rebuild my Kubernetes cluster when I break it. Allows me to test things and recover quicker.

---

## Cilium & eBPF — Replacing kube-proxy

The original cluster used [flannel](https://github.com/flannel-io/flannel) for networking and kube-proxy for service routing. In the effort of efficiency and performance, it didn't make sense to have another system daemon set running another pod, doing IPTables command, which is fine, but is not efficient for overall node CPU utilisation.

I initially tried Calico without eBPF, then turned on eBPF mode, and the performance was definitely noticable. Then when I switched to Talos, I decided to start fresh with **[Cilium](https://cilium.io/)** as the CNI plugin, which is the more common https://docs.cloud.google.com/kubernetes-engine/networking/docs network CNI in production environments, and has first class support for eBPF.

**Why eBPF matters here:** Traditional kube-proxy rewrites iptables rules for every service and endpoint. With hundreds of services, this becomes a long chain of sequential rule evaluations per packet. Cilium's eBPF programs use hash maps to do O(1) lookups regardless of cluster size, and because they run in kernel context, there's no netfilter overhead.

**Challenges:** I ran Calico in eBPF mode for a while before switching to Cilium, and while it was good, trying to get config parity between Calico and Cilium was a bit of a headache. Cilium's documentation is good, but the sheer number of features and options can be overwhelming at first. This became apparent with BGP Peering, which took a bit of trial and error to get right.

**Learning:** How configurable Cilium is, and how much of the Kubernetes networking stack it can replace. It's not just a CNI plugin - it can handle service routing, load balancing, network policies, and even BGP peering. The eBPF-based datapath is a game changer for performance and scalability. I now see why Cilium is the default CNI for many managed Kubernetes services and is widely adopted in production environments.

---

## VyOS & BGP Peering with Kubernetes

I moved from OPNsense to **[VyOS](https://vyos.io/)** for routing. VyOS is a network OS built for engineers - it's configured entirely through a structured CLI, integrates well with Ansible for automation, which was the main reason for picking it, as OPNSense's Ansible support is nonexistent.

Another reason for switching to VyOS was because it is Linux/Debian based, which I found was more performant, I was using single digit CPU percentage on VyOS, compared to 20-30% on OPNSense, which was a bit concerning.

The Kubernetes cluster (now peers)[https://github.com/Jayden-Lind/LINDS-Terraform/blob/main/proxmox/talos.tf#L362] directly with VyOS over BGP. Cilium's BGP control plane advertises service LoadBalancer IPs directly to VyOS, which then redistributes them into the rest of the network. This means:

- No separate MetalLB required
- Load balancer IPs are reachable from anywhere on the network without static routes
- Failover is automatic - if a node goes down, BGP withdraws its routes and traffic shifts
- I can use the Kubernetes native CoreDNS to just resolve service names to their ClusterIPs, and let BGP handle the routing. I only need to advertise the LoadBalancer IPs, for when I want to do DNAT routing from internet to a service.

**Challenges:** Getting the ASN configuration and route filters right between Cilium and VyOS took a few iterations. VyOS's BGP config is verbose but predictable once you understand the FRR underpinnings.

**Learning:** Running BGP at home is a great way to actually understand how it works in production. The concepts of route advertisement, path selection, and graceful restart become very concrete when you're watching routes appear and disappear in real time.

---

## Kubernetes Service Expansion

With a stable, well-networked Kubernetes cluster in place, I migrated a number of services that had been running as standalone Docker containers or directly on VMs:

- **Home automation** - Home Assistant
- **Media** - *arr stack, Plex
- **Game servers** - Factorio, Valheim, Satisfactory, Minecraft
- **Dev services** - Github Action Runners, Postgres
- **Infrastructure services** - internal DNS, monitoring, certificate management, secrets management

This saved storage space by not having separate VM's for each service, and also made it easier to manage and update these services through Helm charts and ArgoCD, while also making it easier to monitor as it's all in a central place.

---

## Full IaC - Terraform, Ansible & Packer

The previous setup was a mix of manually created VMs, some Terraform, and Puppet. I've consolidated this into a clean three-tool stack:

- **[Packer](https://github.com/Jayden-Lind/LINDS-Terraform/tree/main/packer)** - builds golden VM images for Proxmox (Ubuntu)
- **[Terraform](https://github.com/Jayden-Lind/LINDS-Terraform)** - provisions all VMs, Talos node config, and cluster bootstrapping
- **[Ansible](https://github.com/Jayden-Lind/LINDS-Ansible)** - post-provision configuration for non-Talos VMs and VyOS router management

Everything is version-controlled. Rebuilding any part of the stack from scratch is a `terraform apply` and a `ansible-playbook` command away.

**Challenges:** Writing Ansible playbooks was initially hard, but with Github Copilot, it became much easier to get the syntax right and follow best practices. This made it easier, as I knew what I wanted, but didn't have the expertise to make it happen well in Ansible.

**Learning:** The investment in IaC pays off immediately when something goes wrong. Being able to diff the current state against the desired state, or simply tear down and redeploy a node, removes a huge amount of operational anxiety.

---

## Future Plans

- **Cluster autoscaling / VM autoprovisioning** — Explore Cluster API with the Proxmox provider to allow Kubernetes to provision its own nodes on demand.
- **Network segmentation** — Tighter VLAN separation between workload classes, enforced at the VyOS layer and with Cilium network policy.

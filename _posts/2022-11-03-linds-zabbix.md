---
layout: post
title: Monitoring homelab with Zabbix
tags: [zabbix, homelab]
gh-repo: Jayden-Lind/LINDS-Kubernetes
---

![image](/img/2022/11/zabbix.png)

# Introduction

The best way to have visbility on what is going on in your homelab is to have monitoring over everything from Networking, Storage, and Compute hosts. To do this, I have decided to use Zabbix in HA on my Kubernetes cluster, while integrating it with my PostgreSQL HA cluster to ensure ultimate uptime of my monitoring solution.

## Architecture

Below is a simple diagram showing the physical infrastructure backing this Zabbix deployment.

![image](/img/2022/11/kube-zabbix.png)

## Kubernetes

To move this to Kubernetes, ideally we would want a PostgreSQL cluster to store everything in. We can achieve this by using a PostgreSQL operator in Kubernetes, which automates provisioning StatefulSets of databases, which automates the High Availability by switching the Kubernetes service to the master node.

1. PostgreSQL HA cluster using [Zalando PostgreSQL Operator](https://github.com/zalando/postgres-operator)
2. Zabbix Server in HA with [LINDS-Kubernetes/zabbix](https://github.com/Jayden-Lind/LINDS-Kubernetes/tree/master/zabbix)
3. [TrueNAS](https://www.truenas.com/) Host to host the PostgreSQL data.

### Monitored objects

1. 2x Core switches
2. 5x Wireless AP's
3. Physical Host hardware (HPE and Dell)
4. [VMware ESXi](https://www.vmware.com/au/products/esxi-and-esx.html) Hypervisor OS
5. 2x [TrueNAS](https://www.truenas.com/) VM
6. 2X [OPNSense](https://opnsense.org/) VM

### Alerting

To receive alerting, I've set up Discord webhooks as well as [ZBX Viewer](https://zbx.vovanys.com/) to receive any notifications on my phone if there is any alerts.

### Screenshot

#### Dashboard

![image](/img/2022/11/zabbix-1.png)

#### Hosts

![image](/img/2022/11/zabbix-1.png)
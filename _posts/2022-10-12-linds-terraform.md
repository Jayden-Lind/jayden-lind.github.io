---
layout: post
title: Implementing IaaC (Terraform)
tags: [terraform, homelab]
gh-repo: Jayden-Lind/LINDS-Terraform
---

# Introduction

My entire homelab has been very adhoc, with VM's in ESXi just created and then installed from a installer ISO. After working more with Kubernetes and AWS, seeing how nice it is to have easily reproducible infrastructure, and automate deployment/updates, I decided to implement Terraform into my vSphere infrastructure, and use [Puppet](https://github.com/Jayden-Lind/LINDS-Puppet) to provision the VM's to the way I want them.

## Tooling

### Packer

Using [vsphere-iso](https://www.packer.io/plugins/builders/vsphere/vsphere-iso), I can create a CentOS 9 VM template for me to later clone to other VM's. Writing this in a [pkr file](https://github.com/Jayden-Lind/LINDS-Terraform/blob/main/packer/vsphere_centos9_stream.pkr.hcl) allows me to easily rerun and create reproducible images. It just requires having the latest CentOS 9 iso present.

### Terraform Provider

The [vSphere Terraform Provider](https://registry.terraform.io/providers/hashicorp/vsphere/2.2.0) allows me to create, modify and destroy various resources in a vSphere environment.

Utilising this I have defined my

- [Datastores](https://github.com/Jayden-Lind/LINDS-Terraform/blob/main/datastore.tf)
- [Networks](https://github.com/Jayden-Lind/LINDS-Terraform/blob/main/host_network.tf)
- More specifically VM's on my non-cluster ESXi hosts [jd-esxi](https://github.com/Jayden-Lind/LINDS-Terraform/blob/main/jd-vm.tf) and [linds-esxi](https://github.com/Jayden-Lind/LINDS-Terraform/blob/main/linds-vm.tf)

I imported most of these resources into the active state, then modified as need be.

## State

With Terraform, you need to keep track of your state. To achieve this in reliable way, I have stored the state on a [NAS](https://github.com/Jayden-Lind/LINDS-Terraform/blob/main/versions.tf#L10) that is then rsynced to an offsite NAS.


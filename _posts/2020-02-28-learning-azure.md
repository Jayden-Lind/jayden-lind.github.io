---
layout: post
title: Learning Azure
#subtitle: Each post also has a subtitle
tags: [homelab]
#comments: true
---

<p>I recently discovered Windows Admin Centre and saw the integrations with Azure in it. This made me want to learn Azure, as definitely the industry is heading towards the "Cloud".</p>

<h2></h2>

<p> After registering you're presented with this</p>

![image](/img/image-1.png)

<p>First thing you need to do is create a resource group.</p>

![image](/img/image-2.png)

<p>After creating a Resource Group, you can obviously create a Resource.</p>

![image](/img/image-3.png)

<p>The amount of quick start resources is amazing, but what I want to test out is integration with a Server 2016/2019 VM that is hosted in Azure.</p>

![image](/img/image-4.png)

![image](/img/image-5.png)

<p>After creating the VM and RDP'ing into it and verifying it's all working, I set out to attach the VM to my Hyper-V host to manage and learn from. </p>

<p>First I had to link my Azure instance to my WAC (Windows Admin Center) instance. This was not hard, as all I had to do was go to Settings -&gt; Azure, and link the account. Once the account was linked I had to grant permissions to WAC for Azure.</p>

<p>As you can see below, there is an option in the later versions of WAC to create a Azure Network Adapter.</p>

![image](/img/image-6.png)

<p>Submitting the Azure Virtual Network Gateway to be created, took some time, as I first had to create the subnet that it was going to be set up in. Once that was done, the request was sent, and now just waiting on Azure to finish setting it up.</p>

![image](/img/image-7.png)

<p>Once that is created, you will see in your "All Resources" a Virtual network gateway.</p>

![image](/img/image-8.png)

<p>I was under the impression that the setup of the VPN gateway was automatic through the WAC, but it doesn't look like it, so I started setting it up manually.  First I had to go to Point-to-site configuration and download the VPN client and install it on my Hyper-V host.</p>

<p>Once installed on my Hyper-V Host, I can see the VNET adapter</p>

![image](/img/image-9.png)

<p>Attempting to Connect to the Virtual Network Adapter was failing due to a certificate issue. I tried installing the certificate, and did some further research to see what I was doing wrong. I needed to set up a site to site VPN but at the moment, I don't want to do that, as I don't want to mess with my current networking config.</p>

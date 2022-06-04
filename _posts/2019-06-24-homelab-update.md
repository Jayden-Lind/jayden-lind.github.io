---
layout: post
title: Homelab Update 10/06/19
#subtitle: Excerpt from Soulshaping by Jeff Brown
#cover-img: /assets/img/path.jpg
#thumbnail-img: /assets/img/thumb.png
tags: [homelab]
---

<p>Below is a picture of my current setup. The HP N54L was being the main storage for my network, and only had a single GBit Ethernet connection between it, and the Dell R710.</p>

![image](/img/LINDs-Network-1.png)

<p>Since the R710 only had a 4 Drive back-plane installed, I wasn't able to move all 4 physical drives from the N54L to the R710. I purchased the back-plane upgrade part, and also purchased the extra SAS cable to use all 6 ports on the back-plane.</p>

<h2>Updated Diagram</h2>

![image](/img/LINDs-Network-7.png)

<p>After moving the disks to the R710, a big increase in performance was seen, mainly due to the Perc H700 RAID controller. The H700 allows full 6Gb/s interface to the drives, while the N54L only had 3Gb/s. Combined with the LACP/LAGG set up, I can now have 2 computers accessing the "NAS" at full gigabit speeds.</p>

<p></p>
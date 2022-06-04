---
layout: post
title: Changing Domain Name
#subtitle: Excerpt from Soulshaping by Jeff Brown
#cover-img: /assets/img/path.jpg
#thumbnail-img: /assets/img/thumb.png
tags: [homelab]
---

<p>When I first created my homelab ennvironment, I didn't fully know what I was doing. But that's the reason for a homelab right?<br>One of the first things I got wrong when building a domain was the actual forest name being wrong. The domain UPN suffix is linds.local and the domain is LINDS-SERVER, and I wish to change it to linds.com.au and LINDS.</p>

![image](/img/2019/07/image.png)


<ol><li>First is to create the zone of the domain, so I will create a new primary zone, and I wil; have it be an AD integrated zone</li></ol>

![image](/img/2019/07/image-1.png)

<p>2. After you have created the primary zone, you will want to open a administrative PowerShell/CMD prompt, and run the following command.<br> <strong><em>rendom /list</em></strong><br>(DO NOT CLOSE THIS POWERSHELL/CMD PROMPT)</p>

![image](/img/2019/07/image-2.png)

<p>3. After running rendom /list, you will see it's created a file in your current working directory, named Domainlist.xml. Open this file.<br></p>

![image](/img/2019/07/image-3.png)

<p>4. Edit the DNSname attribute to what you wish to change it to, for example from "DomainDnzZones.linds.local" to DomainDnsZones.linds.com.au". Once finished, save the file and close Notepad.</p>
![image](/img/2019/07/image-4.png)


<p>5. Return back to the PowerShell prompt and run<br> <strong><em>rendom /showforest</em></strong><em> </em><br>You should see at the bottom, "This operations completed successfully."<br>This operations parses the Domainlist.xml file for any changes, and shows the changes. Below you can see that it's detected the changes from LINDS.LOCAL, to linds.com.au.</p>

![image](/img/2019/07/image-5.png)

<p>6. Once you are happy, run the command<br><strong><em>rendom /upload</em></strong> <br>then run<br><strong><em>rendom /prepare</em></strong></p>

<p><br>After running "rendom /prepare", I ran into an issue.<br></p>

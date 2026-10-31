---
layout: page
title: "Porthole Support"
permalink: /porthole/support/
sitemap: false
render_with_liquid: false
---

Porthole is an app for iPhone and iPad for browsing and managing Kubernetes clusters, made by
LINDS.

## Getting in touch

Email **jayden@linds.com.au**. Porthole is a spare-time project, so expect a reply within a few days
rather than a few hours.

It helps to include:

- the version, from Settings → About in the app
- your device and its iOS or iPadOS version
- what you did, what you expected, and what happened instead, with the exact error message
- the Kubernetes version and distribution, if it is about a cluster (for example k3s 1.36,
  Talos or kubeadm)

**Never send a kubeconfig, a token, a key or a password**, and blank out server addresses you
would rather keep private. Nobody needs them to help you.

## Security problems

Please email jayden@linds.com.au rather than reporting a security problem in public. The ones that
matter most are credentials ending up anywhere but the keychain, a server being trusted when its
certificate shouldn't be, a change reaching a cluster marked read-only, and the app lock being
bypassed.

## Common questions

### Can I try Porthole without a cluster?

Yes. On the first screen tap **Try the Demo Cluster**, or find it under **+ → Add Cluster**. It
is a simulated cluster with sample apps that runs inside Porthole, so it needs no account and no
network. Change anything you like; to put it back, touch and hold **Demo Cluster** in the cluster
list and choose **Reset Demo Cluster**.

### How do I add my cluster?

Porthole needs a kubeconfig that carries its credentials inline. On your computer, run:

```sh
kubectl config view --raw --flatten --minify
```

Get the output onto your iPhone or iPad (Universal Clipboard, or AirDrop it to Files), then
choose **+ → Add Cluster → Kubeconfig**. It contains credentials: treat it like a password and
delete any copies afterwards.

You can also add a cluster by hand with **Add Cluster → Manual**: the server's address and a
service account token.

### Which kinds of sign-in work?

Client certificates (RSA, or EC P-256, P-384 and P-521), bearer tokens and basic auth.

Kubeconfigs that sign in by running a program aren't supported. That covers anything that needs a
cloud provider's command-line tool or another credential plugin, such as `aws eks get-token`,
`kubelogin` or `gke-gcloud-auth-plugin`, and the older auth providers. They run on your computer,
which iOS doesn't allow, so Porthole lists such a context but can't add it. For those clusters,
use a kubeconfig with a token or a client certificate instead: for example, create a
ServiceAccount and use its token.

### Porthole can't connect to a server on my network

The first time Porthole reaches a server on your local network, iOS asks for permission. If the
first attempt failed while that question was on screen, tap **Try Again**. If you answered Don't
Allow, turn on **Settings → Privacy & Security → Local Network → Porthole**.

### It says the server's certificate isn't trusted

Porthole checks the server against the certificate authority in your kubeconfig. If the cluster's
certificate was replaced, or the kubeconfig came from a different cluster, export it again.

### My port forward stopped

iOS suspends apps shortly after they leave the screen, and a port forward stops with Porthole.
Use Porthole's own browser to open what you forwarded, or on iPad put the other app beside
Porthole.

### Why can't I change anything in a cluster?

It may be marked read-only. Porthole then offers nothing that could change the cluster and
refuses to send anything but reads. Turn it off by editing the cluster. If it isn't read-only,
your credentials may not allow the change; the cluster's own access rules decide that.

### How do I remove my data?

Swipe a cluster in the list and choose **Delete** to remove it and its credentials. iOS can keep
an app's keychain items after the app is deleted, so delete your clusters first if you are
removing Porthole. If you install it again, it first removes anything an earlier installation
left in the keychain. The [privacy policy](https://jayden-lind.github.io/porthole/privacy/) has the details.

## Privacy

Porthole collects nothing: no accounts, analytics, advertising or tracking, and your credentials
stay in the keychain on your device. Read the [privacy policy](https://jayden-lind.github.io/porthole/privacy/).

Kubernetes is a registered trademark of The Linux Foundation. Porthole is not affiliated with or
endorsed by The Linux Foundation or the Kubernetes project.

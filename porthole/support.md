---
layout: page
title: "Porthole Support"
permalink: /porthole/support/
sitemap: false
render_with_liquid: false
---

Porthole is an app for iPhone and iPad for browsing and managing Kubernetes clusters, made by
LINDS. Porthole 1.1 needs iOS 26 or iPadOS 26 or later.

## Getting in touch

Email **jayden@linds.com.au**. Porthole is a spare-time project, so expect a reply within a few days
rather than a few hours.

It helps to include:

- the version, from Settings → About in the app
- your device and its iOS or iPadOS version
- what you did, what you expected, and what happened instead, with the exact error message
- the Kubernetes version and distribution, if it is about a cluster (for example k3s 1.36,
  Talos, kubeadm or Amazon EKS), and the versions of Argo CD, Flux or cert-manager if it is
  about them

**Never send a kubeconfig, a token, a key or a password**, and blank out server addresses and
AWS account numbers you would rather keep private. Nobody needs them to help you.

## Security problems

Please email jayden@linds.com.au rather than reporting a security problem in public. The ones that
matter most are credentials ending up anywhere but the keychain, or being sent anywhere but the
cluster or the AWS service they belong to, a server being trusted when its certificate
shouldn't be, a change reaching a cluster marked read-only, and the app lock being bypassed,
whether in the app or through Siri.

## Common questions

### Can I try Porthole without a cluster?

Yes. On the first screen tap **Try the Demo Cluster**, or find it under **+ → Add Cluster**. It
is a simulated cluster with sample apps that runs inside Porthole, so it needs no account and no
network. It has Argo CD Applications, Flux objects and cert-manager certificates too. Change
anything you like; to put it back, touch and hold **Demo Cluster** in the cluster list and
choose **Reset Demo Data…**. The same button is in Settings, under Demo Cluster, beside a
**Read-only** switch that shows the demo as Porthole shows any cluster marked read-only.

### Which iOS does Porthole need?

Porthole 1.1 needs iOS 26 or iPadOS 26 or later. On an iPhone or iPad that can't run it, the App
Store offers Porthole 1.0, the last version for iOS 17 to 25.

### How do I add my cluster?

Porthole needs a kubeconfig that carries its credentials inline. On your computer, run:

```sh
kubectl config view --raw --flatten --minify
```

Get the output onto your iPhone or iPad (Universal Clipboard, or AirDrop it to Files), then
choose **+ → Add Cluster → Import a Kubeconfig**. It contains credentials: treat it like a
password and delete any copies afterwards.

You can also add a cluster by hand with **Add Cluster → Enter Manually**: the server's address
and a service account token. Amazon EKS clusters can also be found for you: see below.

### Which kinds of sign-in work?

- Client certificates (RSA, or EC P-256, P-384 and P-521), bearer tokens and basic auth.
- **Amazon EKS**, signing in to AWS with **AWS IAM Identity Center** or an **IAM access key**, and
  taking on an IAM role if the cluster needs one. A kubeconfig made by `aws eks update-kubeconfig`
  imports as it is, and so does one that runs `aws-iam-authenticator`.

Other kubeconfigs that sign in by running a program aren't supported. That covers anything that
needs another cloud provider's command-line tool or credential plugin, such as `kubelogin` or
`gke-gcloud-auth-plugin`, and the older auth providers. They run on your computer, which iOS
doesn't allow, so Porthole lists such a context but can't add it. For those clusters, use a
kubeconfig with a token or a client certificate instead: for example, create a ServiceAccount and
use its token.

### How do I add an Amazon EKS cluster?

Choose **+ → Add Cluster → Amazon EKS**, then sign in to AWS in one of two ways:

- **Sign In with IAM Identity Center** (recommended). Enter your AWS access portal's start URL,
  which your administrator can give you, and the region your organisation's IAM Identity Center
  is in if Porthole can't tell it from the address. Porthole shows a code and opens AWS's page:
  check that the page shows the same code, sign in there and allow it. Then choose an account and
  a role.
- **Add an Access Key**: an IAM user's access key ID and secret. Under **Assume a Role** you can
  have Porthole take on a role first, with an external ID if the role needs one.

Porthole then looks for clusters (see the next question). Choose the ones you want and tap
**Add**. Finding clusters needs `eks:ListClusters` and `eks:DescribeCluster`; reaching one needs
an EKS access entry, or an `aws-auth` mapping, for your identity on that cluster. A cluster
whose API server is private can only be reached from inside its VPC, for example over a VPN, and
Porthole says so.

A kubeconfig from `aws eks update-kubeconfig` works too. Import it, and choose the AWS sign-in
it should use: one with the same name as the kubeconfig's AWS profile is chosen for you. If the
kubeconfig carries access keys of its own, **Save These Keys as an AWS Sign-In** keeps them in
the keychain. A context Porthole can't use says why, for example one that needs a web identity
token file.

Your AWS sign-ins are in **Settings → AWS Sign-Ins**, where you can rename them, sign in again,
sign out or delete them. One sign-in can serve several clusters.

### Which regions does Porthole look in?

First one region: that of a cluster already using the sign-in, or else your IAM Identity
Center's own region, or else that of an EKS cluster you have already added. Choose another under
**Region**, or **All Regions**. If the region has no clusters, **Search All Regions** asks every
region the sign-in's partition has (AWS, AWS GovCloud (US) or AWS China) and lists those with
clusters. Opt-in regions your account hasn't turned on don't answer; Porthole names them under
the results rather than treating them as errors.

Your IAM Identity Center's region is where your organisation set it up. Your clusters can be in
any region.

### The cluster didn't accept my AWS sign-in

Porthole shows the identity the cluster refused, as an ARN you can copy. Under **For Your
Administrator** it gives the two AWS CLI commands that let that identity in: an EKS access entry
and a read-only access policy. For an IAM Identity Center role, it names the role, and
**Open in IAM Console** shows the role's page, where its ARN is. Once access has been given, tap
**Try Again**. If you have more than one AWS sign-in, **Choose Another Sign-In…** tries a
different one.

### Signing in with IAM Identity Center didn't work

- **The code expired.** A code lasts ten minutes. Tap **Start Again** for a new one.
- **"Check that the region is your IAM Identity Center's."** The start URL's IAM Identity Center
  is in another region. Choose the one your organisation set it up in.
- **The browser didn't open.** Tap **Open in Safari** and confirm the code there.

### How do I sign out of AWS?

Settings → AWS Sign-Ins → the sign-in. **Sign Out** (IAM Identity Center) deletes its tokens
from this device and ends your session with AWS; clusters that use it ask you to sign in
again. **Delete Sign-In** removes it altogether, an access key included. An access key stays
valid in AWS until you deactivate it in IAM.

### Where are my Argo CD Applications?

On the cluster's home screen, under **Applications**, and in Overview, which count how many are
failing (degraded, say), need a look (out of sync, say), are progressing and are healthy. Both
open every namespace's Applications. Each row shows its sync or health status, whichever needs a
look, and **Problems Only** narrows the list to those in trouble.

An Application's page shows its sync and health, its source and destination, its last sync and
history, the objects it manages (out of step first, each opening its own page) and its external
links. From **Actions** (the ⋯ button):

- **Refresh** and **Hard Refresh** ask Argo CD to compare the Application with its source again.
- **Sync…** opens a sheet that says what will happen before it happens, with **Prune** to delete
  what the source no longer has and **Dry Run** to change nothing and only report what a sync
  would do. It uses the Application's own sync options, and Argo CD records it as started by
  "porthole".

Porthole asks Argo CD for these through the Kubernetes API, so your cluster credentials decide
whether you may: they need to be allowed to patch Applications. Argo CD's own accounts and
project roles aren't involved.

### How do I reconcile or suspend a Flux object?

Find Kustomizations, HelmReleases and Flux's sources (GitRepository, OCIRepository,
HelmRepository, HelmChart and Bucket) by typing the kind, such as "kustomization", into the home
screen's search field, or under **All Resource Types**. Their pages show the Ready state and its
message, the source, the last applied revision, what they depend on and what they applied. From
**Actions**:

- **Reconcile** asks Flux to reconcile it now.
- **Reconcile with Source** fetches its source first, as `flux reconcile --with-source` does.
- **Suspend** stops Flux reconciling it until you **Resume** it.

### When do my certificates expire?

If cert-manager is installed, the cluster's home screen has a **Certificates** row, which says
what needs a look, such as "1 expires within 14 days, 1 failing". A certificate is a warning
when it expires within 14 days, and failing within 3 days or once it has expired; one that
cert-manager reports as not Ready counts as failing too. One whose renewal is more than an hour
overdue is a warning: cert-manager keeps a certificate Ready while its renewals fail, so this is
often the first sign. A Certificate's page says when it expires and when cert-manager will renew
it, marks a renewal that is overdue and points to its events, and links its issuer and Secret.
**Actions → Renew…** asks cert-manager to issue it again now, as `cmctl renew` does.

The page of any TLS Secret, with or without cert-manager, shows when its certificate expires,
who issued it and the names it covers. Porthole reads only the certificate, never the key.

### How do I open my apps in a browser?

The cluster's home screen has **Web Apps**: the addresses your Ingresses, Gateway API routes,
Traefik IngressRoutes and load balancers serve, and Argo CD's external links. The pages of those
objects, and of the Services and workloads behind them, list them under **Web Links** too. Tap
one to open it in Safari, or your default browser. Your device must be able to reach the
address, for example on your network or over a VPN. Wildcard addresses are listed but can't be
opened. In the demo cluster, a link opens its sample app in Porthole's own browser instead.

### How do I find an object when I don't know its type?

Type part of its name into the cluster home screen's search field, then tap **Search Everything
for "…"**, or press ⌘K with a keyboard. Porthole searches every type you are allowed to list, in
the namespace chosen at the top or in all of them, and shows the newest matches of each type.
`-l app=web` finds objects by label instead. Types you aren't allowed to list are skipped, and
Porthole says how many.

### Can I use Porthole with Siri or Shortcuts?

Yes, in English. Try "Check my cluster in Porthole" or "What's broken in Porthole"; Siri asks
which cluster. In the Shortcuts app, Porthole has Open Cluster, Show Problems, Open Kubernetes
Object, Cluster Health, Scale Workload and Restart Workload.

- **Cluster Health** says how many nodes are ready and pods healthy, and names the pods that
  aren't.
- **Show Problems** opens the cluster's unhealthy pods, in every namespace.
- **Scale Workload** and **Restart Workload** change nothing themselves: they open Porthole on the
  Scale sheet or the Restart question for you to confirm. A cluster marked read-only refuses them.

While the app lock is on, they say "Porthole is locked" and do nothing else. The demo cluster
can be chosen once it is in your cluster list.

### How do I choose Light or Dark?

**Settings → Appearance**: **System** follows the device, or choose **Light** or **Dark** for
Porthole alone. It changes every Porthole window at once. Shells always stay dark.

### Porthole can't connect to a server on my network

The first time Porthole reaches a server on your local network, iOS asks for permission. If the
first attempt failed while that question was on screen, tap **Try Again**. If you answered Don't
Allow, turn on **Settings → Privacy & Security → Local Network → Porthole**.

### It says the server's certificate isn't trusted

Porthole checks the server against the certificate authority in your kubeconfig, the one you
entered for the cluster, or for Amazon EKS the one AWS reports. If the cluster's certificate was
replaced, or the kubeconfig came from a different cluster, export it again.

### My port forward stopped

iOS suspends apps shortly after they leave the screen, and a port forward stops with Porthole.
Use Porthole's own browser to open what you forwarded, or on iPad put the other app beside
Porthole.

### Why can't I change anything in a cluster?

It may be marked read-only. Porthole then changes nothing in the cluster and opens no shells or
file transfers in it, though you can still browse it, read its logs and forward ports. Argo CD's
Refresh and Sync, Flux's Reconcile and Suspend, and Renew aren't offered, and Siri's Scale and
Restart are refused. Turn it off by editing the cluster. If it isn't read-only, your credentials
may not allow the change; the cluster's own access rules decide that.

### How do I remove my data?

Swipe a cluster in the list and choose **Delete** to remove it and its credentials. AWS sign-ins
can serve several clusters, so delete them in Settings → AWS Sign-Ins. iOS can keep an app's
keychain items after the app is deleted, so delete your clusters and AWS sign-ins first if you
are removing Porthole. If you install it again, it first removes anything an earlier
installation left in the keychain. The [privacy policy](https://jayden-lind.github.io/porthole/privacy/)
has the details.

## Privacy

Porthole collects nothing: no accounts, analytics, advertising or tracking, and your credentials
stay in the keychain on your device. Read the [privacy policy](https://jayden-lind.github.io/porthole/privacy/).

Kubernetes is a registered trademark of The Linux Foundation. Amazon EKS and AWS are trademarks
of Amazon.com, Inc. or its affiliates. Porthole is not affiliated with or endorsed by The Linux
Foundation, the Kubernetes, Argo CD, Flux or cert-manager projects, or Amazon.

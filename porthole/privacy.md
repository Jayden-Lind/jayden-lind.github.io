---
layout: page
title: "Porthole Privacy Policy"
permalink: /porthole/privacy/
sitemap: false
render_with_liquid: false
---

Last updated: 9 November 2026

Porthole is an app for iPhone and iPad for browsing and managing Kubernetes clusters. It is made
by LINDS, an independent developer ("I" below). This page explains what happens to your
information when you use it.

## In short

- **Porthole collects nothing.** I don't run any servers for it, and nothing you do in the app is
  sent to me.
- **No accounts, analytics, advertising or tracking.** The app contains no third-party code that
  collects data.
- **Your credentials stay on your device**, in the iOS keychain, and are only ever sent to the
  cluster they belong to or, for an Amazon EKS cluster, to Amazon Web Services.

## What Porthole keeps on your device

- **The clusters you add.** For each one: its name, the API server's address, the certificate
  authority to check that server against, a default namespace, whether you marked it read-only,
  and the credentials you gave it (a client certificate and key, a token, or a user name and
  password). These are kept in the iOS keychain, which encrypts them and only makes them
  available while your device is unlocked. They stay on this device: they aren't synced through
  iCloud Keychain and don't move to a new device.
- **Amazon Web Services (AWS) sign-ins**, if you reach an Amazon EKS cluster by signing in to
  AWS. For an access key: the key ID, its secret and, for temporary keys, the session token. For
  AWS IAM Identity Center: the start URL and region, the registration AWS gives Porthole on your
  device when you first sign in, and the tokens AWS issues when you sign in. For both: the name
  you give the sign-in and the identity AWS reports for it (its ARN, which includes your AWS
  account number). They are kept in the keychain in the same way. The short-lived credentials
  and cluster tokens Porthole makes from them are only ever kept in memory.
- **Settings**, such as the appearance you chose and whether the app lock is on, in the app's
  own preferences on the device.
- **The demo cluster.** "Try the Demo Cluster" starts a simulated cluster inside the app. Its
  sample data is made up, is kept in memory, and is discarded when you reset it or the app
  closes. It never uses the network.

Porthole reads a file from your device only when you pick one, for example a kubeconfig to
import or a file to upload into a container. Logs, files and manifests you save or share go
wherever you choose to send them. Porthole doesn't access your contacts, photos, location,
camera, microphone or health data.

## Who Porthole connects to

Porthole connects directly from your device to these, and only when you use them:

- **The Kubernetes API servers you add.** Your credentials for a cluster are sent only to that
  cluster's server. What you browse and change goes to and from it. If the server is on your
  local network, iOS asks your permission first.
- **Amazon Web Services**, only for an Amazon EKS cluster you sign in to with AWS: the AWS
  Security Token Service (STS), to check an access key and to take on a role you name; the
  Amazon EKS API, to find your clusters; and AWS IAM Identity Center, at the start URL and
  region you give it, if you sign in with it. If your start URL is your organisation's own
  address, Porthole asks that address where it leads, as the AWS command-line tool does, and
  sends it nothing else. The cluster itself checks each token Porthole sends it with STS.
- **AWS's sign-in page.** To sign in with IAM Identity Center you confirm a code on AWS's own
  web page, which iOS shows in its sign-in sheet. Porthole doesn't see what you type there.
- **Ports you forward.** A port you forward opens in Porthole's browser, which loads the page
  from your cluster through the forward.

These services are run by you, your organisation or Amazon. What they record, such as a
cluster's audit log or AWS CloudTrail, is governed by your arrangements with them and by their
privacy policies. Nothing goes through a server of mine; there isn't one.

## Web links and certificates

Porthole reads the web addresses that your cluster's Ingresses, routes and load balancers serve,
and the certificates in its cert-manager Certificates and TLS Secrets, from your cluster, as it
reads anything else there, to show them to you. For a TLS Secret it reads only the certificate,
to show when it expires, never the private key. When you open one of those addresses, Porthole
hands it to Safari, or to the browser you chose as your default, which loads it as it loads any
other page, under its own privacy policy. Porthole's own browser only ever opens a port you
forwarded.

## Siri and Shortcuts

Porthole's actions for Siri and the Shortcuts app (Open Cluster, Show Problems, Open Kubernetes
Object, Cluster Health, Scale Workload and Restart Workload) run in Porthole, on your device. To
answer one, Porthole reads from your cluster as it does when you open it. It keeps nothing for
them: the clusters and objects it offers are looked up when you ask, and nothing about your
clusters is stored outside the app. What you say to Siri, and what Siri shows or says in reply,
such as a cluster's name and how many of its pods are healthy, is handled by Apple under Apple's
privacy policy.

While Porthole's app lock is on, these actions read nothing from your clusters, name none of
them but the demo cluster, and ask you to open Porthole. Scale and Restart change nothing
themselves: they open Porthole on the change for you to confirm, and a cluster marked read-only
refuses them.

## Face ID and Touch ID

If you turn on the app lock, iOS checks your face, fingerprint or passcode. Porthole is only told
whether the check succeeded. It never sees biometric data.

## What Apple shares with me

Apple handles downloads from the App Store under its own privacy policy. If you have chosen to
share analytics with app developers (Settings → Privacy & Security → Analytics & Improvements),
Apple may show me crash reports and usage statistics in App Store Connect. They come from Apple,
not from Porthole, and they describe the app and the device, for example where a crash happened,
not your clusters or credentials.

## Removing your information

- To remove a cluster and its credentials, swipe it in the cluster list and choose **Delete**.
  An AWS sign-in can serve several clusters, so it stays until you delete it yourself.
- **AWS sign-ins** are in Settings → AWS Sign-Ins. **Sign Out** deletes an IAM Identity Center
  sign-in's tokens from this device and asks AWS to end the session; **Delete Sign-In** removes
  the sign-in altogether, an access key included. An access key stays valid in AWS until you
  deactivate it in IAM.
- Deleting the app removes its settings. iOS can keep an app's keychain items after the app is
  deleted, so delete your clusters and AWS sign-ins in Porthole first if you want to be sure
  their credentials are gone. If you install Porthole again, it first removes anything an
  earlier installation left in the keychain.

Because I don't hold any of your information, there is nothing for me to send you, correct or
delete on request. Everything Porthole keeps is on your device, under your control.

## Children

Porthole is a tool for people who run Kubernetes clusters. It isn't directed at children.

## Security

Credentials live only in the keychain. Porthole checks each server's certificate, against the
certificate authority you gave it for that cluster, or that AWS reports for an EKS cluster, when
there is one, unless you or your kubeconfig turn that check off for the cluster, which Porthole
then marks "TLS not verified". AWS credentials are sent only to AWS's own endpoints, never to an
address a kubeconfig names instead. Porthole changes nothing in a cluster marked read-only, and
opens no shells or file transfers in it. Port forwarding stays available, and what you do
through a forwarded port is up to the service behind it. If you find a security problem, please
email me at jayden@linds.com.au rather than reporting it publicly.

## Changes to this policy

If this policy changes, the new version will be posted on this page with a new date, before the
version of Porthole it applies to is released.

## Contact

LINDS, jayden@linds.com.au

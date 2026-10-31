---
layout: page
title: "Porthole Privacy Policy"
permalink: /porthole/privacy/
sitemap: false
render_with_liquid: false
---

Last updated: 1 November 2026

Porthole is an app for iPhone and iPad for browsing and managing Kubernetes clusters. It is made
by LINDS, an independent developer ("I" below). This page explains what happens to your
information when you use it.

## In short

- **Porthole collects nothing.** I don't run any servers for it, and nothing you do in the app is
  sent to me.
- **No accounts, analytics, advertising or tracking.** The app contains no third-party code that
  collects data.
- **Your credentials stay on your device**, in the iOS keychain, and are only ever sent to the
  cluster they belong to.

## What Porthole keeps on your device

- **The clusters you add.** For each one: its name, the API server's address, the certificate
  authority to check that server against, a default namespace, whether you marked it read-only,
  and the credentials you gave it (a client certificate and key, a token, or a user name and
  password). These are kept in the iOS keychain, which encrypts them and only makes them
  available while your device is unlocked. They stay on this device: they aren't synced through
  iCloud Keychain and don't move to a new device.
- **Settings**, such as whether the app lock is on, in the app's own preferences on the device.
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
- **Ports you forward.** A port you forward opens in Porthole's browser, which loads the page
  from your cluster through the forward.

These servers are run by you or your organisation. What they record, such as a cluster's audit
log, is governed by your arrangements with whoever runs them. Nothing goes through a server of
mine; there isn't one.

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
- Deleting the app removes its settings. iOS can keep an app's keychain items after the app is
  deleted, so delete your clusters in Porthole first if you want to be sure their credentials are
  gone. If you install Porthole again, it first removes anything an earlier installation left in
  the keychain.

Because I don't hold any of your information, there is nothing for me to send you, correct or
delete on request. Everything Porthole keeps is on your device, under your control.

## Children

Porthole is a tool for people who run Kubernetes clusters. It isn't directed at children.

## Security

Credentials live only in the keychain. Porthole checks each server's certificate, against the
certificate authority in your kubeconfig when it names one, unless the kubeconfig itself turns
that check off. A cluster marked read-only is sent nothing but reads. If you find a security
problem, please email me at jayden@linds.com.au rather than reporting it publicly.

## Changes to this policy

If this policy changes, the new version will be posted on this page with a new date, before the
version of Porthole it applies to is released.

## Contact

LINDS, jayden@linds.com.au

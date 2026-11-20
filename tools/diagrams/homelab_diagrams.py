#!/usr/bin/env python3
"""Draws the homelab diagrams as SVG, one light and one dark file for each.

    python3 tools/diagrams/homelab_diagrams.py            # writes img/2026/*.svg
    python3 tools/diagrams/homelab_diagrams.py --out DIR  # writes somewhere else

No dependencies. The facts are in FACTS and in the three draw_* functions:
change them there and run the script again. The files use only system fonts
and plain attributes (no CSS variables, no scripts), so they render the same
as an <img> on GitHub, in the Jekyll site and in a feed reader.
"""
import argparse
import math
import os
from xml.sax.saxutils import escape

# Read from the running systems on this date. Update both together.
FACTS = {
    "date": "20 Nov 2026",
    "talos": "1.14.6",
    "kubernetes": "1.37.2",
    "cilium": "1.20.5",
    "argocd": "3.6",
    "pve": "9.2",
    "apps": 37,
    "pods": 132,
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": {
        "bg": "#0d1117", "panel": "#151b23", "card": "#1c2430", "stroke": "#303a48",
        "text": "#e6edf3", "muted": "#9da9b6", "faint": "#6b7785",
        "blue": "#58a6ff", "violet": "#b694f6", "teal": "#3fc5b0",
        "amber": "#e3b341", "green": "#6fd17a", "grey": "#8b97a5",
        "tint": 0.14, "edge": 0.55,
    },
    "light": {
        "bg": "#ffffff", "panel": "#f6f8fa", "card": "#ffffff", "stroke": "#d0d7de",
        "text": "#1f2328", "muted": "#57606a", "faint": "#8c959f",
        "blue": "#0969da", "violet": "#8250df", "teal": "#0f7d70",
        "amber": "#9a6700", "green": "#1a7f37", "grey": "#6e7781",
        "tint": 0.08, "edge": 0.50,
    },
}

NARROW = set("iljtfr.,:;'|!()[]/ ·1I")
WIDE = set("mwMW@⇄→")


def text_width(s, size, bold=False, mono=False):
    """A safe estimate of the rendered width: system fonts differ, so it errs wide."""
    if mono:
        return len(s) * size * 0.615
    w = 0.0
    for ch in s:
        if ch in NARROW:
            w += 0.37
        elif ch in WIDE:
            w += 0.95
        elif ch.isupper():
            w += 0.72
        elif ch.isdigit():
            w += 0.64
        else:
            w += 0.62
    return w * size * (1.07 if bold else 1.0)


class Diagram:
    def __init__(self, width, height, theme, title, desc):
        self.w, self.h, self.t = width, height, THEMES[theme]
        self.title, self.desc = title, desc
        self.out = []

    def c(self, name):
        return self.t.get(name, name)

    # --- primitives -------------------------------------------------------
    def rect(self, x, y, w, h, fill="panel", stroke="stroke", rx=10, sw=1, dash=None,
             fill_opacity=None, stroke_opacity=None):
        a = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" fill="{self.c(fill)}"'
        if fill_opacity is not None:
            a += f' fill-opacity="{fill_opacity:g}"'
        if stroke:
            a += f' stroke="{self.c(stroke)}" stroke-width="{sw:g}"'
            if stroke_opacity is not None:
                a += f' stroke-opacity="{stroke_opacity:g}"'
            if dash:
                a += f' stroke-dasharray="{dash}"'
        self.out.append(a + "/>")

    def text(self, x, y, s, size=12.5, weight=400, color="text", anchor="start", mono=False,
             spacing=None):
        a = f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{self.c(color)}"'
        if weight != 400:
            a += f' font-weight="{weight}"'
        if anchor != "start":
            a += f' text-anchor="{anchor}"'
        if mono:
            a += f' font-family="{MONO}"'
        if spacing:
            a += f' letter-spacing="{spacing:g}"'
        self.out.append(f"{a}>{escape(s)}</text>")

    def line(self, pts, color="grey", sw=1.6, dash=None, arrows=""):
        """A polyline. arrows: 'e' at the end, 's' at the start, 'se' at both."""
        d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
        a = (f'<path d="{d}" fill="none" stroke="{self.c(color)}" stroke-width="{sw:g}"'
             ' stroke-linecap="round" stroke-linejoin="round"')
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.out.append(a + "/>")
        if "e" in arrows:
            self._head(pts[-2], pts[-1], color)
        if "s" in arrows:
            self._head(pts[1], pts[0], color)

    def _head(self, a, b, color, size=7):
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        p = [(b[0] - size * math.cos(ang + s * 0.45), b[1] - size * math.sin(ang + s * 0.45)) for s in (-1, 1)]
        tip = (b[0] + 1.5 * math.cos(ang), b[1] + 1.5 * math.sin(ang))
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (tip, p[0], p[1]))
        self.out.append(f'<polygon points="{pts}" fill="{self.c(color)}"/>')

    # --- parts ------------------------------------------------------------
    def heading(self, title, subtitle):
        self.text(24, 38, title, size=21, weight=700)
        self.text(24, 59, subtitle, size=12.5, color="muted")

    def label(self, x, y, s, color="faint", anchor="start"):
        """A small upper-case section label."""
        self.text(x, y, s.upper(), size=10.5, weight=700, color=color, spacing=0.9, anchor=anchor)

    def node(self, x, y, w, hue, title, lines=(), tag=None, mono=True, h=None):
        """A card with a coloured bar, a name and lines of detail. Returns its height."""
        h = h or 34 + 17 * len(lines) + (8 if lines else 2)
        self.rect(x, y, w, h, fill="card", rx=9)
        self.rect(x + 8, y + 9, 3.5, h - 18, fill=hue, stroke=None, rx=1.75)
        self.text(x + 21, y + 23, title, size=13.5, weight=650, mono=mono)
        if tag:
            self.text(x + w - 14, y + 23, tag, size=11.5, weight=600, color=hue, anchor="end")
        for i, s in enumerate(lines):
            self.text(x + 21, y + 42 + 17 * i, s, size=12, color="muted")
        return h

    def chip(self, x, y, s, hue, size=12, mono=False, width=None, h=24):
        """A rounded tag. Returns its width."""
        w = width or text_width(s, size, mono=mono) + 22
        self.rect(x, y, w, h, fill=hue, stroke=hue, rx=h / 2,
                  fill_opacity=self.t["tint"], stroke_opacity=self.t["edge"])
        self.text(x + w / 2, y + h / 2 + size * 0.35, s, size=size, weight=500, anchor="middle", mono=mono)
        return w

    def chips(self, x, y, max_w, items, hue):
        """Chips that wrap inside max_w. Returns the y of the bottom edge."""
        cx, cy = x, y
        for s in items:
            w = text_width(s, 12) + 22
            if cx > x and cx + w > x + max_w:
                cx, cy = x, cy + 32
            self.chip(cx, cy, s, hue, width=w)
            cx += w + 8
        return cy + 24

    def caption(self, cx, y, s, color="muted", size=11.5, weight=500, mono=False, bg="bg"):
        """Centred text on a patch of background, to sit on a line."""
        w = text_width(s, size, mono=mono, bold=weight > 500) + 12
        self.rect(cx - w / 2, y - size, w, size + 6, fill=bg, stroke=None, rx=4)
        self.text(cx, y, s, size=size, weight=weight, color=color, anchor="middle", mono=mono)

    def legend(self, y, items):
        x = 24
        for hue, s in items:
            self.rect(x, y - 9, 10, 10, fill=hue, stroke=None, rx=3)
            self.text(x + 16, y, s, size=11.5, color="muted")
            x += 16 + text_width(s, 11.5) + 22

    def svg(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" role="img" font-family="{SANS}">\n'
                f"<title>{escape(self.title)}</title>\n<desc>{escape(self.desc)}</desc>\n"
                f'<rect width="{self.w}" height="{self.h}" rx="14" fill="{self.c("bg")}"/>\n')
        return head + "\n".join(self.out) + "\n</svg>\n"


# --------------------------------------------------------------------------
def draw_network(theme):
    d = Diagram(960, 932, theme, "Homelab network",
                "Two sites, JD and LINDS. Each has a Debian router VM behind an NBN service. "
                "The routers are joined by an IPsec tunnel and exchange routes over BGP. "
                "Each site has a main LAN and several VLANs.")
    d.heading("Network", f"Two sites, one routed network. Read from the routers on {FACTS['date']}.")

    # Edge row
    d.node(24, 80, 262, "grey", "Cloudflare", ["Public DNS, dynamic DNS for each site"], mono=False)
    d.node(349, 80, 262, "grey", "Internet", ["IPv4 and IPv6 at both sites"], mono=False)
    d.node(674, 80, 262, "grey", "Remote devices", ["IKEv2 remote-access VPN into JD"], mono=False)
    d.line([(286, 109), (349, 109)], "grey")
    d.line([(674, 109), (611, 109)], "violet", dash="5 4", arrows="e")

    # WAN drops
    d.line([(480, 139), (480, 166), (210, 166), (210, 206)], "grey")
    d.line([(480, 166), (750, 166), (750, 206)], "grey")
    d.caption(318, 170, "NBN HFC")
    d.caption(642, 170, "NBN FTTP")

    # Routers
    d.label(24, 196, "Site JD")
    d.label(936, 196, "Site LINDS", anchor="end")
    rh = d.node(24, 206, 372, "blue", "jd-router-01", [
        "Debian 13 VM · nftables with a flowtable",
        "FRR BGP · strongSwan IPsec · WireGuard",
        "Unbound to Quad9 over TLS · Kea DHCP · chrony",
        "Suricata IDS + inline IPS · mDNS reflector · UPnP",
    ], tag="AS 64550")
    d.node(564, 206, 372, "blue", "linds-router-01", [
        "Debian 13 VM · nftables with a flowtable",
        "FRR BGP · strongSwan IPsec · WireGuard",
        "Unbound to Quad9 over TLS · Kea DHCP · chrony",
        "Suricata IDS · mDNS reflector · UPnP",
    ], tag="AS 64551")
    ry = 206 + rh / 2
    d.line([(402, ry), (558, ry)], "violet", sw=2, dash="6 4", arrows="se")
    d.text(480, ry - 26, "IPsec IKEv2", size=12.5, weight=650, anchor="middle")
    d.text(480, ry - 10, "route-based tunnel", size=11.5, color="muted", anchor="middle")
    d.text(480, ry + 20, "eBGP across it", size=11.5, color="muted", anchor="middle")
    d.text(480, ry + 36, "10.255.0.0/30", size=11.5, color="muted", anchor="middle", mono=True)

    # Site panels
    top = 206 + rh + 24
    jd = [
        ("LAN", "10.0.50.0/24", "Servers, desktops, Wi-Fi", "blue"),
        ("VLAN 52", "10.0.52.0/24", "IoT + UniFi devices · isolated", "blue"),
        ("VLAN 53", "10.0.53.0/24", "Kubernetes nodes · AS 64512", "teal"),
        ("VLAN 58", "10.0.58.0/24", "Media devices · VPN egress", "violet"),
        ("VLAN 51", "10.0.51.0/24", "Spare · VPN-only egress", "violet"),
        ("VLAN 99", "cellular modem", "Backup WAN · switched off", "grey"),
    ]
    linds = [
        ("LAN", "192.168.6.0/24", "Servers, desktops, Wi-Fi", "blue"),
        ("VLAN 300", "10.3.1.0/24", "Servers, Kubernetes · AS 64513", "teal"),
        ("VLAN 80", "10.0.80.0/24", "Management · APs, switch", "blue"),
        ("VLAN 110", "10.0.110.0/24", "Cameras", "blue"),
        ("VLAN 36", "10.0.36.0/24", "VPN-only egress", "violet"),
    ]
    jd_gear = [
        ("USW Enterprise 24 PoE + 8 PoE", "UniFi switches, SFP+ link between them"),
        ("2 × U7 Pro", "Wi-Fi 7 access points"),
        ("Cloud Key Gen2 Plus", "UniFi Network and Protect, cameras on VLAN 52"),
    ]
    linds_gear = [
        ("HPE OfficeConnect 1920S 24G PoE+", "linds-switch-01, the core switch"),
        ("EdgeRouter X SFP", "linds-switch-02, used only as a VLAN switch"),
        ("UniFi access points + Cloud Key", "Wi-Fi on the LAN, managed on VLAN 80"),
    ]
    ph = 36 + 34 * 6 + 14 + 26 + 3 * 67 + 6
    for x, lanes, gear, rx_ in ((24, jd, jd_gear, 210), (488, linds, linds_gear, 750)):
        d.line([(rx_, 206 + rh), (rx_, top)], "blue")
        d.rect(x, top, 448, ph)
        d.label(x + 16, top + 24, "Networks")
        y = top + 36
        for tag, net, what, hue in lanes:
            d.chip(x + 16, y, tag, hue, size=11.5, width=74)
            d.text(x + 102, y + 16.5, net, size=12, mono=True)
            d.text(x + 222, y + 16.5, what, size=12, color="muted")
            y += 34
        y = top + 36 + 34 * 6 + 14
        d.label(x + 16, y + 12, "Switching and Wi-Fi")
        y += 26
        for name, what in gear:
            d.node(x + 16, y, 416, "blue", name, [what], mono=False)
            y += 67

    # How the cluster shows up on the network
    y = top + ph + 16
    d.rect(24, y, 912, 76)
    d.rect(40, y + 12, 3.5, 52, fill="teal", stroke=None, rx=1.75)
    d.text(54, y + 27, "Kubernetes on the network", size=13, weight=650)
    d.text(54, y + 47, "Cilium announces the LoadBalancer pool 172.16.1.0/24 and the pod networks to each site's router over eBGP.",
           size=12, color="muted")
    d.text(54, y + 65, "The routers pass them across the tunnel, so a service address works from both sites and from the VPN.",
           size=12, color="muted")
    d.legend(y + 76 + 28, [("blue", "Routing and switching"), ("teal", "Kubernetes"),
                             ("violet", "VPN and tunnels"), ("grey", "Outside, or not in use")])
    d.h = y + 76 + 46
    return d


def draw_compute(theme):
    d = Diagram(960, 1016, theme, "Homelab compute and storage",
                "Two Proxmox hosts, one at each site, the guests on each, the storage pools, "
                "and the four paths that protect the data.")
    d.heading("Compute and storage",
              f"Two Proxmox VE {FACTS['pve']} hosts and everything they run. Read from the hosts on {FACTS['date']}.")

    jd_guests = [
        ("jd-router-01", "Debian 13 · router, firewall", "blue"),
        ("talos-cp", "Talos · control plane, etcd", "teal"),
        ("talos-worker-01 … 04", "Talos · 4 × 8 vCPU / 16 GB", "teal"),
        ("jd-dc-01", "Server 2025 · AD, DNS", "violet"),
        ("jd-fs-01", "Server 2025 · SMB, DFS-R", "violet"),
        ("jd-jump-01", "Ubuntu · IaC deploy runs", "violet"),
        ("jd-torrent-01", "qBittorrent", "violet"),
        ("jd-backup-01", "Weekly Backblaze run", "amber"),
        ("jd-s3-01 (LXC)", "versitygw · S3 object store", "amber"),
    ]
    linds_guests = [
        ("linds-router-01", "Debian 13 · router, firewall", "blue"),
        ("talos-linds-worker-01, 02", "Talos · 2 × 4 vCPU / 16 GB", "teal"),
        ("linds-dc, linds-dc2", "Server 2025 · AD, DNS, DFS-R", "violet"),
        ("linds-plex-01", "Plex", "violet"),
        ("linds-torrent-02", "qBittorrent on the VPN VLAN", "violet"),
        ("linds-truenas-01", "TrueNAS SCALE · ZFS replica", "amber"),
    ]
    jd_store = [
        ("VM · 1.6 TB", "SSD RAIDZ1", ["VM disks, 16 Kubernetes iSCSI volumes, NFS, S3 data"]),
        ("NAS-SSD · 18.2 TB", "SSD RAIDZ1", ["The file server's data disk (jd-fs-01)"]),
        ("HDD-20T · 20 TB", "HDD mirror", ["Media and bulk data over NFS"]),
    ]
    linds_store = [
        ("local-lvm · 0.9 TB", "LVM-thin", ["VM disks"]),
        ("NAS · 12 TB", "LVM-thin", ["The replicated NAS folders (linds-dc)"]),
        ("TrueNAS · 12 TB", "LVM-thin", ["Disks of linds-truenas-01, the replication target"]),
    ]
    hosts = [
        (24, "jd-proxmox-02", "JD", "Lenovo ThinkSystem SR655 · EPYC 7B13, 64 cores · 256 GB",
         "Kernel 7.3 · ZFS · also the cluster's iSCSI and NFS server", jd_guests, jd_store),
        (488, "linds-proxmox-01", "LINDS", "Dell PowerEdge T630 · 2 × Xeon E5-2640 v4 · 128 GB",
         "Kernel 7.0 · PERC H730 hardware RAID under LVM-thin", linds_guests, linds_store),
    ]
    top, rows = 80, 9
    ph = 78 + 26 + rows * 30 + 14 + 26 + 3 * 67 + 6
    for x, name, site, hw, sw_, guests, store in hosts:
        d.rect(x, top, 448, ph)
        d.text(x + 16, top + 30, name, size=16, weight=700, mono=True)
        d.label(x + 432, top + 28, f"Site {site}", anchor="end")
        d.text(x + 16, top + 50, hw, size=12, color="muted")
        d.text(x + 16, top + 67, sw_, size=12, color="muted")
        d.line([(x + 16, top + 80), (x + 432, top + 80)], "stroke", sw=1)
        d.label(x + 16, top + 100, "Guests")
        y = top + 110
        for g, what, hue in guests:
            d.rect(x + 18, y + 9, 9, 9, fill=hue, stroke=None, rx=3)
            d.text(x + 36, y + 18, g, size=12, weight=600, mono=True)
            d.text(x + 232, y + 18, what, size=12, color="muted")
            y += 30
        y = top + 110 + rows * 30 + 14
        d.label(x + 16, y + 12, "Storage")
        y += 26
        for pool, kind, what in store:
            d.node(x + 16, y, 416, "amber", pool, what, tag=kind)
            y += 67

    # Data protection
    y = top + ph + 16
    flows = [
        ("Daily ZFS snapshots at JD", "linds-truenas-01 at LINDS", "nightly ZFS replication", "e"),
        ("jd-fs-01, the NAS folders", "linds-dc at LINDS", "DFS-R, both ways", "se"),
        ("ZFS clone of the NAS disk", "Backblaze, off site", "weekly, by jd-backup-01", "e"),
        ("CloudNativePG databases", "jd-s3-01, S3", "WAL archive, base backups", "e"),
    ]
    d.rect(24, y, 912, 40 + len(flows) * 46 + 8)
    d.label(40, y + 24, "Data protection")
    fy = y + 36
    for src, dst, how, arrows in flows:
        d.node(40, fy, 290, "amber", src, mono=False, h=36)
        d.node(630, fy, 290, "amber", dst, mono=False, h=36)
        d.line([(338, fy + 18), (622, fy + 18)], "amber", arrows=arrows)
        d.caption(480, fy + 22, how, bg="panel")
        fy += 46
    yl = y + 40 + len(flows) * 46 + 8 + 28
    d.legend(yl, [("blue", "Router"), ("teal", "Kubernetes node"), ("violet", "Server"), ("amber", "Storage and backup")])
    d.h = yl + 18
    return d


def draw_kubernetes(theme):
    d = Diagram(960, 900, theme, "Homelab Kubernetes cluster",
                "One Talos Linux cluster of seven nodes across two sites. Cilium peers with each "
                "site's router over BGP. Platform layers and workloads are listed below the nodes.")
    d.heading("Kubernetes cluster",
              f"Talos {FACTS['talos']} · Kubernetes {FACTS['kubernetes']} · Cilium {FACTS['cilium']} · "
              f"7 nodes, {FACTS['pods']} pods. Read from the cluster on {FACTS['date']}.")

    top = 80
    # JD zone
    d.rect(24, top, 584, 148)
    d.label(40, top + 24, "Zone jd · on jd-proxmox-02 · 8 vCPU, 16 GB each")
    names = [("talos-cp", "control plane"), ("worker-01", "worker"), ("worker-02", "worker"),
             ("worker-03", "worker"), ("worker-04", "worker")]
    for i, (n, role) in enumerate(names):
        x = 40 + i * 112
        d.rect(x, top + 36, 104, 54, fill="card", rx=9)
        d.rect(x + 8, top + 45, 3.5, 36, fill="teal", stroke=None, rx=1.75)
        d.text(x + 20, top + 59, n, size=12, weight=650, mono=True)
        d.text(x + 20, top + 76, role, size=11.5, color="muted")
    d.chip(40, top + 106, "eBGP · AS 64512 to jd-router-01 (AS 64550)", "blue", width=552, h=26)

    # LINDS zone
    d.rect(624, top, 312, 148)
    d.label(640, top + 24, "Zone linds · 4 vCPU, 16 GB each")
    for i, n in enumerate(("linds-worker-01", "linds-worker-02")):
        x = 640 + i * 144
        d.rect(x, top + 36, 136, 54, fill="card", rx=9)
        d.rect(x + 8, top + 45, 3.5, 36, fill="teal", stroke=None, rx=1.75)
        d.text(x + 20, top + 59, n, size=12, weight=650, mono=True)
        d.text(x + 20, top + 76, "worker", size=11.5, color="muted")
    d.chip(640, top + 106, "eBGP · AS 64513 to linds-router-01", "blue", width=280, h=26)

    # Tunnel strip
    y = top + 148 + 22
    d.line([(60, y), (900, y)], "violet", sw=1.6, dash="6 4", arrows="se")
    d.caption(480, y + 4, "IPsec tunnel between the site routers · native routing, no overlay")

    layers = [
        ("Networking", "blue", ["Cilium eBPF, no kube-proxy", "BGP control plane", "LB-IPAM 172.16.1.0/24",
                                "Hubble", "Network policies", "CoreDNS at both sites"]),
        ("Ingress and identity", "blue", ["nginx-ingress · LAN and VPN", "nginx-ingress-mtls · internet, client certificates",
                                          "cert-manager", "external-dns · AD DNS", "external-dns · Cloudflare",
                                          "Keycloak · AD single sign-on", "Kyverno"]),
        ("GitOps and secrets", "teal", [f"Argo CD {FACTS['argocd']} · app of apps, {FACTS['apps']} applications",
                                        "Image Updater", "Renovate", "Vault", "External Secrets"]),
        ("Storage and data", "amber", ["democratic-csi · ZFS over iSCSI", "csi-driver-nfs", "csi-driver-smb",
                                       "CloudNativePG · PostgreSQL, 2 instances", "S3 backups on versitygw"]),
        ("Observability", "violet", ["Prometheus", "Alertmanager", "Grafana", "Loki",
                                     "Alloy · pod logs, syslog, Windows events",
                                     "IPMI, SNMP and Proxmox exporters", "descheduler", "metrics-server"]),
        ("Workloads", "green", ["Immich", "Home Assistant", "Plex", "Sonarr, Radarr, Bazarr", "Tautulli",
                                "Minecraft", "Factorio", "Mumble", "Stirling PDF", "catcrawl",
                                "GitHub Actions runners"]),
    ]
    y += 26
    for name, hue, items in layers:
        start = len(d.out)
        bottom = d.chips(224, y + 14, 696, items, hue)
        h = bottom - y + 14
        chips = d.out[start:]
        del d.out[start:]
        d.rect(24, y, 912, h)
        d.rect(40, y + 12, 3.5, h - 24, fill=hue, stroke=None, rx=1.75)
        d.text(54, y + 30, name, size=13, weight=650)
        d.out.extend(chips)
        y += h + 10
    d.text(24, y + 14, "Node names have the prefix talos-: talos-cp, talos-worker-01, talos-linds-worker-01.",
           size=11.5, color="muted")
    d.h = y + 34
    return d


DIAGRAMS = {"network": draw_network, "compute": draw_compute, "kubernetes": draw_kubernetes}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=os.path.join(here, "..", "..", "img", "2026"))
    ap.add_argument("--only", choices=sorted(DIAGRAMS), action="append")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for name in a.only or sorted(DIAGRAMS):
        for theme in THEMES:
            path = os.path.join(a.out, f"{name}-{theme}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(DIAGRAMS[name](theme).svg())
            print(os.path.relpath(path))


if __name__ == "__main__":
    main()

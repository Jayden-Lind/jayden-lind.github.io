---
layout: page
title: About Me
# Index page
---

# Jayden Lind

Software Engineer at [Atlassian](https://www.atlassian.com/) building Kubernetes platform infrastructure. Former SRE at NAB, former systems administrator at ICE (NYSE). Seven years from service desk to the team behind Jira and Confluence's microservice fabric.

📧 [jayden@linds.com.au](mailto:jayden@linds.com.au) &nbsp;|&nbsp; 💼 [linkedin.com/in/jayden-lind](https://www.linkedin.com/in/jayden-lind/) &nbsp;|&nbsp; 🐙 [github.com/Jayden-Lind](https://github.com/Jayden-Lind)

---

## Experience

### Software Engineer, Service to Service Fabric at Atlassian
**Aug 2023 to Present | Melbourne**

Building Atlassian's Kubernetes-based microservice orchestration platform. The work spans Envoy proxy, Istio service mesh, eBPF networking, and the routing infrastructure connecting hundreds of microservices across Atlassian's cell-based architecture.

- Contributed to the initial architecture and implementation of Atlassian's service fabric controller, a Kubernetes-based microservice orchestration platform running at company scale.
- Led Istio service mesh adoption and pod-to-pod routing for Atlassian's new cell-based Kubernetes architecture, serving Jira, Confluence, and their dependencies. Replaced a routing path where intra-cluster traffic traversed external load balancers unnecessarily, saving hundreds of thousands of dollars annually.
- Led HTTP/2 service-to-service communication and sharded routing via Envoy ext_proc, eliminating a central proxy bottleneck and delivering over $1M in annual cloud cost savings.
- Designed a HA failover solution for a mission-critical auth proxy service, improving resilience during platform and cloud incidents.
- Identified and resolved a critical Envoy DNS thread concurrency bug that had blocked Atlassian's org-wide Kubernetes migration for 2-3 weeks. Separately found an Envoy TLS inspector bug causing ~1-2% of requests to hang on 16KB payloads; acknowledged by Envoy maintainers and fixed in v1.36.0.
- Appointed Developer Productivity Lead: pipeline optimisations and test flakiness reduction achieved 25-50% faster builds and improved the team's "I can test my changes quickly and confidently" survey metric from 60% to 75%.
- Mentored an intern on a fleet-wide Envoy metrics migration, reducing CPU utilisation across Atlassian's microservices by 5-10%.
- Unblocked a stalled OpenTelemetry metrics migration, moving Atlassian off a legacy metrics pipeline to a vendor-neutral OTel standard and reducing backend lock-in.
- Prototyped multiple ShipIt projects: an AI-assisted performance review tool, network extension isolation mechanisms, and a Kubernetes-native alternative to serverless workflows.

### Senior Site Reliability Engineer at National Australia Bank
**Jan 2022 to Aug 2023 | Melbourne**

Primary escalation point for NAB's API platform across Kong and Axway gateway environments on AWS and Azure.

- Designed and owned an automated SSL certificate renewal system for NAB's API gateways, eliminating manual renewal and reducing operational risk.
- Built integration and unit tests for the legacy Axway API platform, and CI/CD pipelines for evidence capture, certificate management, and end-to-end deployment.
- Led incident response where NAB's API platform was incorrectly blamed for a Visa outage preventing customers from onboarding cards to Apple Pay; identified the root cause on Visa's side and unblocked resolution.
- Ran sprint planning and delivery for a team of 6 over a 2-month period without a manager.

### Senior Systems Administrator at Intercontinental Exchange (ICE:NYSE)
**Sep 2020 to Jan 2022 | Melbourne**

- Led Python automation projects eliminating manual hardware fault management: automated fault discovery, change request generation, and remediation, significantly reducing production incident resolution times.
- Resolved a complex integration failure between ICE Data Services and Vanguard on a Solaris system through deep diagnostic investigation.

### Systems Engineer at Tech Precision Pty Ltd
**Jan 2019 to Sep 2020 | Melbourne**

- Led consolidation of infrastructure onto VMware and Hyper-V hosts, and migrated Windows and Linux systems to Azure.
- Redesigned service desk workflows, reducing average open ticket count from 150 to 65.

---

## Skills

| | |
|---|---|
| **Languages** | Golang, Python, TypeScript, Bash |
| **Infrastructure** | Kubernetes, Terraform, Ansible, Packer, Docker, Proxmox, VyOS |
| **Cloud** | AWS, Azure, GCP |
| **Networking** | eBPF, BGP, Envoy, Istio, Linux internals, IPSec, NAT, performance tuning |
| **Security** | CTFs, reverse engineering, vulnerability analysis, pen testing |
| **Platforms** | Ubuntu, RHEL, Talos Linux, Windows |
| **Practices** | Observability, CI/CD, GitOps, IaC, incident response, performance optimisation |

---

## Projects

[**LINDS-Homelab**](https://jayden-lind.github.io/homelab/) - Bare-metal homelab fully managed as code. Proxmox, Talos Linux, Cilium eBPF, BGP peering, IPSec VPN.

[**LINDS-Terraform**](https://github.com/Jayden-Lind/LINDS-Terraform) / [**LINDS-Ansible**](https://github.com/Jayden-Lind/LINDS-Ansible) / [**LINDS-Kubernetes**](https://github.com/Jayden-Lind/LINDS-Kubernetes) - The IaC stack powering the homelab.

**Catcrawl** - Golang service scraping Australian supermarket catalogue prices, with a TypeScript browser extension showing price history and trends.

[**Lindrea**](https://github.com/Jayden-Lind/Lindrea) - Real estate listing change tracker built on realestate.com.au's GraphQL API. Used it to buy my first house.

[**PlayHQ Scraper**](https://github.com/Jayden-Lind/PlayHQ-GraphQL-scraper) - GraphQL to Google Calendar sync for sports fixture data.

---

## Education

**Bachelor of Information Technology Systems** (Major: Networking), Monash University, 2015-2018

**Azure Administrator Associate (AZ-104)**, MCID: 17838270

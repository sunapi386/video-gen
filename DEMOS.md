# Demo Videos

**[View demos with inline video players](https://sunapi386.github.io/video-gen/)**

All videos generated using `video-gen` with the [TokenRouter](https://tokenrouter.com) API. Videos are hosted on [GitHub Releases](https://github.com/sunapi386/video-gen/releases/tag/v0.1.0-demos).

## Model Comparison

Same prompt across all available text-to-video models:

> *"Cinematic close-up of a server rack in a dimly lit room. Blue LED lights reflect off polished metal surfaces. A hand reaches in and plugs an ethernet cable into a port with a satisfying click. Green status LEDs illuminate one by one."*

### Rankings

1. **Happyhorse** (`happyhorse-1.0-t2v`) — best overall, includes generated audio
2. **Seedance 2.0** (`dreamina-seedance-2-0-260128`) — clean rendering, good detail
3. **Kling v3** (`kling-v3`) — strong cinematic feel, most reliable
4. **Kling v2.6** (`kling-v2-6`) — solid but older gen
5. **Hailuo 2.3** (`MiniMax-Hailuo-2.3`) — lowest resolution output
6. **Seedance Fast** (`dreamina-seedance-2-0-fast-260128`) — 400 API error

## K8s Migration — Instructional Series

13-scene storyboard generated from `scripts/k8s-migration.json`. 9 of 13 scenes succeeded (all Kling v3). 4 Seedance Fast scenes returned 400 errors.

| Scene | Description | Model | Size |
|-------|-------------|-------|------|
| 1. Cloud Costs | Aerial data center, rising cost counter | Kling v3 | 11 MB |
| 2. Dashboard Frustration | Red outage alerts on monitoring screen | Kling v3 | 7.7 MB |
| 3. Home Lab Reveal | Camera enters home office with servers | Kling v3 | 6.7 MB |
| 4. Network Switch Detail | Macro shot, ethernet cable plug | Kling v3 | 8.2 MB |
| 5. Battery UPS Setup | LiFePO4 wiring to inverter | Kling v3 | 5.5 MB |
| 6. Power Circuit Diagram | *Failed — Seedance Fast 400* | — | — |
| 7. LTE Router & Antenna | Router setup, SIM, antenna swap | Kling v3 | 4.4 MB |
| 8. Network Topology | *Failed — Seedance Fast 400* | — | — |
| 9. Cloudflare Tunnel | *Failed — Seedance Fast 400* | — | — |
| 10. K8s Deployment | Terminal: Helm charts, pods running | Kling v3 | 12 MB |
| 11. Failover Test | Pull fiber, LTE failover kicks in | Kling v3 | 3.4 MB |
| 12. Cost Comparison | *Failed — Seedance Fast 400* | — | — |
| 13. Final Setup Hero | Complete home lab, all systems green | Kling v3 | 6.7 MB |

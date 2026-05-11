# Demo Videos

All videos generated using `video-gen` with the [TokenRouter](https://tokenrouter.com) API.

## Model Comparison

Same prompt across all available text-to-video models:

> *"Cinematic close-up of a server rack in a dimly lit room. Blue LED lights reflect off polished metal surfaces. A hand reaches in and plugs an ethernet cable into a port with a satisfying click. Green status LEDs illuminate one by one."*

| Model | Video | Duration | Size | Notes |
|-------|-------|----------|------|-------|
| **Kling v3** | [01_compare_kling_v3.mp4](demos/model-comparison/01_compare_kling_v3.mp4) | 5s | 5.2 MB | Strong cinematic quality, good lighting |
| **Kling v2.6** | [02_compare_kling_v2.mp4](demos/model-comparison/02_compare_kling_v2.mp4) | 5s | 7.0 MB | Previous gen, slightly different style |
| **Hailuo 2.3** | [03_compare_hailuo.mp4](demos/model-comparison/03_compare_hailuo.mp4) | 6s | 677 KB | Very small file, lower resolution |
| **Seedance 2.0** | [04_compare_seedance.mp4](demos/model-comparison/04_compare_seedance.mp4) | 5s | 2.8 MB | Good quality, clean rendering |
| **Seedance Fast** | — | — | — | 400 error (API issue) |
| **Happyhorse** | [06_compare_happyhorse.mp4](demos/model-comparison/06_compare_happyhorse.mp4) | 5s | 2.5 MB | Includes generated audio! |

### Rankings

1. **Happyhorse** — best overall, includes sound
2. **Seedance 2.0** — clean rendering, good detail
3. **Kling v3** — strong cinematic feel
4. **Kling v2.6** — solid but older gen
5. **Hailuo 2.3** — lowest resolution output

---

## K8s Migration — Instructional Series

13-scene storyboard for a self-hosted Kubernetes migration video. Generated with the `scripts/k8s-migration.json` script. Scenes 6, 8, 9, 12 (Seedance Fast) failed with API errors — all Kling v3 scenes succeeded.

### Scene 1: Cloud Costs

Cinematic aerial shot of a data center campus at night, cost counter ticking upward.

https://github.com/user-attachments/assets/placeholder

[01_intro_cloud_costs.mp4](demos/k8s-migration/01_intro_cloud_costs.mp4) — Kling v3, 11 MB

### Scene 2: Dashboard Frustration

Monitor showing cloud hosting dashboard with red outage alerts popping up.

[02_railway_dashboard_frustration.mp4](demos/k8s-migration/02_railway_dashboard_frustration.mp4) — Kling v3, 7.7 MB

### Scene 3: Home Lab Reveal

Camera pushes through a doorway into a clean home office with servers and network equipment.

[03_home_lab_reveal.mp4](demos/k8s-migration/03_home_lab_reveal.mp4) — Kling v3, 6.7 MB

### Scene 4: Network Switch Detail

Macro shot of a 10-port network switch, ethernet cable being plugged in.

[04_network_switch_detail.mp4](demos/k8s-migration/04_network_switch_detail.mp4) — Kling v3, 8.2 MB

### Scene 5: Battery UPS Setup

Hands wiring a LiFePO4 battery to a pure sine wave inverter, multimeter showing voltage.

[05_battery_ups_setup.mp4](demos/k8s-migration/05_battery_ups_setup.mp4) — Kling v3, 5.5 MB

### Scene 6: Power Circuit Diagram

*Failed — Seedance Fast returned 400*

### Scene 7: LTE Router & Antenna

Compact LTE router being set up — SIM inserted, external antennas attached, LEDs lighting up.

[07_lte_router_antenna.mp4](demos/k8s-migration/07_lte_router_antenna.mp4) — Kling v3, 4.4 MB

### Scene 8: Network Topology Animation

*Failed — Seedance Fast returned 400*

### Scene 9: Cloudflare Tunnel Visualization

*Failed — Seedance Fast returned 400*

### Scene 10: Kubernetes Deployment

Terminal showing K8s deployment commands, pods spinning up from Pending to Running.

[10_kubernetes_deployment.mp4](demos/k8s-migration/10_kubernetes_deployment.mp4) — Kling v3, 12 MB

### Scene 11: Failover Test

Hand pulls fiber cable, switch LEDs change, dashboard shows connection rerouting via LTE.

[11_failover_test.mp4](demos/k8s-migration/11_failover_test.mp4) — Kling v3, 3.4 MB

### Scene 12: Cost Comparison

*Failed — Seedance Fast returned 400*

### Scene 13: Final Setup Hero Shot

Wide cinematic shot of the complete home lab running — servers, switch, battery, LTE router, K8s dashboard all green.

[13_final_setup_hero.mp4](demos/k8s-migration/13_final_setup_hero.mp4) — Kling v3, 6.7 MB

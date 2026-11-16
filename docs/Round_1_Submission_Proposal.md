# SciX India Hackathon — Round 1 Idea Submission Proposal
## Project: AETHER — Zero-Trust Autonomous P2P Micro-Grid & Energy Derivatives Exchange

**Category:** Engineering (Energy, Electronics, Smart Systems)  
**Team Name:** DEADCODE  
**Team Members:** Raj Patil, Nakul Yawalkar, Soumik Das, Laksh Kachure  
**Institution:** Visvesvaraya National Institute of Technology (VNIT Nagpur)  
**Host Organization:** SciAstra Labs (on SciX App)  
**Innovation Partner:** CiiA (Consortium of Indo-Israel Alliances)  
**Grand Finale Target:** CiiA-6 National Science Exhibition, Nehru Science Centre, Worli, Mumbai (4–6 Feb 2027)  
**Hardware Budget (Prototype BOM):** ₹2,646  

---

### 1. Executive Summary
The rapid growth of distributed rooftop solar across India has exposed a severe economic and operational paradox: prosumers are forced to export surplus solar energy to state electricity distribution companies (DISCOMs) at rock-bottom feed-in tariffs (**₹2.82/kWh** under MERC regulations), while their immediate neighbors purchase power from the grid at peak retail rates (**₹10.50/kWh** under MSEDCL upper slabs). This **₹7.68/kWh spread** causes prosumers to forfeit over 73% of their potential energy value, extending solar-plus-storage payback cycles past 7–9 years. Furthermore, uncoordinated electric vehicle (EV) charging during evening hours creates dangerous overload on local distribution transformers.

**AETHER (Autonomous Energy Trading via Hardware Entropy Routing)** replaces static, monopolistic utility net-metering with a decentralized, peer-to-peer (P2P) commodities exchange. Smart meters acting as autonomous financial agents run localized Automated Market Maker (AMM) algorithms on dual-core microcontrollers (ESP32). Nodes continuously monitor solar irradiance, battery State-of-Charge (SoC), and household loads, automatically broadcasting bids and asks into a sub-millisecond Continuous Double Auction (CDA) matching engine. Energy is traded directly between neighbors at a fair clearing spot price (**₹6.00/kWh**), delivering a win-win: sellers earn **+112% more**, while buyers save **42%**.

To guarantee bank-grade zero-trust security without the transaction fees (₹5–₹50/tx) or slow confirmation delays (12s–15m) of traditional blockchains, AETHER integrates a custom **C++ Physical Entropy Generator (`entropy_core.cpp`)**. By harvesting real-world environmental optical and acoustic noise, each cleared trade is cryptographically signed with an un-forgeable True Random Number Generator (TRNG) nonce (`TX_ID`). Solid-state relays with inrush-limiting $10\,\Omega$ ceramic resistors physically steer negotiated DC power across prosumer nodes over a local micro-grid mesh.

---

### 2. The Problem Statement & Indian Context (Relevance — 20%)
#### 2.1 The Economic Inequity of Net-Metering
Under prevailing net-metering regimes in Maharashtra and across India, prosumers bear the full capital expenditure for solar photovoltaic (PV) panels and battery energy storage systems (BESS), but capture only a fraction of the value created:
* **Export Buyback (Feed-in Tariff):** **₹2.82/kWh** *(Source: MERC Tariff Order Case No. 226 of 2022)*.
* **Retail Peak Import Tariff:** **₹10.50/kWh** *(Source: MSEDCL Retail Tariff Schedule FY 2024–25)*.
The utility captures a **₹7.68/kWh arbitrage spread**, discouraging decentralized energy storage investments and leaving prosumers with poor return on investment.

#### 2.2 Grid Congestion & Transformer Stress
Modern distribution grids lack real-time local price discovery. When EV charging sessions occur simultaneously during evening peak hours, local step-down distribution transformers face severe thermal stress, leading to premature transformer failure and localized blackouts. Concurrently, unmanaged midday solar backfeed causes reverse voltage surges on distribution lines.

#### 2.3 Cybersecurity & Cost Deficits in Existing P2P Models (Novelty — 25%)
Current academic and commercial P2P energy platforms (e.g., Power Ledger, Brooklyn Microgrid) rely on public or consortium blockchains:
1. **Gas Fee Prohibitive:** A 50Wh micro-trade is worth ~₹0.30, but blockchain gas fees range from ₹5 to ₹50 per transaction, completely destroying micro-trade economics.
2. **Excessive Block Latency:** 12-second to 15-minute block confirmation times cannot support real-time physical relay switching.
3. **Deterministic Spoofing:** IoT smart meters using standard Pseudo-Random Number Generators (PRNG) are vulnerable to state deduction and replay attacks.

---

### 3. The Proposed Solution: AETHER Architecture
Our system replaces static feed-in tariffs with an **autonomous localized commodities exchange** operating across physical hardware nodes:
1. **Automated Market Makers (AMM) with Battery Degradation Modeling:**
   Each household is equipped with an ESP32 trading node paired with an INA219 bidirectional power sensor. Bids and asks are priced dynamically based on battery State-of-Charge (SoC) and a Levelized Cost of Storage ($C_{\text{deg}}$) floor:
   $$Ask_{\text{floor}} = P_{\text{feed-in}} (₹2.82) + C_{\text{degradation}} (\approx ₹2.00) + \Delta_{\text{SoC}}$$
   This mathematically guarantees prosumers never trade stored battery power at an economic loss.
2. **Continuous Double Auction (CDA) with DISCOM Liquidity Corridor:**
   A low-latency C++20 engine aggregates order books via UDP, dynamically clearing at **₹6.00/kWh**. To eliminate order book starvation, the DISCOM acts as the **Liquidity Provider of Last Resort** with synthetic standing limit orders at ₹2.82 (Floor) and ₹10.50 (Ceiling).
3. **Physical Micro-Grid Routing with Inrush Protection:**
   Solid-state relay modules and series ceramic power resistors ($10\,\Omega$) physically clamp inrush currents safely to ~300 mA while dynamically routing real DC power between matched prosumers.
4. **Zero-Trust TRNG Settlement & Proof-of-Energy-Transfer (PoET):**
   Unrepeatable environmental hardware entropy generates un-forgeable nonces (`TX_ID`), sealing transactions without blockchain overhead. Final financial settlement uses a two-phase commit verified against both nodes' INA219 energy telemetry.

---

### 4. Technical Architecture & Engineering Pipeline
```
[ Mini Solar Cell + Battery ]
           │
           ▼
[ INA219 Current/Voltage Sensor ] (10ms Telemetry)
           │
           ▼ (I2C)
[ ESP32 Autonomous Trading Node ] (Runs AMM Edge Pricing Logic)
           │
           ▼ (Low-Latency UDP over Wi-Fi)
[ C++20 Continuous Double Auction Engine ]
     ▲
     │ (Cryptographic Trade Verification)
[ Physical Entropy Generator (C++ AVX2 TRNG: 39 µs) ]
           │
           ▼ (Execution Signal)
[ Solid-State Relays + 10Ω Resistors ] ➔ [ Physical DC Power Routing to Buyer Load ]
```

#### Pipeline Stages:
1. **Telemetry Layer:** CJMCU-219 INA219 sensors measure real-time bus voltage and current draw with 12-bit precision every 10 milliseconds over I2C.
2. **Algorithmic Edge Bidding:** Dual-core ESP32 executes a localized AMM algorithm with $C_{\text{deg}}$ battery protection.
3. **CDA Limit Order Book:** Central C++20 engine organizes limit orders by price-time priority, crossing matching orders instantaneously.
4. **Zero-Trust Cryptographic Nonce Generation:** Trades are validated via `entropy_core.cpp`, which extracts unrepeatable physical noise into a 32-byte cryptographic seed in **~39 microseconds** (8,800× faster than Python). This seed seals transactions as an immutable `TX_ID = HMAC-SHA256(Seed, TradeData)`.
5. **Physical Power Routing:** The matching engine outputs a clearance trigger, activating opto-isolated solid-state relays that physically deliver DC current to the matched peer.

---

### 5. Bill of Materials (BOM) & Hardware Feasibility (₹2,646 Total)
The prototype is engineered for extreme capital efficiency, proving that autonomous smart-grid infrastructure can be deployed in cost-sensitive markets:

| Item | Component Description | Role | Qty | Unit Cost (₹) | Total Cost (₹) |
|---|---|---|---|---|---|
| 1 | **Robocraze ESP32 Dual-Core Dev Board** | Autonomous AMM Trading Node (Wi-Fi + I2C) | 3 | ₹469 | ₹1,408 |
| 2 | **CJMCU-219 INA219 Current Sensor** | Bidirectional DC Voltage/Current Telemetry | 3 | ₹86 | ₹258 |
| 3 | **4-Channel 5V Relay Module + LCDs** | Physical DC Switching & Local Node Display | 1 set | ₹380 | ₹380 |
| 4 | **Solar PV Cells & Ceramic Inrush Loads** | 6V Solar Cells + 10Ω Power Resistors + Acrylic Base | 1 set | ₹600 | ₹600 |
| **Total** | **Complete 3-Node Physical Tabletop Grid** | — | — | — | **₹2,646** |

#### Early Work Validated vs. 4-Week Sprint Plan:
* **Already Validated:** The core C++ AVX2 entropy engine (`entropy_core.cpp`) is already written, compiled, tested, and benchmarked at 39 µs per 921 KB frame.
* **Week 1–2:** Tabletop DC bus assembly, $10\,\Omega$ ceramic inrush resistor integration, and INA219 sensor calibration.
* **Week 3–4:** UDP socket order book matching, physical relay DC switching, and 3-house interactive demonstration video.

---

### 6. Team DEADCODE (Visvesvaraya National Institute of Technology - VNIT Nagpur)
* **Raj Patil** (VNIT Nagpur) — System Architecture, Firmware Coordination & Market Making
* **Nakul Yawalkar** (VNIT Nagpur) — Core Exchange Engine (C++20) & Network Sockets
* **Soumik Das** (VNIT Nagpur) — Cryptography, TRNG Nonce Integration & Security State Machine
* **Laksh Kachure** (VNIT Nagpur) — Power Electronics, Circuit Rig & Trading Terminal UI

---

### 7. Interactive Live Demonstration for CiiA-6 Exhibition (Nehru Science Centre, Mumbai)
1. **Equilibrium State:** Three tabletop houses generate solar power; batteries maintain normal levels. The centralized trading dashboard displays a live order book and zero pending bids.
2. **The Grid Shock (Judge Participation):** The judge is invited to cover House 1's solar cell with their hand, simulating sudden storm-induced generation loss.
3. **Autonomous Dynamic Reaction:** House 1's INA219 detects a sharp voltage drop. Within milliseconds, House 1's ESP32 autonomously issues an urgent BUY order. The live terminal depth chart spikes.
4. **Physical Power Delivery & Zero-Trust Verification:** The C++ matching engine matches House 1 with House 3. The physical entropy generator produces an un-forgeable nonce; the screen flashes **"SECURE TRADE CLEARED"**, the physical relay snaps closed, and House 1's lights stay illuminated using House 3's real DC power flow.

---

### 8. Commercialization, DISCOM Alignment & National Impact (Impact — 20%)
* **PM Surya Ghar: Muft Bijli Yojana Alignment:** Directly supports the national target of **1 Crore rooftop solar installations** by making residential battery storage financially viable.
* **B2B Micro-Utilities:** Turnkey deployment across gated residential societies, commercial IT parks, and industrial SEZs behind a single master meter.
* **DISCOM Partnership Model:** Utilities act as licensed market clearinghouses, earning a **5% wheeling fee** on all P2P transactions while deferring multi-crore substation transformer upgrades.

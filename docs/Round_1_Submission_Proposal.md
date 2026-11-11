# SciX India Hackathon — Round 1 Idea Submission Proposal
## Project: Zero-Trust Autonomous P2P Micro-Grid & Energy Derivatives Exchange

**Category:** Engineering (Energy, Electronics, Smart Systems)  
**Host Organization:** SciAstra Labs (on SciX App)  
**Innovation Partner:** CiiA (Consortium of Indo-Israel Alliances)  
**Grand Finale Target:** CiiA-6 National Science Exhibition, Nehru Science Centre, Worli, Mumbai (4–6 Feb 2027)  
**Hardware Budget (Prototype BOM):** ₹2,646  

---

### 1. Executive Summary
The transition to distributed renewable energy across India has created a fundamental economic and operational paradox: rooftop solar prosumers are forced to sell surplus energy to state electricity distribution companies (DISCOMs) at rock-bottom feed-in tariffs (e.g., ₹2.50/kWh), while their immediate neighbors purchase power from the grid at peak retail rates (e.g., ₹8.00/kWh). Furthermore, localized surges from electric vehicle (EV) fast-charging place massive strain on neighborhood distribution transformers.

This project introduces a **Zero-Trust Autonomous Peer-to-Peer (P2P) Micro-Grid & Energy Derivatives Exchange**. We turn passive residential and commercial smart meters into autonomous algorithmic trading nodes running on low-cost dual-core microcontrollers (ESP32). Nodes continuously assess local photovoltaic generation, battery State-of-Charge (SoC), and consumption deficits, automatically issuing bids and asks to a centralized sub-millisecond Continuous Double Auction (CDA) matching engine.

To ensure bank-grade transaction security without introducing the latency, computational bloat, or gas fees of traditional blockchains, the system incorporates a **Physical Entropy Generator (`entropy_core.cpp`)**. By harvesting unpredictable environmental hardware noise, each cleared micro-transaction is signed with a high-entropy cryptographic nonce, guaranteeing zero-trust immutability and immunity to replay attacks. Matched trades trigger solid-state relay arrays to physically steer DC power between prosumer nodes over a local micro-grid mesh.

---

### 2. The Problem Statement
#### 2.1 The Economic Inequity of Net-Metering
Under prevailing net-metering regimes in India, prosumers bear the full capital expenditure for solar photovoltaic (PV) panels and battery energy storage systems (BESS), but capture only a fraction of the value created. 
- **Feed-in Tariff (Export):** ~₹2.25 – ₹3.00 per unit (kWh).
- **Retail Consumer Tariff (Import):** ~₹7.50 – ₹10.00 per unit (kWh).
The DISCOM extracts an arbitrage spread of over 200%, discouraging decentralized renewable investments and extending prosumer payback cycles beyond 7–9 years.

#### 2.2 Grid Congestion & Inelastic Local Distribution
Modern distribution grids lack real-time local price discovery. When EV charging sessions occur simultaneously during evening peak hours, local step-down distribution transformers face severe thermal stress, leading to premature transformer failure and localized blackouts.

#### 2.3 Cybersecurity Deficits in Decentralized Trading
Current academic and industrial P2P energy pilot projects face two critical flaws:
1. **Blockchain Bloat:** Distributed ledger technologies (Ethereum, Hyperledger) suffer from slow settlement times (seconds to minutes) and transaction costs that exceed the value of micro-trades (50–100 Wh packets).
2. **Deterministic Spoofing:** IoT smart meters using standard Pseudo-Random Number Generators (PRNG) are vulnerable to side-channel key extraction and replay attacks, where malicious nodes fabricate meter readings and trade confirmations.

---

### 3. The Proposed Solution
Our system replaces static feed-in tariffs with an **autonomous localized commodities exchange** operating across physical hardware nodes:
1. **Automated Market Makers (AMM) with Battery Degradation Modeling:** Each household is equipped with an ESP32 trading node paired with an INA219 bidirectional power sensor. Bids and asks are priced dynamically based on battery State-of-Charge (SoC) and a Levelized Cost of Storage ($C_{\text{deg}}$) floor. This guarantees prosumers never trade stored battery power at an economic loss.
2. **Continuous Double Auction (CDA) with DISCOM Liquidity Corridor:** A low-latency C++20 engine aggregates order books via UDP, dynamically computing the market-clearing **Spot Price** (e.g., ₹5.50/kWh). Sellers earn **+120% more** than feed-in tariffs, while buyers save **31%** compared to grid retail tariffs. To eliminate order book starvation at night, the DISCOM acts as the **Liquidity Provider of Last Resort** with synthetic standing limit orders at ₹2.50 (Floor) and ₹8.00 (Ceiling).
3. **Physical Micro-Grid Routing with Inrush Protection:** Solid-state relay modules and series ceramic power resistors ($10\,\Omega$) physically clamp inrush currents safely to ~300 mA while dynamically routing real DC power between matched prosumers.
4. **Zero-Trust TRNG Settlement & Proof-of-Energy-Transfer (PoET):** Unrepeatable environmental entropy generated from optical/sensor noise generates un-forgeable nonces (`TX_ID`), sealing transactions without blockchain overhead. Final financial settlement uses a two-phase commit verified against both nodes' INA219 energy telemetry.

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
[ Physical Entropy Generator (C++ TRNG Nonces) ]
           │
           ▼ (Execution Signal)
[ Solid-State Relay Module ] ➔ [ Physical DC Power Routing to Buyer Load ]
```

#### Pipeline Stages:
1. **Telemetry Layer:** CJMCU-219 INA219 sensors measure real-time bus voltage and current draw with 12-bit precision every 10 milliseconds over I2C.
2. **Algorithmic Edge Bidding:** Dual-core ESP32 executes a localized AMM algorithm. When battery SoC is critical, the node submits an aggressive BUY order. When storage is full and irradiance is high, it posts a discounted SELL order.
3. **CDA Limit Order Book:** The central C++20 engine organizes limit orders by price-time priority, crossing matching orders instantaneously.
4. **Zero-Trust Cryptographic Nonce Generation:** Trades are validated via `entropy_core.cpp`, which extracts unrepeatable physical noise into a cryptographically conditioned nonce. This nonce serves as an immutable `TX_ID`.
5. **Physical Power Routing:** The matching engine outputs a cryptographic clearance trigger to the node, activating opto-isolated solid-state relays that physically deliver the electric current to the matched peer.

---

### 5. Bill of Materials (BOM) & Budget Feasibility
The prototype is engineered for extreme capital efficiency, proving that autonomous smart-grid infrastructure can be deployed in cost-sensitive markets:

| Item | Component Description | Role | Qty | Unit Cost (₹) | Total Cost (₹) |
|---|---|---|---|---|---|
| 1 | **Robocraze ESP32 Dual-Core Dev Board** | Autonomous AMM Trading Node (Wi-Fi + I2C) | 3 | ₹469 | ₹1,408 |
| 2 | **CJMCU-219 INA219 Current Sensor** | Bidirectional DC Voltage/Current Telemetry | 3 | ₹86 | ₹258 |
| 3 | **4-Channel 5V Relay Module + LCDs** | Physical DC Switching & Local Node Display | 1 set | ₹380 | ₹380 |
| 4 | **Solar PV Cells & Ceramic Loads** | 6V Mini Solar Cells + Power Resistors + Acrylic Base | 1 set | ₹600 | ₹600 |
| **Total** | **Complete 3-Node Physical Tabletop Grid** | — | — | — | **₹2,646** |

*Note: All components are off-the-shelf, low-power, and readily available across Indian electronics suppliers.*

---

### 6. Team Roles & Execution Plan
* **Member 1 (Core Exchange Engine — C++20):** Continuous Double Auction matching algorithm, Limit Order Book (LOB) depth tracking, and UDP socket networking.
* **Member 2 (Cryptography & Zero-Trust Security — C++):** Integration of `physical-entropy-generator`, environmental noise conditioning, and nonce-based transaction verification.
* **Member 3 (Embedded Firmware & AMM Quant Logic — ESP32/C++):** Real-time I2C driver integration for INA219, SoC estimation filters, and automated bid/ask quoting algorithms.
* **Member 4 (Power Electronics, Hardware Rig & UI):** Tabletop circuit assembly (relays, solar panels, battery simulators), safety interlocks, and a dark-mode web/terminal trading dashboard.

---

### 7. Interactive Live Demonstration for CiiA-6 Exhibition (Nehru Science Centre, Mumbai)
The live showcase at CiiA-6 is structured into an interactive 4-phase judge experience:
1. **Equilibrium State:** Three tabletop houses generate solar power; batteries maintain normal levels. The centralized trading dashboard displays a live order book and zero pending bids.
2. **The Grid Shock (Judge Participation):** The judge is invited to cover House 1's solar cell with their hand, simulating sudden storm-induced generation loss.
3. **Autonomous Dynamic Reaction:** House 1's INA219 detects a sharp voltage drop. Within milliseconds, House 1's ESP32 autonomously issues an urgent BUY order. The live terminal depth chart spikes.
4. **Physical Power Delivery & Zero-Trust Verification:** The C++ matching engine matches House 1 with House 3 (which holds surplus solar energy). The physical entropy generator produces an un-forgeable nonce; the screen flashes **"SECURE TRADE CLEARED"**, the physical relay snaps closed, and House 1's lights stay illuminated using House 3's real DC power flow.

---

### 8. Commercialization, DISCOM Alignment & Scalability
* **B2B Micro-Utilities:** Gated communities, IT tech parks, and commercial complexes can self-balance peak energy demand without incurring heavy maximum-demand penalties from utilities.
* **DISCOM Partnership Model:** Rather than resisting P2P energy, DISCOMs operate as the licensed settlement clearinghouse, collecting a 5–8% wheeling fee per transaction while deferring costly substation transformer upgrades.
* **Carbon Credit Verification:** Because every kilowatt-hour traded is stamped with a hardware-anchored cryptographic nonce, carbon offsets and green energy credits can be audited with zero risk of double-counting.

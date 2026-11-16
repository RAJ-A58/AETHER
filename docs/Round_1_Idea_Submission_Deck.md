# AETHER: Autonomous Energy Trading via Hardware Entropy Routing
## SciX India Hackathon — Round 1: Official 8-Slide Pitch Deck Specification
**Category:** Engineering (Smart Systems, Electronics & Energy)  
**Team Name:** DEADCODE  
**Team Members:** Raj Patil, Nakul Yawalkar, Soumik Das, Laksh Kachure  
**Institution:** Visvesvaraya National Institute of Technology (VNIT Nagpur)  
**Innovation Partner:** CiiA (Consortium of Indo-Israel Alliances)  
**Target Exhibition:** CiiA-6 National Science Exhibition, Nehru Science Centre, Mumbai  
**Hardware Budget (Prototype BOM):** ₹2,646  

---

### Slide 1: Title & Team Credentials
* **Main Title:** AETHER: Autonomous Energy Trading via Hardware Entropy Routing
* **Subtitle:** A Zero-Trust Autonomous P2P Micro-Grid & Energy Derivatives Exchange
* **Track:** SciX India Hackathon · Stage 1 · Engineering Track
* **Team Credentials:** `[DEADCODE | RAJ PATIL, NAKUL YAWALKAR, SOUMIK DAS, LAKSH KACHURE | VISVESVARAYA NATIONAL INSTITUTE OF TECHNOLOGY]`
* **4 Metric Highlights:**
  - `₹2,646 Hardware BOM` (Ultra-frugal tabletop testbed)
  - `10ms INA219 Telemetry` (Sub-second power sensing)
  - `Zero-Trust Physical TRNG` (Hardware chaos nonces)
  - `CiiA-6 Track` (Nehru Science Centre, Mumbai)

---

### Slide 2: The Problem — The Broken Economics of Solar Net-Metering in India (Relevance — 20%)
* **Headline:** The Broken Economics of Rooftop Solar Net-Metering in India
* **Summary:** Export buyback sits far below retail import prices, so local solar surplus is undervalued and evening grid peaks stay unmanaged.
* **Card 1 (The ₹7.68 Tariff Gap — Export Buyback vs. Peak Retail Import):**
  - Export buyback is **₹2.82/kWh** vs. peak retail import at **₹10.50/kWh**.
  - Prosumers forfeit about 73% of retail value to the spread (calculated from these two rates).
  - Prosumers lose 73% of generation value, extending solar-plus-storage payback to 7–9 years.
* **Card 2 (Grid Congestion & Transformer Stress — Local Feeder and Transformer Strain):**
  - Simultaneous uncoordinated evening EV charging creates severe peak loads on local step-down transformers.
  - Midday solar backfeed destabilizes local feeder lines when no local price signal exists.
* **Statutory Citation:**
  - *Source: MERC Tariff Order (Case No. 226 of 2022) & MSEDCL Retail Tariff Schedule FY 2024–25; Central Electricity Authority (CEA) Technical Reports.*

---

### Slide 3: What Already Exists & Why It Fails (Novelty — 25%)
* **Headline:** Current Alternatives Fail at the Micro-Grid Edge
* **Summary:** Three incumbent paradigms each miss the same need: fast, low-cost, physically verified trades between neighbors.
* **Card 1 (Traditional Net-Metering — DISCOM Monopoly):**
  - Static monthly credits and zero dynamic pricing.
  - Prosumers are economically penalized for adding battery storage. Pricing: Fixed by regulation.
* **Card 2 (Blockchain P2P — Ledger-Based Trading):**
  - High Gas Fees: Public blockchain fees (₹5–₹50 per tx) dwarf micro-energy packets (50 Wh worth ~₹0.30).
  - 12s–15m block confirmation latencies cannot support real-time physical relay switching. Pricing: Tokenized auctions.
* **Card 3 (Static Bilateral Contracts — Rigid Fixed Rates):**
  - Fixed contracts cannot adapt dynamically to sudden cloud cover, battery drain, or EV charging spikes. Pricing: Rigid contractual.
* **Takeaway:** *The market is trapped between slow, expensive blockchain ledgers and rigid utility monopolies.*

---

### Slide 4: Proposed Solution — AETHER Architecture (Solution Overview)
* **Headline:** Autonomous Micro-Grid Commodities Exchange & Physical Power Routing
* **4-Stage Pipeline:**
  - `SENSE ➔ 10 ms INA219 Sensing`: Edge nodes read current and voltage every 10 ms.
  - `QUOTE ➔ ESP32 AMM Quoting`: Each node posts bids and asks from battery-aware floors.
  - `MATCH ➔ C++20 CDA Matcher @ ₹6.00/kWh`: Continuous double auction with price-time priority.
  - `ROUTE ➔ Solid-State Relays Route DC Current`: Matched trades switch power between peers on the DC bus.
* **The Win-Win Clearing Corridor (Spot Price: ₹6.00/kWh):**
  - **Prosumer Seller:** Earns ₹6.00/kWh (+112% gross uplift over the ₹2.82/kWh feed-in rate).
  - **Neighbor Buyer:** Pays ₹6.00/kWh (42% gross savings vs. the ₹10.50/kWh utility retail tariff).
  - **Utility Partner:** DISCOM operates as the licensed settlement clearinghouse, capturing a 5% wheeling fee on P2P volume while shedding peak transformer strain.

---

### Slide 5: Engineering & Quant Modeling (Feasibility — 25%)
* **Headline:** Battery Degradation-Aware AMM & the DISCOM Liquidity Corridor
* **Card 1 (Battery Degradation Protection):**
  - Formula:
    $$Ask_{\text{floor}} = P_{\text{feed-in}} + C_{\text{degradation}} + \Delta_{\text{SoC}}$$
  - Where:
    $$C_{\text{degradation}} = \frac{\text{Battery Pack Replacement Cost}}{\text{Rated Lifecycle Cycles} \times \text{Usable Capacity}}$$
  - Direct solar surplus quotes down to ₹3.50/kWh ($C_{\text{deg}} = 0$).
  - Stored battery power dynamically enforces a ₹4.80/kWh reserve floor.
  - **Guaranteed Prosumer Margins:** Prosumers are mathematically protected from trading stored battery energy below physical replacement wear (~₹2.00/kWh).
* **Card 2 (DISCOM Liquidity Corridor — Market Maker of Last Resort):**
  - **Standing Synthetic Orders:** A floor at ₹2.82/kWh absorbs surplus; a ceiling at ₹10.50/kWh supplies deficits.
  - **Uninterrupted Supply:** Eliminates thin-market liquidity freezes in small micro-grids, ensuring zero power disruptions.
  - **Utility-Friendly Model:** DISCOM collects a 5% wheeling fee on all P2P trades while avoiding costly transformer upgrades.

---

### Slide 6: Deep-Tech Novelty — Zero-Trust TRNG Settlement (Novelty — 25%)
* **Headline:** Bank-Grade Settlement Powered by Environmental Hardware Chaos
* **Subtitle:** Hardware-accelerated True Random Number Generation for sub-millisecond, zero-gas trade settlement.
* **Card 1 (Physical Entropy Harvesting — CMOS Optical Shot Noise & Acoustic Static):**
  - Captures microscopic, non-deterministic environmental noise through a custom C++ AVX2 SIMD core (`entropy_core.cpp`).
  - **Physical Non-Determinism:** Anchored in physical quantum photon arrival and thermal fluctuations, making seed prediction mathematically impossible.
* **Card 2 (39-Microsecond Benchmark — 921 KB Frames ➔ 32-Byte Seed):**
  - **Ultra-Low Latency:** Distills full raw sensor frames into a 32-byte cryptographic seed in ~39 µs (8,800× faster than Python).
  - **SIMD Vector Pipeline:** Utilizes Intel AVX2 256-bit registers (`_mm256_xor_si256`, 64-bit vector lane permutation, and modular addition).
* **Card 3 (Anti-Replay Nonce Engine — TX_ID = HMAC-SHA256(EntropySeed, TradeData)):**
  - **Replay Immunity:** Each cleared trade is stamped with an un-forgeable single-use Transaction ID verified against hardware sequence registers.
  - **Zero Gas Overhead:** Replaces slow, expensive blockchains with microsecond physical settlement and ₹0.00 transaction fees.
* **Zero-Trust Edge Advantage:**
  - *Eliminates distributed ledger gas bloat (₹0.00 vs ₹5–₹50) and 15-minute block delays, enabling bank-grade physical settlement directly at the micro-grid edge.*

---

### Slide 7: Hardware Feasibility & 4-Week Prototype Work (Feasibility — 25%)
* **Headline:** Frugal Hardware: ₹2,646 BOM & Early Prototype Work
* **Itemized Bill of Materials (100% Off-The-Shelf in India):**
  | Item | Cost (₹) |
  |---|---|
  | 3× Robocraze ESP32 dual-core dev boards | 1,408 |
  | 3× CJMCU-219 INA219 current sensors | 258 |
  | 4-channel 5 V relay module + LCDs | 380 |
  | Solar PV cells + 10 Ω inrush ceramic resistors + base | 600 |
  | **Total hardware prototype** | **₹2,646** |
* **Core Architecture Validated (Already Tested):**
  - C++ AVX2 entropy core (`entropy_core.cpp`) is already compiled, tested, and benchmarked at 39 µs for seed generation.
* **4-Week Prototype Sprint:**
  - **Week 1–2:** Tabletop DC bus assembly, 10 Ω inrush ceramic resistor integration & INA219 calibration.
  - **Week 3–4:** UDP socket order matching, physical relay DC routing, and live demonstration video.

---

### Slide 8: National Impact Alignment & The 4-Phase Live Demonstration (Impact — 20%)
* **Headline:** National Impact Alignment & the 4-Phase Live Demonstration
* **National Policy Alignment (PM Surya Ghar: Muft Bijli Yojana):**
  - Directly aligns with India's national mandate targeting **1 Crore rooftop solar installations**.
  - **Turnkey Micro-Grid Solution:** Engineered for rapid deployment across gated residential societies, commercial IT parks, and rural solar micro-grids.
  - **Prosumer Value Capture:** Converts passive solar owners into active micro-utilities, reducing payback times from 9 years to under 4 years.
* **CiiA-6 Live Demo Script:**
  1. **Equilibrium:** 3 tabletop houses generate balanced solar power; quiet order book on trading terminal.
  2. **The Grid Shock:** Evaluator physically places their hand over House 1's solar cell, simulating a sudden storm blackout.
  3. **Market Reaction:** Voltage drops; House 1's ESP32 autonomously broadcasts aggressive BUY orders into the C++ engine.
  4. **Physical Settlement:** Engine matches House 1 & 3; TRNG nonce signs trade; physical relay snaps audibly; House 1 lights stay powered via House 3's stored energy.

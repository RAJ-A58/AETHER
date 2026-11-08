# AETHER: Autonomous Energy Trading via Hardware Entropy Routing
### Zero-Trust Autonomous P2P Micro-Grid & Energy Derivatives Exchange

[![Hackathon](https://img.shields.io/badge/SciX%20India%20Hackathon-CiiA--6%20Mumbai-blue.svg)](https://scix.in)
[![Category](https://img.shields.io/badge/Category-Engineering%20%7C%20Smart%20Systems-orange.svg)]()
[![Hardware Budget](https://img.shields.io/badge/Prototype%20BOM-%E2%82%B92%2C646-green.svg)]()
[![Security](https://img.shields.io/badge/Security-Zero--Trust%20TRNG%20Nonces-red.svg)]()

---

## 1. Executive Summary
**AETHER** replaces passive, economically inefficient net-metering grids with a decentralized peer-to-peer (P2P) commodities exchange. Smart meters acting as autonomous financial agents allow households to dynamically trade excess rooftop solar power with neighbors at mutually beneficial spot prices.

To guarantee bank-grade zero-trust security without the transaction fees, computational bloat, or slow block times of conventional blockchains, AETHER integrates a custom **C++ Physical Entropy Generator (`entropy_core.cpp`)**. By harvesting environmental hardware noise, every cleared micro-trade is cryptographically signed with an un-forgeable True Random Number Generator (TRNG) nonce (`TX_ID`), making transactions mathematically immune to replay and spoofing attacks.

---

## 2. The Problem & Solution
* **The Broken Economics of Net-Metering:** Prosumers dump excess solar power back to the state DISCOM at rock-bottom feed-in tariffs (e.g., **₹2.50/kWh**), while direct neighbors buy that exact electricity at premium peak rates (e.g., **₹8.00/kWh**).
* **The AETHER Solution:** Autonomous edge nodes running Automated Market Maker (AMM) logic dynamically quote bids/asks into a Continuous Double Auction (CDA) matching engine. Energy is traded directly between neighbors at a fair clearing spot price (e.g., **₹5.50/kWh**), delivering a win-win: sellers earn **+120% more**, while buyers save **31%**. Solid-state relays physically steer the negotiated DC power across the micro-grid mesh.

---

## 3. System Architecture Pipeline

```
[ INA219 Power Sensors ] (10ms Telemetry)
           │
           ▼ (I2C)
[ ESP32 Autonomous Nodes ] (Edge AMM Bidding Logic)
           │
           ▼ (Low-Latency UDP over Wi-Fi)
[ C++20 Continuous Double Auction Engine ]
     ▲
     │ (Cryptographic Verification)
[ Physical Entropy Generator (C++ AVX2 TRNG) ]
           │
           ▼ (Physical Clearance Signal)
[ Solid-State Relays ] ➔ [ Real DC Power Routing to Matched Load ]
```

---

## 4. Hardware Bill of Materials (BOM) — Total: ₹2,646

| Component | Specification | Qty | Unit Cost (₹) | Total Cost (₹) |
|---|---|---|---|---|
| **Robocraze ESP32 Dual-Core** | Autonomous Trading Nodes (Wi-Fi + I2C) | 3 | ₹469 | ₹1,408 |
| **CJMCU-219 INA219 Sensors** | Bidirectional DC Voltage/Current Telemetry | 3 | ₹86 | ₹258 |
| **Opto-Isolated Relay + LCDs** | Physical DC Switching & Node Telemetry Display | 1 set | ₹380 | ₹380 |
| **Solar Cells & Ceramic Loads** | 6V Mini Solar Cells + Power Resistors + Base | 1 set | ₹600 | ₹600 |
| **Total Prototype Cost** | **Complete 3-Node Tabletop Smart Grid** | — | — | **₹2,646** |

---

## 5. Repository Structure

```
AETHER/
├── docs/                               # Hackathon proposals, pitch decks & guides
│   ├── README.md                       # Documentation index
│   ├── TEAM_ONBOARDING_GUIDE.md        # Technical architecture manual & packet specs
│   ├── PHYSICAL_ENTROPY_GENERATOR.md   # Zero-trust TRNG hardware & SIMD spec
│   ├── Round_1_Idea_Submission_Deck.md # 6–8 Slide pitch deck for Round 1
│   ├── Round_1_Submission_Proposal.md  # Detailed technical & economic proposal
│   └── SciX India Hackathon.pdf        # Official event handbook
├── src/                                # Project codebase
│   ├── engine/                         # C++20 Continuous Double Auction matching engine
│   ├── entropy/                        # Physical entropy TRNG core & capture drivers
│   ├── firmware/                       # ESP32 AMM & telemetry firmware (FreeRTOS)
│   └── dashboard/                      # Real-time order book & power flow trading terminal
├── .gitignore
└── README.md
```

---

## 6. Live Demo Plan (CiiA-6 Mumbai, Nehru Science Centre)
1. **Equilibrium:** 3 tabletop houses generate balanced solar power. The live terminal displays a steady order book.
2. **The Grid Shock:** The judge places their hand over House 1’s solar panel, simulating a storm/cloud cover.
3. **Market Reaction:** House 1's voltage drops; ESP32 floods the order book with urgent BUY orders.
4. **Physical Settlement:** The engine matches House 1 with House 3. The C++ entropy core signs the trade with a TRNG nonce, the relay clicks audibly, and House 1's lights stay powered via House 3's surplus energy.

---

## 7. Team Execution (4-Person Split)
* **Member 1 (Core Exchange Engine - C++20):** Continuous Double Auction matching engine & UDP networking.
* **Member 2 (Cryptography & Zero-Trust - C++):** Physical entropy generator integration & nonce-based settlement.
* **Member 3 (Embedded Systems & Quant Pricing - ESP32):** INA219 telemetry driver & AMM edge bidding algorithms.
* **Member 4 (Power Electronics & UI):** Tabletop circuit assembly, relay routing, and dark-mode terminal dashboard.

# AETHER: Technical Architecture & System Guide
## Shared Engineering Manual for Teammates

Welcome to the project! This document outlines the core architecture of **AETHER**, the master data flow between subsystems, the exact network packet contracts, the hardware wiring reference, and key pitch talking points.

---

## 1. The 30-Second Elevator Pitch

> *"AETHER replaces broken net-metering (where prosumers sell solar to the grid at ₹2.50/kWh and buy back at ₹8.00/kWh) with an autonomous peer-to-peer energy exchange. Our ESP32 smart meters use Automated Market Maker (AMM) algorithms to trade power directly with neighbors at ~₹5.50/kWh. To prevent trade spoofing without using slow, expensive blockchains, we use a C++ physical entropy engine that captures real-world hardware noise to sign every micro-trade with an un-forgeable cryptographic nonce."*

---

## 2. Master System Architecture & Data Flow

All subsystems communicate in real time over low-latency UDP and local buses:

```
 EDGE METER NODES                  MATCHING ENGINE                ENTROPY ORACLE
┌────────────────────┐            ┌───────────────────┐          ┌───────────────────┐
│ ESP32 + INA219     │            │ C++20 Double      │          │ Physical Entropy  │
│ Reads V & I (10ms) │            │ Auction Engine    │          │ Generator (TRNG)  │
└─────────┬──────────┘            └─────────┬─────────┘          └─────────┬─────────┘
          │                                 │                              │
          │ 1. Telemetry / Order Packet     │                              │
          │    (UDP over Wi-Fi)             │                              │
          ├────────────────────────────────►│                              │
          │                                 │                              │
          │                                 │ 2. Order Matched!            │
          │                                 │    Request Nonce             │
          │                                 ├─────────────────────────────►│
          │                                 │                              │
          │                                 │ 3. Returns 32-Byte TRNG Nonce│
          │                                 │◄─────────────────────────────┤
          │                                 │                              │
          │ 4. TRADE_CLEARED Packet         │                              │
          │    (Contains verified Nonce)    │                              │
          │◄────────────────────────────────┤                              │
          │                                 │                              │
┌─────────┴──────────┐                      │ 5. Live UI Stream (WebSocket)│
│ PHYSICAL GRID MESH │                      ├─────────────────────────────►│
│ Relays click ON    │                      │                              │
│ Current routes!    │                                            ┌────────┴──────────┐
└────────────────────┘                                            │ TRADING TERMINAL  │
                                                                  │ Dark Mode UI      │
                                                                  └───────────────────┘
```

---

## 3. Subsystem Breakdown

### Subsystem A: Autonomous Edge Trading Nodes (`src/firmware/`)
* **Hardware:** ESP32 Dual-Core microcontroller + CJMCU-219 (INA219) sensor.
* **Function:** Samples bus voltage and current every 10ms. 
* **Quoting Logic (AMM):**
  - Deficit state (`Battery SoC < 40%`): Issues aggressive BUY bids into the order book.
  - Surplus state (`Battery SoC > 80%` and Generation > Load): Issues discounted SELL asks.

### Subsystem B: Continuous Double Auction Matching Engine (`src/engine/`)
* **Core:** High-performance C++20 Limit Order Book.
* **Function:** Ingests bids and asks over UDP (port `8888`), maintains price-time priority queues, and crosses matching orders:
  $$\text{Clearing Spot Price} = \frac{\text{Bid} + \text{Ask}}{2}$$

### Subsystem C: Zero-Trust Cryptographic Settlement (`src/entropy/`)
* **Core:** AVX2 SIMD `entropy_core.cpp` engine.
* **Function:** Extracts unrepeatable thermal/optical noise into a 32-byte physical seed in **~39 microseconds**. Binds trade metadata with the seed via HMAC-SHA256 to create a single-use transaction nonce (`TX_ID`).

### Subsystem D: Physical Micro-Grid Switching & Display (`src/dashboard/` & Tabletop Rig)
* **Hardware:** 4-Channel opto-isolated relay module, 6V solar PV cells, battery banks, load resistors.
* **Function:** On receiving a verified `TRADE_CLEARED` packet, relays physically close the DC connection between seller and buyer nodes. The live dashboard plots order book depth and current power flow in real time.

---

## 4. Network Interface Contract (Packet Formats)

All modules talk using standardized **JSON-over-UDP** packets:

### A. Order Packet (From ESP32 to Matching Engine)
```json
{
  "packet_type": "ORDER",
  "node_id": "HOUSE_1",
  "side": "BUY",          // "BUY" or "SELL"
  "quantity_wh": 50,      // Energy packet size in Watt-hours
  "price_inr": 5.40,      // Quoted price in ₹/kWh
  "battery_soc": 38.5,    // Current State-of-Charge in %
  "timestamp_ms": 1731110000000
}
```

### B. Trade Cleared Packet (From Engine to ESP32s)
```json
{
  "packet_type": "TRADE_CLEARED",
  "trade_id": "0x8e2c4b91f03a65de9871bc45ad3e10fa789c02d184bf321876543210abcdef99",
  "seller_node": "HOUSE_3",
  "buyer_node": "HOUSE_1",
  "quantity_wh": 50,
  "clearing_price_inr": 5.45,
  "duration_seconds": 15, // Time relay stays closed
  "nonce_verified": true
}
```

---

## 5. Hardware Wiring & Pinout Reference

### ESP32 to INA219 Current Sensor (I2C)
| ESP32 Pin | INA219 Pin | Notes |
|---|---|---|
| **3.3V** | `VCC` | Logic power |
| **GND** | `GND` | Ground |
| **GPIO 21** | `SDA` | I2C Data line |
| **GPIO 22** | `SCL` | I2C Clock line |
| In-line Shunt | `Vin+` & `Vin-` | In series with Solar (+) and Battery (+) lines |

### ESP32 to 4-Channel Relay Module
| ESP32 Pin | Relay Input | Action When Triggered |
|---|---|---|
| **GPIO 25** | `IN1` (House 1 Grid Tie) | Connects House 1 DC bus to the shared exchange mesh |
| **GPIO 26** | `IN2` (House 2 Grid Tie) | Connects House 2 DC bus to the shared exchange mesh |
| **GPIO 27** | `IN3` (House 3 Grid Tie) | Connects House 3 DC bus to the shared exchange mesh |
| **5V / VIN** | `VCC` (Relay Board) | Powers the mechanical coils |
| **GND** | `GND` | Relay ground |

---

## 6. How to Answer Common Judge Questions (CiiA-6 Cheat Sheet)

* **Judge:** *"Why not just use a blockchain like Ethereum or Solana?"*
  * **Answer:** *"Micro-grid trades involve tiny energy packets (50 Wh worth ₹0.25). Blockchain gas fees cost ₹5 to ₹50 per transaction, completely destroying micro-trade economics. Furthermore, blockchain settlement takes seconds to minutes; our AVX2 entropy engine clears transactions in 39 microseconds with zero transaction costs."*

* **Judge:** *"Why is normal random number generation (`rand()`) not enough?"*
  * **Answer:** *"Standard PRNGs are deterministic algorithms. If an attacker observes consecutive trade IDs, they can deduce the generator's internal state and forge trade authorizations to fraudulently steal power. Our generator harvests quantum optical and thermal physical noise, making prediction mathematically impossible."*

* **Judge:** *"Won't power distribution companies (DISCOMs) oppose this?"*
  * **Answer:** *"No, we designed this with a utility-friendly B2B model: DISCOMs act as the licensed market operator, collecting a 5% clearing fee on every trade while shedding expensive peak transformer congestion."*

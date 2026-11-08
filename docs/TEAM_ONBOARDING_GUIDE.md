# AETHER: Teammate Onboarding & Technical Interface Guide
## Master Playbook for the 4-Person Engineering Team

Welcome to the team! This document gives every team member a crystal-clear understanding of the project, how all our modules fit together, the exact network packet formats to use, and a personalized checklist for your role.

---

## 1. The 30-Second Elevator Pitch (Memorize This!)

> *"AETHER replaces broken net-metering (where people sell solar to the grid at ₹2.50/kWh and buy back at ₹8.00/kWh) with an autonomous peer-to-peer energy exchange. Our ESP32 smart meters use Automated Market Maker algorithms to trade power directly with neighbors at ~₹5.50/kWh. To prevent trade spoofing without using slow, expensive blockchains, we use a C++ physical entropy engine that captures real-world hardware noise to sign every micro-trade with an un-forgeable cryptographic nonce."*

---

## 2. Master System Data Flow

Here is how all 4 team members' work connects in real time:

```
 MEMBER 3 (Firmware)               MEMBER 1 (Matcher)             MEMBER 2 (Security)
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
│ MEMBER 4 (Hardware)│                      ├─────────────────────────────►│
│ Relays click ON    │                      │                              │
│ Current routes!    │                                            ┌────────┴──────────┐
└────────────────────┘                                            │ MEMBER 4 (UI)     │
                                                                  │ Dark Mode Terminal│
                                                                  └───────────────────┘
```

---

## 3. The Interface Contract (Packet Formats)

To ensure we can work independently without breaking each other's code, we agree on standard **JSON-over-UDP** packet formats:

### A. Order Packet (From ESP32 to Matching Engine)
Sent when battery drops below 40% (BUY) or solar generation exceeds load (SELL):
```json
{
  "packet_type": "ORDER",
  "node_id": "HOUSE_1",
  "side": "BUY",          // "BUY" or "SELL"
  "quantity_wh": 50,      // Energy packet in Watt-hours
  "price_inr": 5.40,      // Quoted price in ₹/kWh
  "battery_soc": 38.5,    // Current State-of-Charge in %
  "timestamp_ms": 1731110000000
}
```

### B. Trade Cleared Settlement Packet (From Engine to ESP32s)
Sent when the Continuous Double Auction crosses a bid and an ask:
```json
{
  "packet_type": "TRADE_CLEARED",
  "trade_id": "0x8e2c4b91f03a65de9871bc45ad3e10fa789c02d184bf321876543210abcdef99",
  "seller_node": "HOUSE_3",
  "buyer_node": "HOUSE_1",
  "quantity_wh": 50,
  "clearing_price_inr": 5.45,
  "duration_seconds": 15, // Relay must stay closed for this long
  "nonce_verified": true
}
```

---

## 4. Hardware Wiring & Pinout Guide (For Members 3 & 4)

### ESP32 to INA219 Current Sensor (I2C)
| ESP32 Pin | INA219 Pin | Notes |
|---|---|---|
| **3.3V** | `VCC` | Power logic |
| **GND** | `GND` | Common ground |
| **GPIO 21** | `SDA` | I2C Data line |
| **GPIO 22** | `SCL` | I2C Clock line |
| In-line Shunt | `Vin+` & `Vin-` | Placed in series with Solar (+) and Battery (+) lines |

### ESP32 to 4-Channel Relay Module
| ESP32 Pin | Relay Input | Action When Triggered |
|---|---|---|
| **GPIO 25** | `IN1` (House 1 Grid Tie) | Connects House 1 DC bus to the shared exchange mesh |
| **GPIO 26** | `IN2` (House 2 Grid Tie) | Connects House 2 DC bus to the shared exchange mesh |
| **GPIO 27** | `IN3` (House 3 Grid Tie) | Connects House 3 DC bus to the shared exchange mesh |
| **5V / VIN** | `VCC` (Relay Board) | Powers the mechanical coils |
| **GND** | `GND` | Relay ground |

---

## 5. Team Member Execution Breakdown

### Member 1: Core Exchange Engine (C++20)
* **Folder:** `src/engine/`
* **Responsibilities:**
  - Build the **Continuous Double Auction (CDA)** Limit Order Book.
  - Implement price-time priority matching (highest bid meets lowest ask).
  - Open a UDP socket server listening on port `8888` to ingest order packets.
  - Compute the fair spot price: $\text{Spot Price} = \frac{\text{Bid} + \text{Ask}}{2}$.
  - Dispatch trade triggers to Member 2's entropy module.

### Member 2: Cryptography & Security (C++ / Python)
* **Folder:** `src/entropy/`
* **Responsibilities:**
  - Maintain the AVX2 SIMD `entropy_core.cpp` engine.
  - Ensure optical/audio sensors continuously condition unrepeatable seeds.
  - Format the `TX_ID` digest using `HMAC-SHA256(seed, trade_data)`.
  - Provide an anti-replay cache (bloom filter / hash map) so no trade ID can ever be re-executed.

### Member 3: Embedded Systems & AMM Quant Logic (ESP32)
* **Folder:** `src/firmware/`
* **Responsibilities:**
  - Write ESP32 firmware (Arduino / ESP-IDF) to read bus voltage and current from INA219 every 10ms.
  - Implement the **Automated Market Maker (AMM) logic**:
    - If `Battery SoC < 40%`: Quote high BUY bid (e.g. ₹6.00).
    - If `Battery SoC > 80%` and Solar > Load: Quote discounted SELL ask (e.g. ₹4.50).
  - Connect to local Wi-Fi and broadcast UDP orders.
  - Listen for `TRADE_CLEARED` packets, verify the nonce, and set GPIO pins HIGH/LOW.

### Member 4: Power Electronics, Hardware Rig & UI
* **Folder:** `src/dashboard/` & Physical Rig
* **Responsibilities:**
  - Mount 3 mini solar cells, 3 ESP32 boards, battery packs, and load resistors onto an acrylic tabletop board.
  - Wire the opto-isolated relay module safely so power only flows between matched nodes.
  - Build a dark-mode web or terminal dashboard (Python/React/Tailwind) displaying:
    1. Live Order Book depth chart (bids in green, asks in red).
    2. Power flow diagram (animated lines showing Watts flowing between houses).
    3. Real-time TRNG Nonce logs flashing on every trade.

---

## 6. How to Answer Common Judge Questions (CiiA-6 Cheat Sheet)

* **Judge:** *"Why not just use a blockchain like Ethereum or Solana?"*
  * **Answer:** *"Micro-grid trades involve tiny energy packets (50 Wh worth ₹0.25). Blockchain gas fees cost ₹5 to ₹50 per transaction, completely destroying micro-trade economics. Furthermore, blockchain settlement takes seconds to minutes; our AVX2 entropy engine clears transactions in 39 microseconds with zero transaction costs."*

* **Judge:** *"Why is normal random number generation (`rand()`) not enough?"*
  * **Answer:** *"Standard PRNGs are mathematical algorithms. If an attacker observes consecutive trade IDs, they can calculate the internal seed and forge trade authorizations to fraudulently steal power. Our generator harvests quantum optical and thermal physical noise, making prediction mathematically impossible."*

* **Judge:** *"Won't power distribution companies (DISCOMs) oppose this?"*
  * **Answer:** *"No, we designed this with a utility-friendly B2B model: DISCOMs act as the licensed market operator, collecting a 5% clearing fee on every trade while shedding expensive peak transformer congestion."*

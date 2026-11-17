# DhvaniPay: Offline Sound-Wave Payment Terminal for Feature Phones
### Zero-Internet Digital Rupee (e₹) Micro-POS with Built-In Biometric Protection

[![Hackathon](https://img.shields.io/badge/SciX%20India%20Hackathon-CiiA--6%20Mumbai-blue.svg)](https://scix.in)
[![Category](https://img.shields.io/badge/Category-Engineering%20%7C%20Smart%20Systems-orange.svg)]()
[![Hardware Budget](https://img.shields.io/badge/Prototype%20BOM-%E2%82%B91%2C929-green.svg)]()
[![Communication](https://img.shields.io/badge/Audio%20Data-18--20%20kHz%20Sound%20Waves-red.svg)]()
[![Security](https://img.shields.io/badge/Anti--Fraud-Hardware%20Odometer%20Counter-purple.svg)]()

---

## 1. Project Overview & The Big Idea
**DhvaniPay** is an ultra-low-cost (**₹1,929**) physical payment terminal designed for rural Indian shops, weekly village markets (*mandis*), and network blackout zones. 

While urban India runs on UPI QR codes, over **25 crore (250 million) Indians** still use ₹1,000 basic keypad feature phones (like JioBharat or Nokia 105). These phones **cannot scan QR codes** (they have no camera or a very low-res one) and **cannot tap-to-pay** (they lack expensive NFC chips). Furthermore, when mobile towers drop in remote areas or during heavy rains, even smartphones fail completely.

**Our Core Breakthrough:**
Every phone ever manufactured—from a ₹1,000 basic keypad phone to an iPhone—has two universal components: **a speaker and a microphone**. 

DhvaniPay uses **safe, near-ultrasonic sound waves (18–20 kHz)** to transfer encrypted Digital Rupee (e₹) payments through thin air. You do **not** need cellular data, Wi-Fi, or Bluetooth. 

---

## 2. How It Solves the Two Biggest Problems

### Problem 1: No Internet & Feature Phone Exclusion
* **Today's Reality:** UPI requires 4G/5G data. Tap-to-pay cards require expensive NFC chips. If network drops, commerce stops.
* **DhvaniPay Solution:** Sound waves travel through the air. The customer’s phone plays a 1-second encrypted audio chirp (inaudible to human ears) into the terminal's microphone. Payment is completed in 1.2 seconds with **zero internet connection**.

### Problem 2: The "Double-Spending" Fraud
* **The Danger:** When there is no bank server online, what stops someone from spending the same ₹500 at three different village shops before reconnecting?
* **DhvaniPay Solution (Hardware Odometer):** Just like a car's mechanical odometer only rolls forward and cannot be turned back, our terminal uses a **tamper-proof hardware counter inside the chip's physical memory**. Every transaction permanently ticks this counter forward (+1) and seals it with a cryptographic lock. If someone tries to replay an old payment sound recording, the terminal rejects it instantly because the counter number is already spent.

---

## 3. Hardware Prototype & Cost (Total BOM: ₹1,929)

Built entirely with components readily available across Indian electronics stores:

| Component | Function in Simple Words | Unit Price (INR) |
|---|---|---|
| **ESP32 Dual-Core Microcontroller** | The brain: decodes sound waves and verifies payment tokens | ₹499 |
| **R307 Optical Fingerprint Scanner** | Fast thumbprint verification directly on the machine in <1 second | ₹719 |
| **16x2 LCD Display with I2C** | Clear screen showing "₹50 PAID - OFFLINE VERIFIED" | ₹212 |
| **MAX9814 Microphone + Mini Speaker** | Ears and mouth: listens for and plays high-frequency sound waves | ₹319 |
| **4x4 Keypad & Enclosure Box** | Numeric buttons for shopkeeper to type amount, plus sturdy case | ₹180 |
| **Total Prototype Hardware Cost** | **Complete Standalone Physical Terminal** | **₹1,929** |

---

## 4. The 60-Second Live Exhibition Demo (CiiA-6 Mumbai)
1. The judge puts their smartphone or a ₹1,000 Nokia keypad phone into **Airplane Mode** (completely disabling 4G/5G, Wi-Fi, and Bluetooth).
2. The merchant enters `₹50` on the DhvaniPay keypad.
3. The customer touches the optical fingerprint scanner on the terminal to authorize the payment.
4. The phone plays a short, near-silent 1-second ultrasonic chirp.
5. The terminal's screen immediately flashes: **"₹50 RECEIVED · OFFLINE SUCCESS"** and displays the remaining balance.
6. The entire payment settles offline in **1.2 seconds** without a single byte of cellular data used!

---

## 5. Team DEADCODE (VNIT Nagpur)
* **Raj Patil** (Embedded Firmware, Security & Audio DSP)
* **Nakul Yawalkar** (Hardware Integration & System Architecture)
* **Soumik Das** (Mathematical Modeling & Cryptographic Logic)
* **Laksh Kachure** (Circuit Assembly, Power Design & Enclosure)

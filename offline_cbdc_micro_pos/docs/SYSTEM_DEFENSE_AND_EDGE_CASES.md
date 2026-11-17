# DhvaniPay: System Defense Dossier & Edge-Case Engineering
## Technical Defense Guide for Evaluator Q&A and Viva (CiiA-6 & SciX)

---

### Question 1: What if the market is extremely noisy with vegetable vendors shouting and horns honking?
* **Defense:**
  1. **Acoustic Separation:** Human speech, shouting, and vehicle horns operate at low frequencies, virtually all below **4 kHz to 8 kHz**.
  2. **High-Frequency Band (18 kHz – 20 kHz):** DhvaniPay operates in the near-ultrasound band (18.5 kHz and 19.5 kHz). There is almost zero acoustic energy at 18+ kHz in natural market environments.
  3. **Auto-Gain Pre-Amplifier (MAX9814):** The microphone module features hardware Automatic Gain Control (AGC) that compresses loud background noise while amplifying faint high-frequency tones.
  4. **Goertzel Tone Filtering:** The ESP32 executes a narrow digital filter that only measures energy at the exact target frequencies (±50 Hz window), completely ignoring background noise.

---

### Question 2: What stops an attacker from recording the payment sound and playing it again to steal money (Replay Attack)?
* **Defense:**
  1. **Two-Way Random Challenge Handshake:** Before the phone chirps, the merchant terminal generates a random, single-use 8-byte challenge code. The phone includes this challenge inside its encrypted sound packet.
  2. **Hardware "Odometer" (Monotonic Counter):** Inside the ESP32's non-volatile memory, an irreversible counter ticks forward (+1) for every transaction. 
  3. **Instant Rejection:** If someone records the chirp and plays it back 10 seconds later, the terminal checks its counter: that transaction number and challenge code are already recorded as spent. The terminal immediately beeps an error and displays **"INVALID TOKEN: REPLAY REJECTED"**.

---

### Question 3: Can high-frequency sound waves hurt human hearing or disturb street animals/pets?
* **Defense:**
  1. **Volume Capped at 65 dB SPL:** Standard conversation is 60–70 dB. DhvaniPay chirps at a gentle ~65 dB for only **1.2 seconds**.
  2. **Safety Standards:** Occupational safety limits (such as OSHA) permit continuous exposure up to 85 dB for 8 hours. A 1.2-second pulse at 65 dB is completely safe and painless.
  3. **Frequency Threshold:** Most adult humans cannot hear sounds above 16–17 kHz, making the payment chirp essentially silent and non-intrusive.

---

### Question 4: How does the merchant eventually convert offline tokens into actual money in their bank account?
* **Defense:**
  1. **Local Cryptographic Ledger:** Each approved payment generates a compact 64-byte signed cryptographic receipt stored in the terminal's flash memory.
  2. **End-of-Day Batch Sync:** When the merchant returns home or gets near a Wi-Fi connection / cellular hotspot (even once a day or once a week), the terminal automatically connects and uploads the accumulated batch of receipts to the bank or RBI e₹ gateway.
  3. **Lightweight Merkle Tree:** Instead of sending hundreds of separate files, the terminal aggregates all daily transactions into a single compact cryptographic root hash (under 2 KB), settling thousands of rupees in seconds.

---

### Question 5: What if the merchant terminal runs out of battery?
* **Defense:**
  1. **Low Power Consumption:** The ESP32, LCD, and mic consume under 120 mA during active listening and drop to deep sleep (<5 mA) between transactions.
  2. **Standard 18650 Battery / Mobile Power Bank:** The device is powered by a standard 3.7V 18650 rechargeable lithium cell or can be plugged into any standard ₹500 mobile power bank via USB-C, providing **over 48 hours of continuous operation** on a single charge.

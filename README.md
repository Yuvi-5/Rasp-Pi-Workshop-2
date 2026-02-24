# Workshop II: From Processing Core to Edge Interaction

**Brought to you by Circuit Revival | [cite_start]Delivered by Yuvraj** [cite: 2, 13, 14]

Welcome to the second workshop in our Raspberry Pi series. This session focuses on moving beyond the processor to interact with the physical world using the Grove ecosystem and Python.

## 🎯 Workshop Goals
* **The Foundation:** Understand Raspberry Pi 5 architecture and the Grove Base Hat[cite: 3, 20].
* [cite_start]**The Toolkit:** Master 7 modular components (Sensors & Actuators)[cite: 4].
* [cite_start]**The Objective:** Master `grove.py` for Edge Devices[cite: 5].
* **Final Project:** Build a "Red Light, Green Light" Tournament system[cite: 204].

---

## 🛠 Hardware Checklist
This workshop utilizes the **Raspberry Pi 5** and the **Grove Base Hat** to bridge digital processing with physical interaction[cite: 20, 52].

### The Bridge
* [cite_start]**Grove Base Hat:** Adds an ADC (Analog-to-Digital Converter) to the purely digital Raspberry Pi, enabling analog sensors[cite: 52, 96].

### The Modules (Inputs & Outputs)
1.  [cite_start]**Visual Output:** 16x2 LCD Display (I2C)[cite: 100].
2.  [cite_start]**Spatial Sensing:** Ultrasonic Ranger (Digital)[cite: 112].
3.  [cite_start]**Physical Actuation:** Servo Motor (PWM)[cite: 125].
4.  [cite_start]**Environmental Sensing:** Light Sensor (Analog)[cite: 140].
5.  [cite_start]**Presence Detection:** Mini PIR Motion Sensor (Digital)[cite: 148].
6.  [cite_start]**Audio Output:** Buzzer (PWM/Digital)[cite: 156].
7.  [cite_start]**Interactive Input:** Red LED Button (Digital Composite)[cite: 163].

---

## 💻 Environment Setup

### OS & Libraries
[cite_start]We are using **Raspberry Pi OS (Debian Bookworm)**[cite: 41].

### Installation
Open your terminal on the Pi and clone the `grove.py` library. [cite_start]This library treats complex hardware behaviors as simple Python objects[cite: 43].

```bash
cd ~
git clone [https://github.com/Seeed-Studio/grove.py](https://github.com/Seeed-Studio/grove.py)

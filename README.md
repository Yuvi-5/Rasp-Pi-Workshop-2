# Workshop II: From Processing Core to Edge Interaction

**Brought to you by Circuit Revival | Delivered by Yuvraj** 

Welcome to the second workshop in our Raspberry Pi series. This session focuses on moving beyond the processor to interact with the physical world using the Grove ecosystem and Python.

## 🎯 Workshop Goals
* **The Foundation:** Understand Raspberry Pi 5 architecture and the Grove Base Hat.
* **The Toolkit:** Master 7 modular components (Sensors & Actuators).
* **The Objective:** Master `grove.py` for Edge Devices.
* **Final Project:** Build a "Red Light, Green Light" Tournament system.

---

## 🛠 Hardware Checklist
This workshop utilizes the **Raspberry Pi 5** and the **Grove Base Hat** to bridge digital processing with physical interaction.

### The Bridge
* **Grove Base Hat:** Adds an ADC (Analog-to-Digital Converter) to the purely digital Raspberry Pi, enabling analog sensors.

### The Modules (Inputs & Outputs)
1.  Visual Output:** 16x2 LCD Display (I2C).
2.  **Spatial Sensing:** Ultrasonic Ranger (Digital).
3.  **Physical Actuation:** Servo Motor (PWM).
4.  **Environmental Sensing:** Light Sensor (Analog).
5.  **Presence Detection:** Mini PIR Motion Sensor (Digital).
6.  **Audio Output:** Buzzer (PWM/Digital).
7.  **Interactive Input:** Red LED Button (Digital Composite).

---

## 💻 Environment Setup

### OS & Libraries
We are using **Raspberry Pi OS (Debian Bookworm)**.

### Installation
Open your terminal on the Pi and clone the `grove.py` library. This library treats complex hardware behaviors as simple Python objects.

```bash
cd ~
git clone [https://github.com/Seeed-Studio/grove.py](https://github.com/Seeed-Studio/grove.py)
```
## 🏆 Final Project: Red Light, Green Light Tournament

The hardware is ready. The logic is yours to write. 

Combine the modules to create a "Squid Game" inspired reflex test system.      
System LogicInput (Sense) $\rightarrow$ Logic (Python) $\rightarrow$ Output (Act)   
Motion Sensor (Input): Detects player movement.  
LCD Display (Output): Shows "Red Light" or "Green Light" status.  
Servo Motor (Output): Rotates a "head" or indicator to face the players.  
Buzzer (Output): Alarms when motion is detected during a Red Light.  

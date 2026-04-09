# 🤖 Autonomous Agri-Bot Simulator

An interactive robotics simulation of an autonomous agricultural robot with real-time obstacle avoidance, A* pathfinding, and a 4-directional ultrasonic sensor array. Built to demonstrate embedded systems logic applied to precision agriculture — bridging software programming with real-world robotics concepts.

---

## 🎥 Live Demo

**[https://agri-bot-simulator-vai886w2qfb9bmntapppcr.streamlit.app/](#)**

Press **START** to watch the bot autonomously navigate a field, avoid obstacles, and harvest all crops.

---

## 🔬 What It Does

This project simulates the core decision-making architecture of a real agricultural robot:

**Sensor Input → Obstacle Detection → Pathfinding Algorithm → Motor Output**

Every 280ms, the bot's sensor array polls all four directions. When a path is blocked, the A* algorithm recalculates the optimal route in real time — exactly how an Arduino or Raspberry Pi processes ultrasonic sensor signals to control motor drivers and wheel movement.

---

## 🧠 Robotics & Embedded Systems Concepts Demonstrated

| Simulation Component | Real Hardware Equivalent |
|---|---|
| 4-directional sensor array | HC-SR04 ultrasonic sensors on GPIO pins |
| 280ms polling interval | Microcontroller interrupt/timer cycle |
| A* pathfinding algorithm | Navigation logic running on Arduino Mega / Raspberry Pi |
| CLEAR / BLOCKED status | Digital HIGH / LOW sensor readings |
| Path recalculation on obstacle | Motor driver signal change (L298N / L293D) |
| Crop harvesting trigger | Servo actuator or solenoid activation |
| Telemetry display | Serial monitor / OLED display output |

> In a physical build, this Python/JavaScript logic maps directly to C++ on Arduino or Python on Raspberry Pi — the same conditional sensor-to-action flow, just running on real hardware.

---

## ✨ Features

- **Live A\* Pathfinding** — optimal route calculated to each crop target, updated in real time
- **4-Directional Ultrasonic Sensor Array** — shows CLEAR/BLOCKED status per direction every frame
- **Autonomous Mission Logic** — bot harvests crops one by one, replanning after each collection
- **Bot Telemetry Panel** — live position, path steps remaining, algorithm, and update rate
- **System Log** — timestamped navigation events and harvest confirmations
- **Interactive Controls** — Start, Pause, Resume, and Reset the mission at any time
- **Visual Field Grid** — colour-coded cells for bot position, obstacles, crops, explored area, and planned path

---

## 🌾 Why Agriculture?

Precision agriculture is one of the most impactful applications of robotics in the African context. Autonomous bots can:

- Reduce labour costs for smallholder farmers
- Enable targeted crop monitoring and harvesting
- Operate in conditions hazardous or inaccessible to humans

This project was built with that real-world application in mind — not just as a technical exercise, but as a demonstration of how embedded systems can solve problems relevant to Nigeria and the wider African agricultural sector.

---

## 🛠 Built With

- React (Hooks — useState, useEffect, useRef, useCallback)
- A* Search Algorithm (custom implementation)
- CSS animations for real-time visual feedback
- No external dependencies beyond React

---

## 🚀 Run Locally

```bash
git clone https://github.com/asiyasabiu25/agri-bot-simulator.git
cd agri-bot-simulator
npm install
npm start
```

---

## 🔌 Physical Implementation Roadmap

To build this as a real robot, the software logic maps to:

```
Raspberry Pi / Arduino Mega
├── HC-SR04 Ultrasonic Sensors (x4) → GPIO input pins
├── L298N Motor Driver → GPIO output pins
├── DC Motors (x2) → differential drive
├── Python / C++ navigation script → this A* logic
└── OLED display → telemetry output (optional)
```

Estimated BOM cost: ~₦25,000–40,000 for a functional prototype.

---

## 👩🏾‍💻 About the Developer

**Asiya Sabiu Sulaiman** — Data Analytics, Health Technology & Embedded Systems

- B.Sc. Human Physiology, Bayero University Kano
- 3MTT Data Science & Machine Learning Certificate
- Microsoft Business Analyst Professional Certificate (Coursera)
- McKinsey Forward Programme 2026
- Digital Literacy Facilitator — trained 200+ students across northern Nigeria (DL4ALL / NITDA)

This project was built as part of my preparation to facilitate the **Buildathon 4th Edition** Robotics & Embedded Systems workshop — demonstrating that strong software programming fundamentals, combined with a clear understanding of how code maps to hardware, are the foundation of effective robotics education.

🔗 [Portfolio](https://asiyasabiu25.github.io/Data-Science-Portfolio) · [GitHub](https://github.com/asiyasabiu25) · [LinkedIn](https://linkedin.com/in/asiya-sabiu) · [Vital Signs Monitor](https://github.com/asiyasabiu25/vital-signs-monitor)

---

## 📄 License

MIT — free to use, adapt, and build on.

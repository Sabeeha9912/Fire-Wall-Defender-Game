# Firewall Defender 🛡️👾

An interactive, 2D network security simulator built in Python using Pygame. This project visually translates enterprise-level infrastructure defense concepts into an active tactical triage gameplay loop.

---

 Cyber Security Concepts Demonstrated

As a **Cyber Security** student/professional, this game was developed to gamify and demonstrate fundamental network security mechanics:

* **Inbound Packet Filtering:** The player operates the primary firewall stateful inspection engine, evaluating incoming data traffic blocks and determining which data safely passes to the internal network stack.
* **Signature-Based Malware Detection:** Threat blocks (`virus_icon`) represent known malicious signature payloads. These must be blocked immediately at the network boundary before they can breach system integrity and deplete health resources.
* **Heuristic Analysis (Zero-Day Threats):** Encrypted or ambiguous packets (`unknown_icon`) simulate unknown traffic data. The player must actively utilize a limited threat intelligence/hint decryptor to classify whether the incoming stream is benign or an active exploit.
* **Denial of Service (DoS) Risk:** Letting malicious packets pass or dropping legitimate traffic simulates an active network compromise, causing system downtime and an eventual service crash (**Game Over**).

---Tech Stack & Requirements

* **Language:** Python 3.x
* **Core Library:** Pygame (Built using Object-Oriented Architecture)

### Prerequisites
Make sure you have `pygame` installed on your architecture before deploying the simulator:
```bash
pip install pygame

# QR Phishing Awareness Lab

A safe cybersecurity awareness lab demonstrating how QR-code phishing attacks, also known as Quishing, can trick users into visiting fake login pages.

This project is built strictly for:

- Cybersecurity education
- Awareness training
- Defensive research
- Authorized lab testing

No real credential collection or malicious functionality is included.

---

# Features

- QR code generation
- Fake awareness login page
- Warning simulation page
- Local web server testing
- Beginner-friendly project structure
- Safe cybersecurity training environment

---

# Technologies Used

- HTML5
- CSS3
- Python
- QRCode Library
- VS Code
- Git & GitHub

---

# Project Structure

```text
qr-phishing-awareness-lab/
│
├── assets/
│   └── qr-demo.png
│
├── screenshots/
│
├── docs/
│
├── index.html
├── warning.html
├── style.css
├── generate_qr.py
├── README.md
└── .gitignore
````md
# QR Phishing Awareness Lab

A safe cybersecurity awareness lab demonstrating how QR-code phishing attacks, also known as Quishing, can trick users into visiting fake login pages.

This project is built strictly for:

- Cybersecurity education
- Awareness training
- Defensive research
- Authorized lab testing

No real credential collection or malicious functionality is included.

---

# Features

- QR code generation
- Fake awareness login page
- Warning simulation page
- Local web server testing
- Beginner-friendly project structure
- Safe cybersecurity training environment

---

# Technologies Used

- HTML5
- CSS3
- Python
- QRCode Library
- VS Code
- Git & GitHub

---

# Project Structure

```text
qr-phishing-awareness-lab/
│
├── assets/
│   └── qr-demo.png
│
├── screenshots/
│
├── docs/
│
├── index.html
├── warning.html
├── style.css
├── generate_qr.py
├── README.md
└── .gitignore
````

---

# How to Run

## Start Local Server

```bash
python -m http.server 8080
```

Open browser:

```text
http://127.0.0.1:8080
```

---

# Generate QR Code

Install dependency:

```bash
pip install qrcode[pil]
```

Run:

```bash
python generate_qr.py
```

Generated QR code will be saved in:

```text
assets/qr-demo.png
```

---

# Testing on Mobile Device

1. Connect laptop and phone to same Wi-Fi
2. Find local IPv4 address using:

```bash
ipconfig
```

3. Update the URL inside:

```python
generate_qr.py
```

Example:

```python
url = "http://192.168.1.5:8080"
```

4. Generate QR code again
5. Scan using phone camera

---

# Awareness Simulation

The project demonstrates:

* QR-based phishing attacks
* Fake login page redirection
* User awareness concepts
* Safe browsing practices
* QR security risks

---

# Security Disclaimer

This repository is created strictly for educational and defensive cybersecurity purposes.

Do not use these techniques against systems, users, or networks without explicit authorization.

The author is not responsible for misuse of this project.

---

# Future Improvements

* Flask backend integration
* Admin dashboard
* Mobile responsive UI
* Cyber-themed animations
* Docker deployment
* Awareness analytics
* SIEM integration examples

---

# Author

Shaan
Aspiring Cybersecurity Enthusiast 🛡️

GitHub:
[https://github.com/shaan150406-svg](https://github.com/shaan150406-svg)

```
```

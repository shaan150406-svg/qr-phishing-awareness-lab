# generate_correct_qr.py
import qrcode

# REPLACE THIS with your actual IP address from Step 1
YOUR_COMPUTER_IP = "192.168.1.100"  # ← CHANGE THIS!

# Generate QR code with your computer's IP
url = "http://10.118.221.78:5000/qr-login"
qr = qrcode.make(url)
qr.save('static/img/qr-demo.png')

print(f"✅ QR Code updated!")
print(f"📱 Scan this with your phone: {url}")
print(f"⚠️ Make sure your phone and computer are on the SAME Wi-Fi network")
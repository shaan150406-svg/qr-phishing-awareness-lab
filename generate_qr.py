import qrcode

url = "http://10.118.221.78:8080"
img = qrcode.make(url)

img.save("assets/qr-demo.png")

print("QR Code Generated Successfully")
import qrcode
from PIL import Image

# Your app URL
url = "https://publicpulse.streamlit.app"

# Generate QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Create with colors
img = qr.make_image(fill_color="#1e3a8a", back_color="white")

# Save
img.save("public_pulse_qr.png")
print("✅ QR Code saved as public_pulse_qr.png!")
print(f"📱 Scan to open: {url}")
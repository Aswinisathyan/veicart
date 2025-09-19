from ultralytics import YOLO
import cv2
import sqlite3

# -------------------
# Database Connection
# -------------------
conn = sqlite3.connect("items.db")
cursor = conn.cursor()

# Fetch all valid database items
cursor.execute("SELECT name, price FROM products")
database_items = {row[0]: row[1] for row in cursor.fetchall()}

# -------------------
# Load YOLO model
# -------------------
model = YOLO("yolov8n.pt")

# -------------------
# Cart for items
# -------------------
cart = []

# -------------------
# Open webcam
# -------------------
cap = cv2.VideoCapture(0)
print("Press 'a' to add detected item to bill, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame,conf=0.4)
    annotated = results[0].plot()
    cv2.imshow("VEICART Detection", annotated)

    if len(results[0].boxes) > 0:
        # Get all detected items
        detected_items = [results[0].names[int(box.cls)] for box in results[0].boxes]
        
        # Keep only database items
        valid_items = [item for item in detected_items if item in database_items]

        if valid_items:
            item = valid_items[0]
            print(f"Detected: {item}")

            key = cv2.waitKey(1) & 0xFF

            if key == ord('a'):
                price_per_kg = database_items[item]
                weight = float(input(f"Enter weight (kg) for {item}: "))
                cost = weight * price_per_kg
                cart.append((item, weight, cost))
                print(f"✅ {item} added. Price: ₹{cost:.2f}")

    # Quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()

# -------------------
# Final Bill
# -------------------
print("\n🧾 Final Bill:")
total = 0
for item, weight, cost in cart:
    print(f"{item} - {weight} kg - ₹{cost:.2f}")
    total += cost
print(f"Total: ₹{total:.2f}")

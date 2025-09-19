import streamlit as st
from ultralytics import YOLO
import sqlite3
import pandas as pd
import cv2
import numpy as np
import qrcode
from PIL import Image
import io

# -----------------------
# Database connection
# -----------------------
conn = sqlite3.connect("items.db")
cursor = conn.cursor()
cursor.execute("SELECT name, price FROM products")
database_items = {row[0]: row[1] for row in cursor.fetchall()}

# -----------------------
# Load YOLO model
# -----------------------
model = YOLO("yolov8n.pt")

# -----------------------
# Session state
# -----------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "detected_items" not in st.session_state:
    st.session_state.detected_items = []

# -----------------------
# Page layout
# -----------------------
st.set_page_config(page_title="🍎 VEICART - Smart Market Checkout", layout="wide")
st.markdown("<h1 style='text-align:center; color:green;'>🍏 VEICART - Smart Fruits & Veggies Checkout</h1>", unsafe_allow_html=True)

# -----------------------
# Layout: three columns
# -----------------------
col1, col2, col3 = st.columns([3, 2, 2])

# -----------------------
# Column 1: Camera and detection
# -----------------------
with col1:
    st.subheader("📸 Live Item Detection")
    uploaded_file = st.camera_input("Place your items in front of the camera")
    
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        results = model(frame)
        annotated_frame = results[0].plot()
        st.image(annotated_frame, channels="BGR")

        if len(results[0].boxes) > 0:
            detected = [results[0].names[int(box.cls)] for box in results[0].boxes]
            # Keep only **unique items**
            valid_items = list(set([item for item in detected if item in database_items]))
            st.session_state.detected_items = valid_items
            if valid_items:
                st.success(f"Detected Items: {', '.join(valid_items)}")
            else:
                st.warning("No valid items detected in the database.")

# -----------------------
# Column 2: Add detected items to cart (styled)

with col2:
    st.subheader("🛒 Add Detected Items")

    if st.session_state.detected_items:
        for idx, item in enumerate(st.session_state.detected_items):
            with st.container():
                col_item, col_input, col_button = st.columns([2, 2, 1])

                # Column 1: Item name and price
                with col_item:
                    st.markdown(f"### 🥬 {item}")
                    st.markdown(f"**Price:** ₹{database_items[item]}/kg")

                # Column 2: Weight input
                with col_input:
                    # If item is already in cart, prefill the weight
                    existing = next((c for c in st.session_state.cart if c["item"] == item), None)
                    initial_weight = existing["weight"] if existing else 0.01
                    weight = st.number_input(
                        f"Weight (kg) for {item}",
                        min_value=0.01,
                        step=0.01,
                        format="%.2f",
                        value=initial_weight,
                        key=f"{item}_{idx}"
                    )

                # Column 3: Add/Update button
                with col_button:
                    if st.button(f"➕ Add/Update", key=f"add_{item}_{idx}"):
                        cost = weight * database_items[item]
                        if existing:
                            existing["weight"] = weight
                            existing["cost"] = cost
                            st.success(f"Updated {item}: {weight} kg → ₹{cost:.2f}")
                        else:
                            st.session_state.cart.append({"item": item, "weight": weight, "cost": cost})
                            st.success(f"Added {item} ({weight} kg) → ₹{cost:.2f}")
    else:
        st.info("No items detected yet. Place items in front of the camera.")

# -----------------------
# Column 3: Cart & payment
# -----------------------
with col3:
    st.subheader("🧾 Your Cart")

    if st.session_state.cart:
        df = pd.DataFrame(st.session_state.cart)
        st.table(df)

        remove_item = st.selectbox("Remove Item", [c["item"] for c in st.session_state.cart])
        if st.button("➖ Remove"):
            st.session_state.cart = [c for c in st.session_state.cart if c["item"] != remove_item]
            st.warning(f"Removed {remove_item}")

        total = sum(c["cost"] for c in st.session_state.cart)
        st.success(f"💰 Total: ₹{total:.2f}")

        payee_vpa = "sreeaswini3@oksbi"
        payee_name = "VEICART"
        transaction_note = "Bill Payment"
        upi_link = f"upi://pay?pa={payee_vpa}&pn={payee_name}&am={total}&cu=INR&tn={transaction_note}"

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(upi_link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        st.subheader("📲 Scan to Pay via UPI")
        st.image(buf)
        st.caption(f"Amount: ₹{total:.2f}")
    else:
        st.info("Your cart is empty. Detected items will appear here.")

# Veicart

Veicart is an intelligent checkout system designed for groceries, specifically fruits and vegetables. It combines **object detection** and **weight measurement** to automate the billing process, making checkout faster and more accurate. 

## Features

- **Object Detection**: Uses AI (YOLOv8) to identify fruits and vegetables placed on the counter.
- **Weight Measurement**: Integrates with a digital scale (HX711 + Load Cell) to calculate the weight of each item.
- **Automated Billing**: Combines object recognition and weight to generate the total price automatically.
- **User-Friendly Dashboard**: Displays detected items, weights, and prices in real-time.

## How It Works

1. Customer places items on the scale.
2. The system detects each item using **YOLOv8 object detection**.
3. The weight of the item is measured using a connected **load cell sensor**.
4. The total price is calculated and displayed on the dashboard.

## Technologies Used

- Python
- Streamlit (for dashboard)
- YOLOv8 (object detection)
- HX711 Load Cell (weight sensor)
- SQLite (for storing item prices and transactions)

## Benefits

- Speeds up the checkout process.
- Reduces human error in billing.
- Can be deployed in grocery stores, supermarkets, or farmers' markets.


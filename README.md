# 🦶 Smart Diabetic Foot Ulcer Monitoring System

## 📌 Overview

The **Smart Diabetic Foot Ulcer Monitoring System** is an IoT-based healthcare solution designed to monitor foot pressure, temperature, and derived skin moisture to predict early signs of diabetic foot ulcers.

The system uses **smart insoles embedded with sensors**, **ESP32 microcontrollers**, and a **machine learning model** to analyze foot conditions in real-time and provide a **health percentage score**.

---

## 🎯 Objective

- Monitor foot pressure distribution continuously  
- Detect abnormal pressure patterns  
- Predict risk of foot ulcer formation  
- Provide real-time health insights  
- Enable preventive healthcare using AI  

---

## 🚀 Features

- 👟 Smart insole with multiple pressure sensors  
- 🌡️ Skin temperature monitoring  
- 💧 Skin Moisture Index (SMI) calculation  
- 📡 Wireless data transmission (WiFi)  
- 🧠 Machine Learning-based prediction  
- 📊 Real-time data logging (CSV/Excel)  
- ⚠️ Disconnection detection (Left/Right shoe)  
- 🖥️ Interactive UI for monitoring  

---

## 🏗️ System Architecture

[FSR Sensors + Temp Sensor]
↓
ESP32 (Left Shoe)
↓
WiFi (TCP/IP)
↓
Python Server
↓
Data Processing + ML Model
↓
UI Dashboard


(Same architecture for Right Shoe)

---

## 🔧 Hardware Components

| Component | Quantity |
|----------|---------|
| ESP32 | 2 |
| FSR Sensors | 8 (4 per shoe) |
| DS18B20 Temperature Sensor | 2 |
| Resistors (4.7kΩ) | 10 |
| Shoes / Insoles | 1 pair |

---

## 💻 Software Technologies

- Python 3.x  
- Pandas  
- NumPy  
- Scikit-learn  
- Socket Programming  
- Tkinter (UI)  
- Arduino IDE  

---

## 🌐 Communication

- WiFi-based communication  
- TCP Socket connection  
- Static IP configuration for ESP32  

---

## 📊 Data Collection

### 👤 User Inputs
- Name  
- Age  
- Gender  
- Weight  
- Height  

### 🧾 Sensor Data
- Left Foot: Heel, Midfoot, Ball, Toe  
- Right Foot: Heel, Midfoot, Ball, Toe  
- Skin Temperature  

### 📈 Derived Data
- Skin Moisture Index (SMI)

---

## 🧠 Machine Learning Model

### 🔹 Model Name:
**Foot Health Prediction Model**

### 🔹 Algorithm Used:
- Random Forest Regression

### 🔹 Input Features:
- Pressure values (FSR sensors)  
- Skin Temperature  
- SMI  
- Age, Weight, Height  

### 🔹 Output:
- Foot Health Score (0–100%)

---


## Author
Jaya Prasad, 
IoT and Embedded Systems Engineer

---

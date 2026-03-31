import socket
import time
import requests
import joblib
import numpy as np

# ---------------- ESP32 CONFIG ----------------

LEFT_IP = "192.168.31.200"
RIGHT_IP = "192.168.31.201"
PORT = 80

# ---------------- WEATHER CONFIG ----------------

API_KEY = "open_weather_api_eky"

LAT = 10.7870
LON = 79.1378


# ---------------- LOAD MODEL ----------------  

model = joblib.load("foot_health_model.pkl")
scaler = joblib.load("scaler.pkl")

print("AI model loaded successfully")


# ---------------- WEATHER FUNCTION ----------------

def get_weather():

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

    r = requests.get(url)

    data = r.json()

    env_temp = data["main"]["temp"]
    env_humidity = data["main"]["humidity"]

    return env_temp, env_humidity


# ---------------- SENSOR READ FUNCTION ----------------

def get_data(ip):

    try:

        s = socket.socket()
        s.settimeout(2)

        s.connect((ip, PORT))

        data = s.recv(1024).decode().strip()

        s.close()

        return data

    except:

        return None


# ---------------- USER DETAILS ----------------

print("\nENTER USER DETAILS\n")

age = float(input("Age: "))
weight = float(input("Weight (kg): "))
height = float(input("Height (cm): "))

gender_input = input("Gender (Male/Female): ")

if gender_input.lower() == "male":
    gender = 1
else:
    gender = 0


# ---------------- CHECK SHOE CONNECTION ----------------

print("\nChecking shoe connections...\n")

while True:

    left = get_data(LEFT_IP)
    right = get_data(RIGHT_IP)

    if left:
        print("LEFT SHOE CONNECTED")

    if right:
        print("RIGHT SHOE CONNECTED")

    if left and right:
        print("\nBoth shoes connected successfully\n")
        break

    print("Waiting for both shoes...\n")
    time.sleep(2)


# ---------------- GET WEATHER ----------------

env_temp, env_humidity = get_weather()

print("Environment temperature:", env_temp)
print("Environment humidity:", env_humidity)


# ---------------- REAL TIME MONITOR ----------------

print("\nStarting real-time foot health monitoring...\n")


while True:

    left_data = get_data(LEFT_IP)
    right_data = get_data(RIGHT_IP)

    if left_data is None:
        print("WARNING: LEFT SHOE DISCONNECTED")
        continue

    if right_data is None:
        print("WARNING: RIGHT SHOE DISCONNECTED")
        continue


    # ---------------- PARSE SENSOR DATA ----------------

    l = left_data.split(",")
    r = right_data.split(",")

    Left_Heel = int(l[0])
    Left_Midfoot = int(l[1])
    Left_Ball = int(l[2])
    Left_Toe = int(l[3])

    Right_Heel = int(r[0])
    Right_Midfoot = int(r[1])
    Right_Ball = int(r[2])
    Right_Toe = int(r[3])

    left_temp = float(l[4])
    right_temp = float(r[4])

    Skin_Temp = (left_temp + right_temp) / 2


    # ---------------- CALCULATE SMI ----------------

    SMI = ((Skin_Temp - env_temp) / 10) * env_humidity


    # ---------------- PRESSURE FEATURES ----------------

    Left_Total = (
        Left_Heel +
        Left_Midfoot +
        Left_Ball +
        Left_Toe
    )

    Right_Total = (
        Right_Heel +
        Right_Midfoot +
        Right_Ball +
        Right_Toe
    )

    Pressure_Difference = abs(Left_Total - Right_Total)

    if Left_Total > 0:
        Left_Heel_ratio = Left_Heel / Left_Total
    else:
        Left_Heel_ratio = 0

    if Right_Total > 0:
        Right_Heel_ratio = Right_Heel / Right_Total
    else:
        Right_Heel_ratio = 0


    # ---------------- PREPARE ML INPUT ----------------

    sample = [[

        age,
        weight,
        height,
        gender,

        Left_Heel,
        Left_Ball,
        Right_Heel,
        Right_Ball,

        Skin_Temp,
        SMI,

        Left_Heel_ratio,
        Right_Heel_ratio,

        Pressure_Difference

    ]]


    sample_scaled = scaler.transform(sample)

    prediction = model.predict(sample_scaled)

    health_score = round(prediction[0],2)


    # ---------------- HEALTH INTERPRETATION ----------------

    if health_score > 90:
        status = "Healthy Foot"

    elif health_score > 75:
        status = "Minor Pressure Imbalance"

    elif health_score > 50:
        status = "Moderate Ulcer Risk"

    else:
        status = "HIGH ULCER RISK"


    # ---------------- PRINT RESULT ----------------

    print("\n----------------------------")

    print("Left Heel:", Left_Heel,
          "Right Heel:", Right_Heel)

    print("Skin Temperature:", round(Skin_Temp,2))

    print("SMI:", round(SMI,2))

    print("Foot Health Score:", health_score,"%")

    print("Status:", status)

    print("----------------------------")

    time.sleep(1)

import socket
import requests
import joblib
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------- CONFIG ----------------

LEFT_IP = "192.168.31.200"
RIGHT_IP = "192.168.31.201"
PORT = 80

API_KEY = "open_weather_api_key"
LAT = 10.7870
LON = 79.1378


# ---------------- LOAD MODEL ----------------

model = joblib.load("foot_health_model.pkl")
scaler = joblib.load("scaler.pkl")


# ---------------- WEATHER ----------------

def get_weather():

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

    r = requests.get(url)

    data = r.json()

    return data["main"]["temp"], data["main"]["humidity"]


env_temp, env_humidity = get_weather()


# ---------------- SOCKET ----------------

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


# ---------------- UI ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Insole Health Monitoring")
app.geometry("1100x700")


# ---------------- LEFT PANEL ----------------

left_frame = ctk.CTkFrame(app,width=300)
left_frame.pack(side="left",fill="y",padx=10,pady=10)


ctk.CTkLabel(left_frame,text="User Information",font=("Arial",18)).pack(pady=10)

age_entry = ctk.CTkEntry(left_frame,placeholder_text="Age")
age_entry.pack(pady=5)

weight_entry = ctk.CTkEntry(left_frame,placeholder_text="Weight (kg)")
weight_entry.pack(pady=5)

height_entry = ctk.CTkEntry(left_frame,placeholder_text="Height (cm)")
height_entry.pack(pady=5)

gender_box = ctk.CTkComboBox(left_frame,values=["Male","Female"])
gender_box.pack(pady=5)


health_label = ctk.CTkLabel(left_frame,text="Health Score: --",font=("Arial",20))
health_label.pack(pady=20)

status_label = ctk.CTkLabel(left_frame,text="Status: --",font=("Arial",16))
status_label.pack(pady=10)


# ---------------- PRESSURE MAP ----------------

fig, ax = plt.subplots(figsize=(5,6))

canvas = FigureCanvasTkAgg(fig,master=app)
canvas.get_tk_widget().pack(side="right",fill="both",expand=True)


# ---------------- DRAW MAP ----------------

def draw_map(LH,LM,LB,LT,RH,RM,RB,RT):

    ax.clear()

    left_points=[(-1,-2,LH),(-1,-1,LM),(-1,1,LB),(-1,2,LT)]
    right_points=[(1,-2,RH),(1,-1,RM),(1,1,RB),(1,2,RT)]

    for x,y,v in left_points:

        color="blue"

        if v>100:
            color="yellow"

        if v>250:
            color="red"

        ax.scatter(x,y,s=1200,c=color)

        ax.text(x,y,str(v),ha="center",va="center",color="white")


    for x,y,v in right_points:

        color="blue"

        if v>100:
            color="yellow"

        if v>250:
            color="red"

        ax.scatter(x,y,s=1200,c=color)

        ax.text(x,y,str(v),ha="center",va="center",color="white")


    ax.set_xlim(-2,2)
    ax.set_ylim(-3,3)

    ax.set_title("Foot Pressure Map")

    ax.axis("off")

    canvas.draw()


# ---------------- MONITOR FUNCTION ----------------

def monitor():

    age=float(age_entry.get())
    weight=float(weight_entry.get())
    height=float(height_entry.get())

    gender=1 if gender_box.get()=="Male" else 0


    left=get_data(LEFT_IP)
    right=get_data(RIGHT_IP)

    if left is None or right is None:

        status_label.configure(text="Shoe disconnected")

        app.after(1000,monitor)

        return


    l=left.split(",")
    r=right.split(",")

    LH=int(l[0])
    LM=int(l[1])
    LB=int(l[2])
    LT=int(l[3])

    RH=int(r[0])
    RM=int(r[1])
    RB=int(r[2])
    RT=int(r[3])

    left_temp=float(l[4])
    right_temp=float(r[4])

    skin_temp=(left_temp+right_temp)/2


    sensors=[LH,LM,LB,LT,RH,RM,RB,RT]

    active=sum(1 for s in sensors if s>=2)

    if active<2:

        status_label.configure(text="Person not wearing shoe")

        draw_map(LH,LM,LB,LT,RH,RM,RB,RT)

        app.after(1000,monitor)

        return


    SMI=((skin_temp-env_temp)/10)*env_humidity


    left_total=LH+LM+LB+LT
    right_total=RH+RM+RB+RT

    pressure_diff=abs(left_total-right_total)

    left_ratio=LH/left_total if left_total>0 else 0
    right_ratio=RH/right_total if right_total>0 else 0


    sample=[[

    age,
    weight,
    height,
    gender,

    LH,
    LB,
    RH,
    RB,

    skin_temp,
    SMI,

    left_ratio,
    right_ratio,

    pressure_diff

    ]]


    sample_scaled=scaler.transform(sample)

    health=model.predict(sample_scaled)[0]


    health_label.configure(text=f"Health Score: {health:.2f}%")


    if health>90:
        status="Healthy"

    elif health>75:
        status="Minor Imbalance"

    elif health>50:
        status="Moderate Risk"

    else:
        status="High Ulcer Risk"


    status_label.configure(text="Status: "+status)


    draw_map(LH,LM,LB,LT,RH,RM,RB,RT)

    app.after(1000,monitor)


# ---------------- SUBMIT BUTTON ----------------

submit_btn = ctk.CTkButton(left_frame,text="Submit & Start Monitoring",command=monitor)
submit_btn.pack(pady=20)


app.mainloop()

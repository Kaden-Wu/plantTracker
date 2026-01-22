import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from plant import Plant
from datetime import datetime, timedelta
import pymysql

plants = {}                 
currentPlant = None         
editMode = False            
currentScreen = "H"         
reminder_list = []          

#PyMySQL Database
try:
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="Ziggy1989!",
        database="plant_tracker",
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = db.cursor()
    print("Connected to MySQL")

except Exception as err:
    print("Database connection failed:", err)
    db = None
    cursor = None

def loadPlantsFromDB():
    if not cursor:
        print("No database connection")
        return

    try:
        cursor.execute("SELECT * FROM plants")
        rows = cursor.fetchall()

        for row in rows:
            plant = Plant(
                row["name"],
                row["water_hours"],
                row["sunlight_hours"]
            )

            plant.last_watered = row["last_watered"]
            plant.last_rotated = row["last_rotated"]

            plants[plant.name] = plant

        print(f"Loaded {len(plants)} plants from database")

    except Exception as e:
        print("Error loading plants:", e)

def db_insert_plant(plant):
    if not cursor:
        return

    cursor.execute(
        """
        INSERT INTO plants (name, water_hours, sunlight_hours, last_watered, last_rotated)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            plant.name,
            plant.water,
            plant.sunlight,
            plant.last_watered,
            plant.last_rotated
        )
    )
    db.commit()


def db_update_plant(old_name, plant):
    if not cursor:
        return

    cursor.execute(
        """S
        UPDATE plants
        SET name=%s,
            water_hours=%s,
            sunlight_hours=%s,
            last_watered=%s,
            last_rotated=%s
        WHERE name=%s
        """,
        (
            plant.name,
            plant.water,
            plant.sunlight,
            plant.last_watered,
            plant.last_rotated,
            old_name
        )
    )
    db.commit()


def db_delete_plant(name):
    if not cursor:
        return

    cursor.execute(
        "DELETE FROM plants WHERE name=%s",
        (name,)
    )
    db.commit()

root = tk.Tk()
root.title("Plant Tracker")
root.geometry("1920x1080")

home = tk.Frame(root)
header = tk.Frame(root)
plantLibrary = tk.Frame(root)
toDo = tk.Frame(root)
reminders = tk.Frame(root)

home.place(relx=0, rely=0, relwidth=1, relheight=1)
header.place(relx=0, rely=0, relwidth=1, relheight=1)
plantLibrary.place(relx=0, y=200, relwidth=1, relheight=1)
toDo.place(relx=0, y=200, relwidth=1, relheight=1)
reminders.place(relx=0, y=200, relwidth=1, relheight=1)

home.tkraise()

def on_screen_switch(button_id):
    if currentScreen == "PL" and button_id == "A":
        swap_header(0)
    elif currentScreen == "PL" and button_id == "B":
        swap_header(2)
    elif currentScreen == "PL" and button_id == "C":
        swap_header(3)

    elif currentScreen == "TD" and button_id == "A":
        swap_header(1)
    elif currentScreen == "TD" and button_id == "B":
        swap_header(0)
    elif currentScreen == "TD" and button_id == "C":
        swap_header(3)

    elif currentScreen == "R" and button_id == "A":
        swap_header(1)
    elif currentScreen == "R" and button_id == "B":
        swap_header(2)
    elif currentScreen == "R" and button_id == "C":
        swap_header(0)

    elif currentScreen == "H" and button_id == "A":
        swap_header(1)
    elif currentScreen == "H" and button_id == "B":
        swap_header(2)
    elif currentScreen == "H" and button_id == "C":
        swap_header(3)

    else:
        print(f"Unknown navigation: {currentScreen}, {button_id}")

#Home Screen 

titleLabel = tk.Label(
    home,
    text="PLANT TRACKER",
    height=1,
    bg="#36ad53",
    fg="white",
    font=("Helvetica", 100)
)
titleLabel.pack(fill="both")

PLButtonFrame = tk.Frame(home, height=200, width=800)
PLButtonFrame.place(x=550, y=200)

PLButton = tk.Button(
    PLButtonFrame,
    text="Plant Library",
    bg="#286a26",
    fg="white",
    font=("Helvetica", 80),
    width=13,
    command=lambda: on_screen_switch("A")
)
PLButton.pack()

TDButtonFrame = tk.Frame(home, height=200, width=800)
TDButtonFrame.place(x=550, y=450)

TDButton = tk.Button(
    TDButtonFrame,
    text="To-Do List",
    bg="#286a26",
    fg="white",
    font=("Helvetica", 80),
    width=13,
    command=lambda: on_screen_switch("B")
)
TDButton.pack()

RButtonFrame = tk.Frame(home, height=200, width=800)
RButtonFrame.place(x=550, y=700)

RButton = tk.Button(
    RButtonFrame,
    text="Reminders",
    bg="#286a26",
    fg="white",
    font=("Helvetica", 80),
    width=13,
    command=lambda: on_screen_switch("C")
)
RButton.pack()

#Header Bar

HLabel = tk.Label(
    header,
    text="placeholder",
    bg="#36ad53",
    fg="white",
    font=("Helvetica", 63)
)
HLabel.pack(fill="both")

AHeaderFrame = tk.Frame(header, height=100, width=640)
AHeaderFrame.place(x=0, y=100)

AHeader = tk.Button(
    AHeaderFrame,
    bg="#286a26",
    fg="white",
    font=("Helvetica", 40),
    width=21,
    command=lambda: on_screen_switch("A")
)
AHeader.pack()

BHeaderFrame = tk.Frame(header, height=100, width=640)
BHeaderFrame.place(x=640, y=100)

BHeader = tk.Button(
    BHeaderFrame,
    bg="#286a26",
    fg="white",
    font=("Helvetica", 40),
    width=21,
    command=lambda: on_screen_switch("B")
)
BHeader.pack()

CHeaderFrame = tk.Frame(header, height=100, width=640)
CHeaderFrame.place(x=1280, y=100)

CHeader = tk.Button(
    CHeaderFrame,
    bg="#286a26",
    fg="white",
    font=("Helvetica", 40),
    width=21,
    command=lambda: on_screen_switch("C")
)
CHeader.pack()

def swap_header(page):
    global currentScreen

    if page == 0:
        currentScreen = "H"
        home.tkraise()

    elif page == 1:
        currentScreen = "PL"
        HLabel.config(text="Plant Library")
        AHeader.config(text="Home")
        BHeader.config(text="To-Do List")
        CHeader.config(text="Reminders")
        header.tkraise()
        plantLibrary.tkraise()

    elif page == 2:
        currentScreen = "TD"
        HLabel.config(text="To-Do List")
        AHeader.config(text="Plant Library")
        BHeader.config(text="Home")
        CHeader.config(text="Reminders")
        header.tkraise()
        toDo.tkraise()
        generateTodoTasks()

    elif page == 3:
        currentScreen = "R"
        HLabel.config(text="Reminders")
        AHeader.config(text="Plant Library")
        BHeader.config(text="To-Do List")
        CHeader.config(text="Home")
        header.tkraise()
        reminders.tkraise()

#Plant Library 

plant_buttons = []

def open_plant_detail(plant_name):
    global currentPlant
    plant = plants.get(plant_name)
    if not plant:
        return

    currentPlant = plant
    PD_title.config(text=plant.name)
    PD_water.config(text=f"Water every: {plant.water} hours")
    PD_sun.config(text=f"Rotate every: {plant.sunlight} hours")
    plantDetailFrame.place(x=400, y=200)

def add_plant_button(plant_name):
    btn = tk.Button(
        plantButtonFrame,
        text=plant_name,
        anchor="w",
        font=("Helvetica", 30),
        bg="#DFF5D8",
        relief="flat",
        command=lambda n=plant_name: open_plant_detail(n)
    )
    btn.pack(fill="x", padx=20, pady=5)
    plant_buttons.append(btn)

def PLAraise():
    PLAframe.place(x=600, y=60)

def addPlant():
    global editMode

    name = pn.get()
    water = pw.get()
    sun = ps.get()

    if not name:
        return

    if editMode:
        old_name = currentPlant.name
        if old_name != name:
            plants.pop(old_name)
            plants[name] = currentPlant

        currentPlant.name = name
        currentPlant.water = water
        currentPlant.sunlight = sun

        refreshPlantButtons()
        db_update_plant(old_name, currentPlant)

        editMode = False
        PLAconfirm.config(text="CONFIRM")
        plantDetailFrame.place_forget()
    else:
        plant = Plant(name, water, sun)
        plants[name] = plant
        add_plant_button(name)
        db_insert_plant(plant)

    PLAframe.place_forget()
    pn.delete(0, tk.END)
    pw.delete(0, tk.END)
    ps.delete(0, tk.END)

    generateTodoTasks()

def refreshPlantButtons():
    for widget in plantButtonFrame.winfo_children():
        widget.destroy()

    plant_buttons.clear()

    for name in plants:
        add_plant_button(name)

def cancel():
    global editMode
    editMode = False

    PLAconfirm.config(text="CONFIRM")
    PLAframe.place_forget()

    pn.delete(0, tk.END)
    pw.delete(0, tk.END)
    ps.delete(0, tk.END)

def update_scrollregion(event):
    plantCanvas.configure(scrollregion=plantCanvas.bbox("all"))


def editPlant():
    global editMode

    if not currentPlant:
        return

    editMode = True

    pn.delete(0, tk.END)
    pn.insert(0, currentPlant.name)

    pw.delete(0, tk.END)
    pw.insert(0, currentPlant.water)

    ps.delete(0, tk.END)
    ps.insert(0, currentPlant.sunlight)

    PLAconfirm.config(text="SAVE")
    PLAframe.place(x=600, y=60)
    PLAframe.tkraise()

def deletePlant():
    global currentPlant, editMode

    if not currentPlant:
        return

    confirm = messagebox.askyesno(
        "Delete Plant",
        f"Are you sure you want to delete {currentPlant.name}?"
    )

    if not confirm:
        return

    db_delete_plant(currentPlant.name)
    plants.pop(currentPlant.name, None)

    currentPlant = None
    editMode = False

    plantDetailFrame.place_forget()
    refreshPlantButtons()
    PLAbutton.place(x=40, y=680)

    generateTodoTasks()

plantListContainer = tk.Frame(plantLibrary, bg="white", bd=2, relief="solid")
plantListContainer.place(x=40, y=40, width=1830, height=600)

plantCanvas = tk.Canvas(
    plantListContainer,
    bg="#DFF5D8",
    highlightthickness=0
)
plantCanvas.pack(side="left", fill="both", expand=True)

plantScrollbar = tk.Scrollbar(
    plantListContainer,
    orient="vertical",
    command=plantCanvas.yview
)
plantScrollbar.pack(side="right", fill="y")

plantCanvas.configure(yscrollcommand=plantScrollbar.set)

plantButtonFrame = tk.Frame(plantCanvas, bg="#DFF5D8")
plantCanvas.create_window((0, 0), window=plantButtonFrame, anchor="nw")

plantButtonFrame.bind("<Configure>", update_scrollregion)

def _on_mousewheel(event):
    plantCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

plantCanvas.bind_all("<MouseWheel>", _on_mousewheel)

PLAbutton = tk.Button(
    plantLibrary,
    text="Add Plant",
    bg="green",
    fg="white",
    font=("Helvetica", 40),
    width=10,
    command=PLAraise
)
PLAbutton.place(x=40, y=680)

#Add Plant 

PLAframe = tk.Frame(plantLibrary, width=730, height=600, bg="#E8E8E8")

PLAname = tk.Label(
    PLAframe,
    text="Enter Plant Name:",
    font=("Helvetica", 40),
    bg="#E8E8E8"
)
PLAname.place(x=10, y=10)

pn = tk.Entry(PLAframe, bg="grey", font=("Helvetica", 40))
pn.place(x=10, y=80)

PLAwater = tk.Label(
    PLAframe,
    text="Enter Water Requirements:",
    font=("Helvetica", 40),
    bg="#E8E8E8"
)
PLAwater.place(x=10, y=180)

pw = tk.Entry(PLAframe, bg="grey", font=("Helvetica", 40))
pw.place(x=10, y=250)

PLAsun = tk.Label(
    PLAframe,
    text="Enter Sunlight Requirements:",
    font=("Helvetica", 40),
    bg="#E8E8E8"
)
PLAsun.place(x=10, y=350)

ps = tk.Entry(PLAframe, bg="grey", font=("Helvetica", 40))
ps.place(x=10, y=420)

PLAconfirm = tk.Button(
    PLAframe,
    text="CONFIRM",
    bg="green",
    fg="white",
    font=("Helvetica", 20),
    width=10,
    command=addPlant
)
PLAconfirm.place(x=10, y=500)

PLAcancel = tk.Button(
    PLAframe,
    text="CANCEL",
    bg="red",
    fg="white",
    font=("Helvetica", 20),
    width=10,
    command=cancel
)
PLAcancel.place(x=200, y=500)

PLAframe.place_forget()

#Plant Detail

plantDetailFrame = tk.Frame(
    plantLibrary,
    bg="#E8E8E8",
    bd=3,
    relief="solid",
    width=1000,
    height=600
)
plantDetailFrame.place_forget()

PD_title = tk.Label(
    plantDetailFrame,
    text="Plant Name",
    font=("Helvetica", 50),
    bg="#E8E8E8"
)
PD_title.pack(pady=30)

PD_water = tk.Label(
    plantDetailFrame,
    text="Water every: X days",
    font=("Helvetica", 35),
    bg="#E8E8E8"
)
PD_water.pack(pady=15)

PD_sun = tk.Label(
    plantDetailFrame,
    text="Rotate every: X days",
    font=("Helvetica", 35),
    bg="#E8E8E8"
)
PD_sun.pack(pady=15)

PD_buttonFrame = tk.Frame(plantDetailFrame, bg="#E8E8E8")
PD_buttonFrame.pack(side="bottom", pady=40)

PD_back = tk.Button(
    PD_buttonFrame,
    text="BACK",
    bg="#286a26",
    fg="white",
    font=("Helvetica", 30),
    width=10,
    command=lambda: (
        plantDetailFrame.place_forget(),
        PLAbutton.place(x=40, y=680)
    )
)
PD_back.grid(row=0, column=0, padx=20)

PD_edit = tk.Button(
    PD_buttonFrame,
    text="EDIT",
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 30),
    width=10,
    command=editPlant
)
PD_edit.grid(row=0, column=1, padx=20)

PD_delete = tk.Button(
    PD_buttonFrame,
    text="DELETE",
    bg="red",
    fg="white",
    font=("Helvetica", 30),
    width=10,
    command=deletePlant
)
PD_delete.grid(row=0, column=2, padx=20)

#To-Do List

todoContainer = tk.Frame(toDo, bg="white", bd=2, relief="solid")
todoContainer.place(x=40, y=40, width=1800, height=700)

todoCanvas = tk.Canvas(
    todoContainer,
    bg="#F5FFF5",
    highlightthickness=0
)
todoCanvas.pack(side="left", fill="both", expand=True)

todoScrollbar = tk.Scrollbar(
    todoContainer,
    orient="vertical",
    command=todoCanvas.yview
)
todoScrollbar.pack(side="right", fill="y")

todoCanvas.configure(yscrollcommand=todoScrollbar.set)

todoFrame = tk.Frame(todoCanvas, bg="#F5FFF5")
todoCanvas.create_window((0, 0), window=todoFrame, anchor="nw")

todoFrame.bind(
    "<Configure>",
    lambda e: todoCanvas.configure(scrollregion=todoCanvas.bbox("all"))
)

def _on_mousewheel_scroll(event):
    todoCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

todoCanvas.bind_all("<MouseWheel>", _on_mousewheel_scroll)

def generateTodoTasks():
    for widget in todoFrame.winfo_children():
        widget.destroy()

    now = datetime.now()
    tasks = []

    for plant in plants.values():
        tasks.append((plant.next_water_date(), plant, "water"))
        tasks.append((plant.next_rotate_date(), plant, "rotate"))

    tasks.sort(key=lambda x: x[0])

    for due_date, plant, task_type in tasks:
        hours_left = int((due_date - now).total_seconds() // 3600)

        if task_type == "water":
            text = f"Water {plant.name}"
        else:
            text = f"Rotate {plant.name}"

        if hours_left < 0:
            label_text = f"{text} — OVERDUE"
            fg = "red"
        else:
            label_text = f"{text} — due in {hours_left} hours"
            fg = "black"

        row = tk.Frame(todoFrame, bg="#F5FFF5")
        row.pack(fill="x", padx=20, pady=8)

        task_label = tk.Label(
            row,
            text=label_text,
            font=("Helvetica", 28),
            bg="#F5FFF5",
            fg=fg,
            anchor="w"
        )
        task_label.pack(side="left", fill="x", expand=True)

        check_button = tk.Button(
            row,
            text="○",
            font=("Helvetica", 30),
            bg="#F5FFF5",
            relief="flat"
        )

        check_button.config(
            command=lambda r=row, b=check_button, p=plant, t=task_type:
            completeTask(r, b, p, t)
        )
        check_button.pack(side="right")

def completeTask(row, button, plant, task_type):
    row.config(bg="#E0E0E0")

    for widget in row.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(fg="grey", bg="#E0E0E0")

    button.config(
        text="●",
        fg="grey",
        state="disabled",
        bg="#E0E0E0"
    )

    now = datetime.now()

    if task_type == "water":
        plant.last_watered = now
    elif task_type == "rotate":
        plant.last_rotated = now

    db_update_plant(plant.name, plant)
    
    root.after(600, generateTodoTasks)

# Reminders 

def check_reminders():
    now = datetime.now()

    for reminder in reminder_list:
        if (
            reminder["enabled"]
            and not reminder["triggered"]
            and now >= reminder["time"]
        ):
            reminder["triggered"] = True
            messagebox.showinfo("Plant Reminder", reminder["message"])

    root.after(30000, check_reminders)

def addReminder(remind_time, message):
    reminder_list.append({
        "time": remind_time,
        "message": message,
        "enabled": True,
        "triggered": False
    })
    refreshReminderList()

reminderTitle = tk.Label(
    reminders,
    text="Add Reminder",
    font=("Helvetica", 40),
    bg="white"
)
reminderTitle.place(x=40, y=40)

timeLabel = tk.Label(
    reminders,
    text="Time (HH:MM)",
    font=("Helvetica", 30)
)
timeLabel.place(x=40, y=120)

timeEntry = tk.Entry(
    reminders,
    font=("Helvetica", 30)
)
timeEntry.place(x=300, y=120)

msgLabel = tk.Label(
    reminders,
    text="Message",
    font=("Helvetica", 30)
)
msgLabel.place(x=40, y=200)

msgEntry = tk.Entry(
    reminders,
    font=("Helvetica", 30),
    width=25
)
msgEntry.place(x=300, y=200)

def submitReminder():
    try:
        time_str = timeEntry.get()
        hour, minute = map(int, time_str.split(":"))

        remind_time = datetime.now().replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        if remind_time < datetime.now():
            remind_time += timedelta(days=1)

        message = msgEntry.get()
        addReminder(remind_time, message)

        messagebox.showinfo("Reminder Set", "Reminder successfully added!")

        timeEntry.delete(0, tk.END)
        msgEntry.delete(0, tk.END)

    except:
        messagebox.showerror("Error", "Invalid time format (HH:MM)")

addReminderBtn = tk.Button(
    reminders,
    text="Add Reminder",
    font=("Helvetica", 30),
    bg="green",
    fg="white",
    command=submitReminder
)
addReminderBtn.place(x=40, y=300)

reminderContainer = tk.Frame(reminders, bg="white", bd=2, relief="solid")
reminderContainer.place(x=40, y=400, width=1800, height=400)

reminderCanvas = tk.Canvas(
    reminderContainer,
    bg="#F5FFF5",
    highlightthickness=0
)
reminderCanvas.pack(side="left", fill="both", expand=True)

reminderScrollbar = tk.Scrollbar(
    reminderContainer,
    orient="vertical",
    command=reminderCanvas.yview
)
reminderScrollbar.pack(side="right", fill="y")

reminderCanvas.configure(yscrollcommand=reminderScrollbar.set)

reminderFrame = tk.Frame(reminderCanvas, bg="#F5FFF5")
reminderCanvas.create_window((0, 0), window=reminderFrame, anchor="nw")

reminderFrame.bind(
    "<Configure>",
    lambda e: reminderCanvas.configure(scrollregion=reminderCanvas.bbox("all"))
)

def refreshReminderList():
    for widget in reminderFrame.winfo_children():
        widget.destroy()

    for reminder in reminder_list:
        row = tk.Frame(reminderFrame, bg="#F5FFF5")
        row.pack(fill="x", padx=20, pady=10)

        time_label = tk.Label(
            row,
            text=reminder["time"].strftime("%I:%M %p"),
            font=("Helvetica", 26),
            width=10,
            anchor="w",
            bg="#F5FFF5"
        )
        time_label.pack(side="left")

        msg_label = tk.Label(
            row,
            text=reminder["message"],
            font=("Helvetica", 26),
            bg="#F5FFF5",
            anchor="w"
        )
        msg_label.pack(side="left", fill="x", expand=True)

        toggle_btn = tk.Button(
            row,
            text="ON" if reminder["enabled"] else "OFF",
            font=("Helvetica", 22),
            width=6,
            bg="#8BC34A" if reminder["enabled"] else "grey",
            command=lambda r=reminder: toggleReminder(r)
        )
        toggle_btn.pack(side="right")

def toggleReminder(reminder):
    reminder["enabled"] = not reminder["enabled"]
    refreshReminderList()

check_reminders()
loadPlantsFromDB()
refreshPlantButtons()
generateTodoTasks()
print("program started")
root.mainloop()
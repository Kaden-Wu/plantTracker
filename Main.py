import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from plant import Plant
from datetime import datetime, timedelta
import pymysql

plants = {}                 
currentPlant = None         
editMode = False            
currentScreen = "h"         
reminderList = []          

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

def dbInsertPlant(plant):
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


def dbUpdatePlant(oldName, plant):
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
            oldName
        )
    )
    db.commit()


def dbDeletePlant(name):
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
todo = tk.Frame(root)
reminders = tk.Frame(root)

home.place(relx=0, rely=0, relwidth=1, relheight=1)
header.place(relx=0, rely=0, relwidth=1, relheight=1)
plantLibrary.place(relx=0, y=200, relwidth=1, relheight=1)
todo.place(relx=0, y=200, relwidth=1, relheight=1)
reminders.place(relx=0, y=200, relwidth=1, relheight=1)

home.tkraise()

def onScreenSwitch(button_id):
    if currentScreen == "pl" and button_id == "A":
        swapHeader(0)
    elif currentScreen == "pl" and button_id == "B":
        swapHeader(2)
    elif currentScreen == "pl" and button_id == "C":
        swapHeader(3)

    elif currentScreen == "td" and button_id == "A":
        swapHeader(1)
    elif currentScreen == "td" and button_id == "B":
        swapHeader(0)
    elif currentScreen == "td" and button_id == "C":
        swapHeader(3)

    elif currentScreen == "r" and button_id == "A":
        swapHeader(1)
    elif currentScreen == "r" and button_id == "B":
        swapHeader(2)
    elif currentScreen == "r" and button_id == "C":
        swapHeader(0)

    elif currentScreen == "h" and button_id == "A":
        swapHeader(1)
    elif currentScreen == "h" and button_id == "B":
        swapHeader(2)
    elif currentScreen == "h" and button_id == "C":
        swapHeader(3)

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

plantLibraryButtonFrame = tk.Frame(home, height=200, width=800)
plantLibraryButtonFrame.place(x=550, y=200)

plantLibraryButton = tk.Button(
    plantLibraryButtonFrame,
    text="Plant Library",
    bg="#286a26",
    fg="white",
    font=("Helvetica", 80),
    width=13,
    command=lambda: onScreenSwitch("A")
)
plantLibraryButton.pack()

todoButtonFrame = tk.Frame(home, height=200, width=800)
todoButtonFrame.place(x=550, y=450)

todoButton = tk.Button(
    todoButtonFrame,
    text="To-Do List",
    bg="#286a26",
    fg="white",
    font=("Helvetica", 80),
    width=13,
    command=lambda: onScreenSwitch("B")
)
todoButton.pack()

remindersButtonFrame = tk.Frame(home, height=200, width=800)
remindersButtonFrame.place(x=550, y=700)

remindersButton = tk.Button(
    remindersButtonFrame,
    text="Reminders",
    bg="#286a26",
    fg="white",
    font=("Helvetica", 80),
    width=13,
    command=lambda: onScreenSwitch("C")
)
remindersButton.pack()

#Header Bar

headerLabel = tk.Label(
    header,
    text="placeholder",
    bg="#36ad53",
    fg="white",
    font=("Helvetica", 63)
)
headerLabel.pack(fill="both")

aHeaderFrame = tk.Frame(header, height=100, width=640)
aHeaderFrame.place(x=0, y=100)

aHeader = tk.Button(
    aHeaderFrame,
    bg="#286a26",
    fg="white",
    font=("Helvetica", 40),
    width=21,
    command=lambda: onScreenSwitch("A")
)
aHeader.pack()

bHeaderFrame = tk.Frame(header, height=100, width=640)
bHeaderFrame.place(x=640, y=100)

bHeader = tk.Button(
    bHeaderFrame,
    bg="#286a26",
    fg="white",
    font=("Helvetica", 40),
    width=21,
    command=lambda: onScreenSwitch("B")
)
bHeader.pack()

cHeaderFrame = tk.Frame(header, height=100, width=640)
cHeaderFrame.place(x=1280, y=100)

cHeader = tk.Button(
    cHeaderFrame,
    bg="#286a26",
    fg="white",
    font=("Helvetica", 40),
    width=21,
    command=lambda: onScreenSwitch("C")
)
cHeader.pack()

def swapHeader(page):
    global currentScreen

    if page == 0:
        currentScreen = "h"
        home.tkraise()

    elif page == 1:
        currentScreen = "pl"
        headerLabel.config(text="Plant Library")
        aHeader.config(text="Home")
        bHeader.config(text="To-Do List")
        cHeader.config(text="Reminders")
        header.tkraise()
        plantLibrary.tkraise()

    elif page == 2:
        currentScreen = "td"
        headerLabel.config(text="To-Do List")
        aHeader.config(text="Plant Library")
        bHeader.config(text="Home")
        cHeader.config(text="Reminders")
        header.tkraise()
        todo.tkraise()
        generateTodoTasks()

    elif page == 3:
        currentScreen = "r"
        headerLabel.config(text="Reminders")
        aHeader.config(text="Plant Library")
        bHeader.config(text="To-Do List")
        cHeader.config(text="Home")
        header.tkraise()
        reminders.tkraise()

#plant Library 

plantButtons = []

def openPlantDetail(plantName):
    global currentPlant
    plant = plants.get(plantName)
    if not plant:
        return

    currentPlant = plant
    plantDetailTitle.config(text=plant.name)
    plantDetailWater.config(text=f"Water every: {plant.water} hours")
    plantDetailSun.config(text=f"Rotate every: {plant.sunlight} hours")
    plantDetailFrame.place(x=400, y=200)

def addPlantButton(plantName):
    button = tk.Button(
        plantButtonFrame,
        text=plantName,
        anchor="w",
        font=("Helvetica", 30),
        bg="#DFF5D8",
        relief="flat",
        command=lambda n=plantName: openPlantDetail(n)
    )
    button.pack(fill="x", padx=20, pady=5)
    plantButtons.append(button)

def plantLibraryAddRaise():
    plantLibraryAddFrame.place(x=600, y=60)

def addPlant():
    global editMode

    name = plantName.get()
    water = plantWater.get()
    sun = plantSun.get()

    if not name:
        return

    if editMode:
        oldName = currentPlant.name
        if oldName != name:
            plants.pop(oldName)
            plants[name] = currentPlant

        currentPlant.name = name
        currentPlant.water = water
        currentPlant.sunlight = sun

        refreshPlantButtons()
        dbUpdatePlant(oldName, currentPlant)

        editMode = False
        plantLibraryAddConfirm.config(text="CONFIRM")
        plantDetailFrame.place_forget()
    else:
        plant = Plant(name, water, sun)
        plants[name] = plant
        addPlantButton(name)
        dbInsertPlant(plant)

    plantLibraryAddFrame.place_forget()
    plantName.delete(0, tk.END)
    plantWater.delete(0, tk.END)
    plantSun.delete(0, tk.END)

    generateTodoTasks()

def refreshPlantButtons():
    for widget in plantButtonFrame.winfo_children():
        widget.destroy()

    plantButtons.clear()

    for name in plants:
        addPlantButton(name)

def cancel():
    global editMode
    editMode = False

    plantLibraryAddConfirm.config(text="CONFIRM")
    plantLibraryAddFrame.place_forget()

    plantName.delete(0, tk.END)
    plantWater.delete(0, tk.END)
    plantSun.delete(0, tk.END)

def updateScrollRegion(event):
    plantCanvas.configure(scrollregion=plantCanvas.bbox("all"))


def editPlant():
    global editMode

    if not currentPlant:
        return

    editMode = True

    plantName.delete(0, tk.END)
    plantName.insert(0, currentPlant.name)

    plantWater.delete(0, tk.END)
    plantWater.insert(0, currentPlant.water)

    plantSun.delete(0, tk.END)
    plantSun.insert(0, currentPlant.sunlight)

    plantLibraryAddConfirm.config(text="SAVE")
    plantLibraryAddFrame.place(x=600, y=60)
    plantLibraryAddFrame.tkraise()

def deletePlant():
    global currentPlant, editMode

    if not currentPlant:
        return

    confirm = messagebox.askyesno(
        "Delete plant",
        f"Are you sure you want to delete {currentPlant.name}?"
    )

    if not confirm:
        return

    dbDeletePlant(currentPlant.name)
    plants.pop(currentPlant.name, None)

    currentPlant = None
    editMode = False

    plantDetailFrame.place_forget()
    refreshPlantButtons()
    plantLibraryAddButton.place(x=40, y=680)

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

plantButtonFrame.bind("<Configure>", updateScrollRegion)

def onMousewheel(event):
    plantCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

plantCanvas.bind_all("<MouseWheel>", onMousewheel)

plantLibraryAddButton = tk.Button(
    plantLibrary,
    text="Add plant",
    bg="green",
    fg="white",
    font=("Helvetica", 40),
    width=10,
    command=plantLibraryAddRaise
)
plantLibraryAddButton.place(x=40, y=680)

#Add plant 

plantLibraryAddFrame = tk.Frame(plantLibrary, width=730, height=600, bg="#E8E8E8")

plantLibraryAddName = tk.Label(
    plantLibraryAddFrame,
    text="Enter Plant Name:",
    font=("Helvetica", 40),
    bg="#E8E8E8"
)
plantLibraryAddName.place(x=10, y=10)

plantName = tk.Entry(plantLibraryAddFrame, bg="grey", font=("Helvetica", 40))
plantName.place(x=10, y=80)

plantLibraryAddWater = tk.Label(
    plantLibraryAddFrame,
    text="Enter Water Requirements:",
    font=("Helvetica", 40),
    bg="#E8E8E8"
)
plantLibraryAddWater.place(x=10, y=180)

plantWater = tk.Entry(plantLibraryAddFrame, bg="grey", font=("Helvetica", 40))
plantWater.place(x=10, y=250)

plantLibraryAddSun = tk.Label(
    plantLibraryAddFrame,
    text="Enter Sunlight Requirements:",
    font=("Helvetica", 40),
    bg="#E8E8E8"
)
plantLibraryAddSun.place(x=10, y=350)

plantSun = tk.Entry(plantLibraryAddFrame, bg="grey", font=("Helvetica", 40))
plantSun.place(x=10, y=420)

plantLibraryAddConfirm = tk.Button(
    plantLibraryAddFrame,
    text="CONFIRM",
    bg="green",
    fg="white",
    font=("Helvetica", 20),
    width=10,
    command=addPlant
)
plantLibraryAddConfirm.place(x=10, y=500)

plantLibraryAddCancel = tk.Button(
    plantLibraryAddFrame,
    text="CANCEL",
    bg="red",
    fg="white",
    font=("Helvetica", 20),
    width=10,
    command=cancel
)
plantLibraryAddCancel.place(x=200, y=500)

plantLibraryAddFrame.place_forget()

#plant Detail

plantDetailFrame = tk.Frame(
    plantLibrary,
    bg="#E8E8E8",
    bd=3,
    relief="solid",
    width=1000,
    height=600
)
plantDetailFrame.place_forget()

plantDetailTitle = tk.Label(
    plantDetailFrame,
    text="Plant Name",
    font=("Helvetica", 50),
    bg="#E8E8E8"
)
plantDetailTitle.pack(pady=30)

plantDetailWater = tk.Label(
    plantDetailFrame,
    text="Water every: X days",
    font=("Helvetica", 35),
    bg="#E8E8E8"
)
plantDetailWater.pack(pady=15)

plantDetailSun = tk.Label(
    plantDetailFrame,
    text="Rotate every: X days",
    font=("Helvetica", 35),
    bg="#E8E8E8"
)
plantDetailSun.pack(pady=15)

plantDetailButtonFrame = tk.Frame(plantDetailFrame, bg="#E8E8E8")
plantDetailButtonFrame.pack(side="bottom", pady=40)

plantDetailBack = tk.Button(
    plantDetailButtonFrame,
    text="BACK",
    bg="#286a26",
    fg="white",
    font=("Helvetica", 30),
    width=10,
    command=lambda: (
        plantDetailFrame.place_forget(),
        plantLibraryAddButton.place(x=40, y=680)
    )
)
plantDetailBack.grid(row=0, column=0, padx=20)

plantDetailEdit = tk.Button(
    plantDetailButtonFrame,
    text="EDIT",
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 30),
    width=10,
    command=editPlant
)
plantDetailEdit.grid(row=0, column=1, padx=20)

plantDetailDelete = tk.Button(
    plantDetailButtonFrame,
    text="DELETE",
    bg="red",
    fg="white",
    font=("Helvetica", 30),
    width=10,
    command=deletePlant
)
plantDetailDelete.grid(row=0, column=2, padx=20)

#To-Do List

todoContainer = tk.Frame(todo, bg="white", bd=2, relief="solid")
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

def onMousewheelScroll(event):
    todoCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

todoCanvas.bind_all("<MouseWheel>", onMousewheelScroll)

def generateTodoTasks():
    for widget in todoFrame.winfo_children():
        widget.destroy()

    now = datetime.now()
    tasks = []

    for plant in plants.values():
        tasks.append((plant.next_water_date(), plant, "water"))
        tasks.append((plant.next_rotate_date(), plant, "rotate"))

    tasks.sort(key=lambda x: x[0])

    for dueDate, plant, taskType in tasks:
        hoursLeft = int((dueDate - now).total_seconds() // 3600)

        if taskType == "water":
            text = f"Water {plant.name}"
        else:
            text = f"Rotate {plant.name}"

        if hoursLeft < 0:
            labelText = f"{text} — OVERDUE"
            fg = "red"
        else:
            labelText = f"{text} — due in {hoursLeft} hours"
            fg = "black"

        row = tk.Frame(todoFrame, bg="#F5FFF5")
        row.pack(fill="x", padx=20, pady=8)

        taskLabel = tk.Label(
            row,
            text=labelText,
            font=("Helvetica", 28),
            bg="#F5FFF5",
            fg=fg,
            anchor="w"
        )
        taskLabel.pack(side="left", fill="x", expand=True)

        checkButton = tk.Button(
            row,
            text="○",
            font=("Helvetica", 30),
            bg="#F5FFF5",
            relief="flat"
        )

        checkButton.config(
            command=lambda r=row, b=checkButton, p=plant, t=taskType:
            completeTask(r, b, p, t)
        )
        checkButton.pack(side="right")

def completeTask(row, button, plant, taskType):
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

    if taskType == "water":
        plant.last_watered = now
    elif taskType == "rotate":
        plant.last_rotated = now

    dbUpdatePlant(plant.name, plant)
    
    root.after(600, generateTodoTasks)

# Reminders 

def checkReminders():
    now = datetime.now()

    for reminder in reminderList:
        if (
            reminder["enabled"]
            and not reminder["triggered"]
            and now >= reminder["time"]
        ):
            reminder["triggered"] = True
            messagebox.showinfo("Plant Reminder", reminder["message"])

    root.after(30000, checkReminders)

def addReminder(remindTime, message):
    reminderList.append({
        "time": remindTime,
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

messageLabel = tk.Label(
    reminders,
    text="Message",
    font=("Helvetica", 30)
)
messageLabel.place(x=40, y=200)

messageEntry = tk.Entry(
    reminders,
    font=("Helvetica", 30),
    width=25
)
messageEntry.place(x=300, y=200)

def submitReminder():
    try:
        timeStr = timeEntry.get()
        hour, minute = map(int, timeStr.split(":"))

        remindTime = datetime.now().replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        if remindTime < datetime.now():
            remindTime += timedelta(days=1)

        message = messageEntry.get()
        addReminder(remindTime, message)

        messagebox.showinfo("Reminder Set", "Reminder successfully added!")

        timeEntry.delete(0, tk.END)
        messageEntry.delete(0, tk.END)

    except:
        messagebox.showerror("Error", "Invalid time format (HH:MM)")

addReminderButton = tk.Button(
    reminders,
    text="Add Reminder",
    font=("Helvetica", 30),
    bg="green",
    fg="white",
    command=submitReminder
)
addReminderButton.place(x=40, y=300)

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

    for reminder in reminderList:
        row = tk.Frame(reminderFrame, bg="#F5FFF5")
        row.pack(fill="x", padx=20, pady=10)

        timeLabel = tk.Label(
            row,
            text=reminder["time"].strftime("%I:%M %p"),
            font=("Helvetica", 26),
            width=10,
            anchor="w",
            bg="#F5FFF5"
        )
        timeLabel.pack(side="left")

        messageLabel = tk.Label(
            row,
            text=reminder["message"],
            font=("Helvetica", 26),
            bg="#F5FFF5",
            anchor="w"
        )
        messageLabel.pack(side="left", fill="x", expand=True)

        toggleButton = tk.Button(
            row,
            text="ON" if reminder["enabled"] else "OFF",
            font=("Helvetica", 22),
            width=6,
            bg="#8BC34A" if reminder["enabled"] else "grey",
            command=lambda r=reminder: toggleReminder(r)
        )
        toggleButton.pack(side="right")

def toggleReminder(reminder):
    reminder["enabled"] = not reminder["enabled"]
    refreshReminderList()

checkReminders()
loadPlantsFromDB()
refreshPlantButtons()
generateTodoTasks()
print("program started")
root.mainloop()
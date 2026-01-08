import tkinter as tk

# 1. Create the main window
root = tk.Tk()
root.title("Plant Tracker") 
root.geometry("1920x1080") 

home = tk.Frame(root)
home.place(relx=0, rely=0, relwidth=1, relheight=1)

header = tk.Frame(root)
header.place(relx=0, rely=0, relwidth=1, relheight=1)

plantLibrary = tk.Frame(root, bg="black")   
plantLibrary.place(relx=0, y=200, relwidth=1, relheight=1)

toDo = tk.Frame(root, bg="red")   
toDo.place(relx=0, y=200, relwidth=1, relheight=1)

reminders = tk.Frame(root, bg="blue")   
reminders.place(relx=0, y=200, relwidth=1, relheight=1)

home.tkraise()

currentScreen = "H"

titleLabel = tk.Label(home, text="PLANT TRACKER", height=1, bg="#36ad53", fg="white", font=("Helvetica", 100))
titleLabel.pack(fill="both") 

def on_screen_switch(button_id):
    if currentScreen == "PL" and button_id == "A":
        swap_header("H")
    elif currentScreen == "PL" and button_id == "B":
        swap_header("TD")
    elif currentScreen == "PL" and button_id == "C":
        swap_header("R")
    elif currentScreen == "TD" and button_id == "A":
        swap_header("PL")
    elif currentScreen == "TD" and button_id == "B":
        swap_header("H")
    elif currentScreen == "TD" and button_id == "C":
        swap_header("R")
    elif currentScreen == "R" and button_id == "A":
        swap_header("PL")
    elif currentScreen == "R" and button_id == "B":
        swap_header("TD")
    elif currentScreen == "R" and button_id == "C":
        swap_header("H")
    elif currentScreen == "H" and button_id == "A":
        swap_header("PL")
    elif currentScreen == "H" and button_id == "B":
        swap_header("TD")
    elif currentScreen == "H" and button_id == "C":
        swap_header("R")
    else:
        print(currentScreen)
        print(f"Unknown button ID: {button_id}")

PLButtonFrame = tk.Frame(home, height=200, width=800, bg="black")
PLButtonFrame.place(x=40, y=200)
PLButton = tk.Button(PLButtonFrame, text="Plant Library", bg="#286a26", fg="white", font=("Helvetica", 80), height=1, width=13, command=lambda: on_screen_switch(button_id="A"))
PLButton.place(x=0, y=0)

TDButtonFrame = tk.Frame(home, height=200, width=800, bg="black") 
TDButtonFrame.place(x=40, y=450)
TDButton = tk.Button(TDButtonFrame, text="To-Do List", bg="#286a26", fg="white", font=("Helvetica", 80), height=1, width=13, command=lambda: on_screen_switch(button_id="B"))
TDButton.place(x=0, y=0)

RButtonFrame = tk.Frame(home, height=200, width=800, bg="black") 
RButtonFrame.place(x=40, y=700)
RButton = tk.Button(RButtonFrame, text="Reminders", bg="#286a26", fg="white", font=("Helvetica", 80), height=1, width=13, command=lambda: on_screen_switch(button_id="C"))
RButton.place(x=0, y=0)

HLabel = tk.Label(header, text="placeholder", height=1, bg="#36ad53", fg="white", font=("Helvetica", 63))
HLabel.pack(fill="both") 

AHeaderFrame = tk.Frame(header, height=100, width=640, bg="white")
AHeaderFrame.place(x=0, y=100)
AHeader = tk.Button(AHeaderFrame, text="a", bg="#286a26", fg="white", font=("Helvetica", 40), height=1, width=21, command=lambda: on_screen_switch(button_id="A"))
AHeader.place(x=0, y=0)

BHeaderFrame = tk.Frame(header, height=100, width=640, bg="red")
BHeaderFrame.place(x=640, y=100)
BHeader = tk.Button(BHeaderFrame, text="b", bg="#286a26", fg="white", font=("Helvetica", 40), height=1, width=21, command=lambda: on_screen_switch(button_id="B"))
BHeader.place(x=0, y=0)

CHeaderFrame = tk.Frame(header, height=100, width=640, bg="blue")
CHeaderFrame.place(x=1280, y=100)
CHeader = tk.Button(CHeaderFrame, text="c", bg="#286a26", fg="white", font=("Helvetica", 40), height=1, width=21, command=lambda: on_screen_switch(button_id="C"))
CHeader.place(x=0, y=0)

def swap_header(page):
    if page == "PL":
        print("PL")
        currentScreen = "PL"
        print(currentScreen)
        HLabel.configure(text="Plant Library")
        AHeader.configure(text="Home")
        BHeader.configure(text="To-Do List")
        CHeader.configure(text="Reminders")
        plantLibrary.tkraise()
        header.tkraise()
    elif page == "TD":
        print("TD")
        currentScreen = "TD"
        HLabel.configure(text="To-Do List")
        AHeader.configure(text="Plant Library")
        BHeader.configure(text="Home")
        CHeader.configure(text="Reminders")
        toDo.tkraise()
        header.tkraise()
    elif page == "R":
        print("R")
        currentScreen = "R"
        HLabel.configure(text="Reminders")
        AHeader.configure(text="Plant Library")
        BHeader.configure(text="To-Do List")
        CHeader.configure(text="Home")
        reminders.tkraise()
        header.tkraise()
    elif page == "H":
        print("help")
        currentScreen = "H"
        home.tkraise()
    else:
        print("error")
    
home.tkraise()
root.mainloop()

# Dev Notes: Currently the screen swap when pushing home button swaps it to same page idk why instead of home page
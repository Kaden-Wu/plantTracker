import tkinter as tk
from tkinter import ttk
from plant import Plant

root = tk.Tk()
root.title("Plant Tracker") 
root.geometry("1920x1080") 

home = tk.Frame(root)
home.place(relx=0, rely=0, relwidth=1, relheight=1)

header = tk.Frame(root)
header.place(relx=0, rely=0, relwidth=1, relheight=1)

plantLibrary = tk.Frame(root)   
plantLibrary.place(relx=0, y=200, relwidth=1, relheight=1)

toDo = tk.Frame(root, bg="blue")   
toDo.place(relx=0, y=200, relwidth=1, relheight=1)

reminders = tk.Frame(root, bg="green")   
reminders.place(relx=0, y=200, relwidth=1, relheight=1)

home.tkraise()

currentScreen = "H"

titleLabel = tk.Label(home, text="PLANT TRACKER", height=1, bg="#36ad53", fg="white", font=("Helvetica", 100))
titleLabel.pack(fill="both") 

def on_screen_switch(button_id):
    print("screen swap")
    print(currentScreen)
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
    global currentScreen
    if page == 1:
        currentScreen = "PL"
        HLabel.configure(text="Plant Library")
        AHeader.configure(text="Home")
        BHeader.configure(text="To-Do List")
        CHeader.configure(text="Reminders")
        header.tkraise()
        plantLibrary.tkraise()
    elif page == 2:
        currentScreen = "TD"
        HLabel.configure(text="To-Do List")
        AHeader.configure(text="Plant Library")
        BHeader.configure(text="Home")
        CHeader.configure(text="Reminders")
        header.tkraise()
        toDo.tkraise()
    elif page == 3:
        currentScreen = "R"
        HLabel.configure(text="Reminders")
        AHeader.configure(text="Plant Library")
        BHeader.configure(text="To-Do List")
        CHeader.configure(text="Home")
        header.tkraise()
        reminders.tkraise()
    elif page == 0:
        currentScreen = "H"
        home.tkraise()
    else:
        print("error")
        
#Plant Library Screen

def PLAraise():
    print("PLA raise")
    PLAframe.place(x=600, y=60)
    
def addPlant():
    print("add plant")
    print(pn.get())
    print(pw.get())
    print(ps.get())
    plant1 = Plant(pn.get(), pw.get(), ps.get())
    print(plant1.display_info())
    PLAframe.place_forget()
    pn.delete(0, tk.END)
    pw.delete(0, tk.END)
    ps.delete(0, tk.END)

def cancel():
    print("cancel")
    PLAframe.place_forget()
    pn.delete(0, tk.END)
    pw.delete(0, tk.END)
    ps.delete(0, tk.END)
    
"""
LFrame = tk.Frame(plantLibrary, height=720, width=1200, bg="black")
LFrame.place(x=40, y=40)
LScrollbar = tk.Scrollbar(LFrame, orient=tk.VERTICAL, width=60)
LScrollbar.place(x=0, y=0, height=720)
LListFrame = tk.Frame(LFrame, height=720, width=1140)
LListFrame.place(x=60, y=0)
"""
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        # Create a Canvas widget and a vertical scrollbar
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        # Create an inner frame to hold the widgets
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Bind the Configure event of the inner frame to update the scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all") # Set the scroll region to the bounding box of all items in the frame
            )
        )

        # Add the inner frame to the canvas using create_window
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") # Anchor to the top-left (northwest)

        # Configure the canvas to use the scrollbar and pack everything
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
scroll_frame = ScrollableFrame(plantLibrary)
scroll_frame.place(x=40, y=40)

PLAbutton=tk.Button(plantLibrary, text="Add Plant", bg="green", fg="white", font=("Helvetica", 40), height=1, width=10, command=PLAraise)  
PLAbutton.place(x=1400, y=200)

PLAframe=tk.Frame(plantLibrary, width=730, height=600, bg="#E8E8E8")
PLAframe.place(x=600, y=60)
PLAname=tk.Label(PLAframe, text="Enter Plant Name: ", font=("Helvetica", 40))
PLAname.place(x=10, y=10)
pn =tk.Entry(PLAframe, bg="grey", font=("Helvetica", 40))
pn.place(x=10, y=80)
PLAwater=tk.Label(PLAframe, text="Enter Water Requirements: ", font=("Helvetica", 40))
PLAwater.place(x=10, y=180)
pw =tk.Entry(PLAframe, bg="grey", font=("Helvetica", 40))
pw.place(x=10, y=250)
PLAsun=tk.Label(PLAframe, text="Enter Sunlight Requirements: ", font=("Helvetica", 40))
PLAsun.place(x=10, y=350)
ps =tk.Entry(PLAframe, bg="grey", font=("Helvetica", 40))
ps.place(x=10, y=420)
PLAconfirm=tk.Button(PLAframe, text="CONFIRM", bg="green", fg="white", font=("Helvetica", 20), height=1, width=10, command=addPlant)
PLAconfirm.place(x=10, y=500)
PLAcancel=tk.Button(PLAframe, text="CANCEL", bg="red", fg="white", font=("Helvetica", 20), height=1, width=10, command=cancel)
PLAcancel.place(x=200, y=500)
PLAframe.place_forget()


on_screen_switch("A")
print("program started")
root.mainloop()
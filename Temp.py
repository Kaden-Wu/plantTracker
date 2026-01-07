import tkinter as tk

# 1. Create the main window
root = tk.Tk()
root.title("Plant Tracker") 
root.geometry("1920x1080") 

home = tk.Frame(root)
home.place(relx=0, rely=0, relwidth=1, relheight=1)

plantLibrary = tk.Frame(root, bg="black")   
plantLibrary.place(relx=0, rely=0, relwidth=1, relheight=1)

toDo = tk.Frame(root, bg="red")   
toDo.place(relx=0, rely=0, relwidth=1, relheight=1)

reminders = tk.Frame(root, bg="blue")   
reminders.place(relx=0, rely=0, relwidth=1, relheight=1)

home.tkraise()

screenNum = 1

titleLabel = tk.Label(home, text="PLANT TRACKER", height=1, bg="#36ad53", fg="white", font=("Helvetica", 100))
titleLabel.pack(fill="both") 

def on_screen_switch():
    if screenNum == 0:
        show_frame(home)
    elif screenNum == 1:
        show_frame(plantLibrary)
    elif screenNum == 2:
        show_frame(toDo)
    elif screenNum == 3:
        show_frame(reminders)

PLButtonFrame = tk.Frame(home, height=200, width=800, bg="black")
PLButtonFrame.place(x=40, y=200)
PLButton = tk.Button(PLButtonFrame, text="Plant Library", bg="#286a26", fg="white", font=("Helvetica", 80), height=1, width=13, command=on_screen_switch)
PLButton.place(x=0, y=0)

TDButtonFrame = tk.Frame(home, height=200, width=800, bg="black") 
TDButtonFrame.place(x=40, y=450)
TDButton = tk.Button(TDButtonFrame, text="To-Do List", bg="#286a26", fg="white", font=("Helvetica", 80), height=1, width=13, command=on_screen_switch)
TDButton.place(x=0, y=0)

RButtonFrame = tk.Frame(home, height=200, width=800, bg="black") 
RButtonFrame.place(x=40, y=700)
RButton = tk.Button(RButtonFrame, text="Reminders", bg="#286a26", fg="white", font=("Helvetica", 80), height=1, width=13, command=on_screen_switch)
RButton.place(x=0, y=0)

def show_frame(page):
    page.tkraise()

root.mainloop()

# fortnite
from tkinter import *
import customtkinter
from tkinter.ttk import *
from games_window import set_games_window
from PIL import Image, ImageTk
import tkinter as tk
# Create a GUI app
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.title("I LIKE TO MOVE IT")
app.geometry('800x780')
# Bind the app with Escape keyboard to
# quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())

# Declare the width and height in variables
WIDTH, HEIGHT = 800, 780

image= ImageTk.PhotoImage(Image.open("main-imag-1.jpg"))
background_label= Label(app, image=image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


def open_gams_window():
    # new_frame = customtkinter.CTkFrame(master=app, height=HEIGHT, width=WIDTH)
    games_frame = set_games_window(app)
    games_frame.pack()


go_inside = customtkinter.CTkButton(
    master=app,
    command=open_gams_window,
    text="Let's play",
    text_color="#FFFFFF",
    font=('calibri', 22),
    hover=True,
    hover_color="#A8E6FE",
    height=50,
    width=300,
    border_width=4,
    corner_radius=2,
    border_color="#68aec9",
    bg_color="#68aec9",
    fg_color="#68aec9").place(anchor='center', relx=0.5, rely=0.8)


if __name__ == "__main__":
    # Create an infinite loop for displaying app on screen
    app.mainloop()
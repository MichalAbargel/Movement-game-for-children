import random
import time
from tkinter import *
import customtkinter
from tkinter.ttk import *
import cv2
import cvzone
from PIL import Image, ImageTk
import points_game
from music_player import play_well_done, play_try_again, is_busy
from hand_recognition_model import deditiction_hands
from numbers_game import numbers


# define global frame counter
hands_counter_frames = 0
numbers_counter_frames = 0
max_counter = 200
camera_frame = None
camera = None
user_order = None
app = None

# Define a video capture object
vid = cv2.VideoCapture(0)

# Set the width and height
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 590)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 350)


def configur_image_camera(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    image = Image.fromarray(image)
    imageTK = ImageTk.PhotoImage(image=image)
    # Displaying photoimage in the label
    camera.photo_image = imageTK
    # Configure image in the label
    camera.configure(image=imageTK)


def show_stream_numbers(counter, finger, time_start, score):
    global user_order
    user_order.configure(text=str(finger))
    # Wait for 3 seconds
    # time.sleep(3)
    # frame = int(vid.get(cv2.CAP_PROP_FPS))
    total_time = 20
    _, frame = vid.read()
    img = cv2.flip(frame, 1)
    image, win = numbers(finger, frame)
    if win:
        counter += 1
    # if flag-> make sound
    if counter == 5:
        # Need 5 frames to call it win/loss
        if win:
            play_well_done()
            user_order.configure(text='well done!!')
            counter = 0
            finger = random.randrange(1, 6)
            score = score + 1
        else:
            play_try_again()
            user_order.configure(text='Try again...')
            counter = 0
    configur_image_camera(image)
    if time.time() - time_start >= total_time:
        game_over = True
        cvzone.putTextRect(img, 'GAME OVER !!!', (50, 140), scale=5, offset=8, thickness=7)
        cvzone.putTextRect(image, f'Your Score: {score}', (70, 200), scale=3, offset=2, thickness=5)
        user_order.configure(text=f'GAME OVER !!!\n  Your Score: {score}')

        return
    camera.after(2, lambda: show_stream_numbers(counter, finger, time_start, score))


def show_stream_hands(is_playing, counter_win, counter_lose, random_order, time_start, game_over,score):
    global hands_counter_frames
    global max_counter
    orders = ['Raise your right hand', 'Raise your left hand', 'Raise your hands together']
    order = random_order
    user_order.configure(text=orders[order])
    _, frame = vid.read()
    image, win, game_over_ = deditiction_hands(frame, order, time_start, game_over)
    if game_over_:
        user_order.configure(text=f'GAME OVER !!!\nYour Score: {score}')
        return
    print(win)
    if win == 'win':
        counter_win += 1
    elif win == 'lose':
        counter_lose += 1
    if not is_playing:
        if win == 'win' and counter_win == 2:
            score = score+1
            user_order.configure(text='well done!!')
            print("enter to win section")
            play_well_done()
            is_playing = True
            counter_win = 0
            counter_lose = 0
            order = random.randrange(0, 3)
        elif win == 'lose' and counter_lose == 2:
            user_order.configure(text='oops...')
            print("enter to lose section")
            play_try_again()
            is_playing = True
            counter_win = 0
            counter_lose = 0
            order = random.randrange(0, 3)
    if is_playing:
        while is_busy():
            continue
        is_playing = False
    configur_image_camera(image)
    hands_counter_frames = hands_counter_frames+ 2
    camera.after(2, lambda: show_stream_hands(is_playing, counter_win, counter_lose, order,time_start, game_over_,score))


def show_stream_points(is_playing, counter, score, cx, cy,time_start,game_over):
    _, frame = vid.read()
    image, game_over, score_, counter_ = points_game.analyze_points_frame(frame, counter,score,cx, cy,time_start,game_over)
    if not is_playing:
        if game_over:
            if score_ != 0:
                play_well_done()
                user_order.configure(text='well done!!')
                is_playing = True
            else:
                play_try_again()
                user_order.configure(text='Try again...')
                is_playing = True
    if is_playing:
        while is_busy():
            continue
        is_playing = False
    if game_over:
        # game over so after need to call function that return home page
        return
    configur_image_camera(image)
    if score_ > score:
        # 590 350
        cx = random.randint(10, 590)
        cy = random.randint(10, 350)
    camera.after(2, lambda: show_stream_points(is_playing, counter_,score_, cx, cy,time_start,game_over))


def set_camera():
    # set camera
    camera_frame.pack()
    camera_frame.place(anchor='n', relx=0.5, rely=0.05)
    camera.pack()


def hands_control():
    set_camera()
    order = random.randrange(0, 3)
    time_start = time.time()
    game_over = False
    score = 0
    show_stream_hands(False, 0, 0, order,time_start, game_over, score)


def numbers_control():
    set_camera()
    finger = random.randrange(1, 6)
    counter = 0
    score = 0
    time_start = time.time()
    show_stream_numbers(counter, finger, time_start,score)


def points_control():
    set_camera()
    counter = 0
    score = 0
    cx, cy = 250, 250
    time_start = time.time()
    total_time = 20
    game_over = False
    show_stream_points(False, counter, score, cx, cy, time_start,game_over)


def close_app():
    app.destroy()


def change_appearance_mode_event(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)


def set_games_window(master):
    global camera_frame
    global camera
    global user_order
    global app

    app = master
    background_frame = customtkinter.CTkFrame(app, width=800, height=780)
    background_frame.pack()
    background_frame.place(anchor='center', relx=0.5, rely=0.05)
    # be n, ne, e, se, s, sw, w, nw, or center

    # Create an object of tkinter ImageTk
    image_frame = customtkinter.CTkFrame(background_frame, width=700, height=350)
    image_frame.place()
    image_frame.pack()
    img = ImageTk.PhotoImage(Image.open("main-image-2.jpg"))
    # Create a Label Widget to display the text or Image
    background_label = Label(image_frame, image=img)
    background_label.place(anchor='center', relx=0.5, rely=0.2)
    background_label.pack()

    # define a camera_frame and camera and display it on app
    camera_frame = customtkinter.CTkFrame(app, width=700, height=300)
    camera = customtkinter.CTkLabel(camera_frame, text="")

    menu_frame = customtkinter.CTkFrame(app, width=700, height=300, fg_color='white')
    menu_frame.pack(anchor='center')
    menu_frame.place(x=50, y=450)

    # user_output
    user_order = customtkinter.CTkLabel(master=menu_frame, font=("calibri", 30), text="Hello! let's play",
                                        text_color=('#008B8B', 'white'), width=200)
    user_order.place(anchor='center', relx=0.5, rely=0.2)

    # buttons:
    hands_button = customtkinter.CTkButton(
        master=menu_frame,
        command=hands_control,
        text="Hands",
        text_color="#68aec9",
        hover=True,
        hover_color="#A8E6FE",
        height=50,
        width=140,
        border_width=4,
        corner_radius=20,
        border_color="#68aec9",
        bg_color="#FFFFFF",
        fg_color="#FFFFFF").place(x=80, y=130)

    numbers_button = customtkinter.CTkButton(
        master=menu_frame,
        command=numbers_control,
        text="Numbers",
        text_color="#68aec9",
        hover=True,
        hover_color="#A8E6FE",
        height=50,
        width=140,
        border_width=4,
        corner_radius=20,
        border_color="#68aec9",
        bg_color="#FFFFFF",
        fg_color="#FFFFFF").place(x=280, y=130)

    points_button = customtkinter.CTkButton(
        master=menu_frame,
        command=points_control,
        text="Points",
        text_color="#68aec9",
        hover=True,
        hover_color="#A8E6FE",
        height=50,
        width=140,
        border_width=4,
        corner_radius=20,
        border_color="#68aec9",
        bg_color="#FFFFFF",
        fg_color="#FFFFFF").place(x=480, y=130)

    close_button = customtkinter.CTkButton(
        master=menu_frame,
        command=close_app,
        text="Good By",
        text_color="#FFFFFF",
        hover=True,
        hover_color="#A8E6FE",
        height=50,
        width=200,
        border_width=4,
        corner_radius=2,
        border_color="#68aec9",
        bg_color="#68aec9",
        fg_color="#68aec9").place(anchor='center', relx=0.5, rely=0.85)
    return background_frame


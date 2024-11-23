import math
from winsound import PlaySound, SND_FILENAME
from tkinter import *
from threading import Thread
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
TIMER_IS_ON = False
REPS = 0
TIMER = None

# ---------------------------- TIMER RESET ------------------------------- #

def play_sound():
    PlaySound('Files/sound.wav', SND_FILENAME)

# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
    global TIMER, REPS, TIMER_IS_ON
    if TIMER is not None:
        window.after_cancel(TIMER)
        TIMER = None
    canvas.itemconfig(timer_text, text="00:00")
    label_1.config(text='TIMER', fg=GREEN)
    complete_marks.config(text="")
    REPS = 0
    TIMER_IS_ON = False

# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global REPS
    global TIMER_IS_ON

    if not TIMER_IS_ON:
        REPS += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if REPS % 2 != 0:
        time = work_sec
        label_1.config(text='WORK', fg=GREEN)
    elif REPS % 2 == 0 and REPS % 8 != 0:
        time = short_break_sec
        label_1.config(text='BREAK', fg=PINK)
    else:
        time = long_break_sec
        label_1.config(text='BREAK', fg=RED)

    if not TIMER_IS_ON:
        count_down(time)
        TIMER_IS_ON = True

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    minutes = int(count/60)
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}")
    if count >= 0:
        global TIMER
        TIMER = window.after(1000, count_down, count-1)
    else:
        sound = Thread(target=play_sound)
        sound.daemon = True
        sound.start()

        global TIMER_IS_ON
        TIMER_IS_ON = False
        start_timer()

        global REPS
        tick = ""
        for _ in range(math.floor(REPS/ 2)):
            tick += "✔"

        complete_marks.config(text=tick)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro Timer")
window.config(padx=50, pady=50, bg=YELLOW)
window.resizable(width=False, height=False)
image = PhotoImage(file='Files/tomato.png')
window.iconphoto(False,image)

# Adding the Timer label
label_1 = Label(text='TIMER')
label_1.config(fg=GREEN, font=(FONT_NAME, 35, 'bold'), bg=YELLOW)
label_1.grid(row=0, column=1)
# Creating The Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_image(100, 112, image=image)
timer_text = canvas.create_text(100,130, text="00:00", fill='white', font=(FONT_NAME, 35,'bold'))
canvas.grid(row=1, column=1)
# Adding Buttons
start_button = Button(bg='white', font=(FONT_NAME,),
                      highlightthickness=2, activebackground=GREEN, activeforeground='white',
                      border=0, text='Start', command=start_timer
                      )
start_button.grid(row=2, column=0)

reset_button = Button(text='Reset', bg='white', font=(FONT_NAME,), command=reset_timer,
                      activebackground=GREEN, activeforeground='white', border=0)
reset_button.grid(row=2, column=2)

# Tick Marks
complete_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME,15))
complete_marks.grid(row=3, column=1)



window.mainloop()

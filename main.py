import tkinter as tk
from pydub import AudioSegment
from pydub.playback import play


SONG = AudioSegment.from_mp3("star_tours-loud.mp3")
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
TIMER = None


def timer_reset():
    global REPS
    window.after_cancel(TIMER)
    REPS = 0
    checkmark_label.config(text="")
    title_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")


def start_timer():
    global REPS
    REPS += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if REPS % 8 == 0:
        title_label.config(text="Relax", fg=RED)
        count_down(long_break_sec)
    elif REPS % 2 == 0:
        title_label.config(text="Relax", fg=PINK)
        count_down(short_break_sec)
    else:
        title_label.config(text="Work!", fg=GREEN)
        count_down(work_sec)


def count_down(count):
    global REPS
    global TIMER
    minutes = count // 60
    if minutes < 10:
        minutes = f"0{minutes}"
    seconds = count % 60
    if seconds == 0:
        seconds = "00"
    elif seconds < 10:
        seconds = f"0{seconds}"
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        TIMER = window.after(1000, count_down, count - 1)
    else:
        if REPS < 8:
            play(SONG)
            start_timer()
            if REPS % 2 == 0:
                checkmarks = (REPS // 2) * "✔"
                checkmark_label.config(text=checkmarks)
        else:
            play(SONG)
            REPS = 0


window = tk.Tk()
window.title("Pomodoro")
window.resizable(False, False)
window.config(padx=100, pady=50, bg=YELLOW)

#  Labels

title_label = tk.Label(text="Timer", font=(FONT_NAME, 28, "bold"), bg=YELLOW, fg=GREEN)
title_label.grid(column=0, row=0, columnspan=3)

checkmark_label = tk.Label(font=(FONT_NAME, 18, "bold"), bg=YELLOW, fg=GREEN)
checkmark_label.grid(column=0, row=3, columnspan=3, padx=20, pady=20)

#  Canvas
canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_pic = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_pic)
timer_text = canvas.create_text(106, 140, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=0, row=1, columnspan=3)

#  Buttons

start_button = tk.Button(text="Start", command=start_timer, highlightthickness=0,
                         bg=GREEN, fg=RED, activebackground=PINK,  activeforeground=RED,
                         font=("Arial", 14, "bold"), bd=1)
start_button.grid(column=0, row=4, sticky="e")

reset_button = tk.Button(text="Reset", command=timer_reset, highlightthickness=0,
                         bg=GREEN, fg=RED, activebackground=PINK,  activeforeground=RED,
                         font=("Arial", 14, "bold"), bd=1)
reset_button.grid(column=2, row=4, sticky="w")


window.mainloop()

from tkinter import Tk, Checkbutton, IntVar, Label, Frame
from time import time


class Alarm:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("200x100")
        self.alarm = Label(self.root, text="Alarm: ---")
        self.alarm.pack(side="bottom")

    def command(self, state):
        self.alarm.config(text="PÍÍÍP" if state else "---")


inst_alarm = Alarm()


class Sim:
    def __init__(self, side, name, t_waggle=10, t_autolock=7200, t_alarm=18000):
        self.name = name
        self.t_waggle = t_waggle
        self.t_autolock = t_autolock
        self.t_alarm = t_alarm
        self.frame = Frame(inst_alarm.root)
        self.frame.pack(side=side)
        Label(self.frame, text=name).pack()
        self.var_key_inserted = IntVar(value=1)
        self.w_key_inserted = Checkbutton(self.frame,
                                          text="klíček",
                                          command=self.key_present,
                                          variable=self.var_key_inserted)
        self.w_key_inserted.pack()
        self.w_key_locked = Label(self.frame, text="LOCKED")
        self.w_key_locked.pack()
        self.key_taken = None
        self.key_present()
        self.key_unlocked = False
        self.key_ready_to_return = False

    def key_present(self):
        if not bool(self.var_key_inserted.get()):
            self.key_taken = time()
        else:
            self.key_taken = False

    def key_lock(self):
        self.w_key_locked.config(text="LOCKED!")
        self.key_unlocked = False

    def key_unlock(self):
        self.w_key_locked.config(text="UNLOCKED!")
        self.key_unlocked = time()

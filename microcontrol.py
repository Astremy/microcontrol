import tkinter as tk

list_in = {}
list_out = {}
list_process = []
config = ["white", "black", True]

def io(name):

    def register(function):

        default_value = function()

        def call():
            if name in list_in:
                return int(list_in[name].get() | default_value)

        def set(value):
            if name in list_out:
                list_out[name].config(fg = config[value | default_value])

        call.set = set
        return call

    return register

def macro(function):

    def func_call(*args):

        if len(args) != args_needed:
            raise NotEnoughError(len(args), args_needed)

        return function(*args)

    args_needed = function.__code__.co_argcount

    return func_call

def process(function):
    list_process.append(function)

def start():
    init_fen()

class NotEnoughError(Exception):

    def __init__(self, argscount, neededcount):
        self.argscount = argscount
        self.needed = neededcount
        super().__init__(self)

    def __str__(self):
        return f"No Enough Arguments : Need {self.needed}, but get {self.argscount}"

def update():
    if config[2]:
        for out in list_out.values():
            out.config(fg = config[0])
    for func in list_process:
        func()

def init_fen():

    fen = tk.Tk()

    inputs = ["D2", "E4", "E3", "H7", "J7", "G5", "G4", "H6", "H5", "J6"]
    outputs = ["B1", "B2", "C2", "C1", "E1", "F2", "H1", "J3", "J2", "J1"]
    digits = [
    ["D15","A16","B16","E15","A17","B17","F14","A18"],
    ["A13","B13","C13","A14","B14","E14","A15","B15"],
    ["E11","F11","H12","H13","G12","F12","F13","D13"]]

    output_frame = tk.Frame(fen)
    output_frame.pack()
    button_frame = tk.Frame(fen)
    button_frame.pack(pady=10)
    digit_frame = tk.Frame(fen)
    digit_frame.pack()

    for o in outputs:
        io = tk.Label(output_frame, text="◉", font=("Courier", 30))
        list_out[o] = io
        io.pack(side = tk.LEFT, padx=5)

    for i in inputs:
        var = tk.IntVar()
        io = tk.Checkbutton(button_frame, variable=var, command = update)
        list_in[i] = var
        io.pack(side = tk.LEFT)

    c = 0

    for d in digits:

        d0 = tk.Label(digit_frame, text = "___")
        d0.grid(column=c+1, row=0)
        list_out[d[0]] = d0

        d1 = tk.Label(digit_frame, text = "|")
        d1.grid(column=c+0, row=1)
        list_out[d[1]] = d1

        d2 = tk.Label(digit_frame, text = "|")
        d2.grid(column=c+2, row=1)
        list_out[d[2]] = d2

        d3 = tk.Label(digit_frame, text = "___")
        d3.grid(column=c+1, row=2)
        list_out[d[3]] = d3
        
        d4 = tk.Label(digit_frame, text = "|")
        d4.grid(column=c+0, row=3)
        list_out[d[4]] = d4
        
        d5 = tk.Label(digit_frame, text = "|")
        d5.grid(column=c+2, row=3)
        list_out[d[5]] = d5
        
        d6 = tk.Label(digit_frame, text = "___")
        d6.grid(column=c+1, row=4)
        list_out[d[6]] = d6
        
        d7 = tk.Label(digit_frame, text = "o")
        d7.grid(column=c+3, row=4)
        list_out[d[7]] = d7

        c += 5

    update()

    tk.mainloop()
from tkinter import *
from tkinter import filedialog
from psap_parameters import *
from psap_core import psap

class UserInput(Tk):

    def __init__(self):
        Tk.__init__(self)

        "Setting up the window."
        self.title("PSAP Startup")
        self.geometry("300x250")

        "Setting up the components."
        self.name_prompt = Label(self, text="Please enter participant's name below: ")
        self.entry = Entry(self)
        self.image_prompt = Label(self, text="Please press the button below to choose opponent's image: ")
        self.image_button = Button(self, text="Choose", command=self.get_image_name)
        self.submit = Button(self, text="Submit", command=self.submit_name)

        "Printing components."
        self.name_prompt.pack()
        self.entry.pack()
        self.image_prompt.pack()
        self.image_button.pack()
        self.submit.pack()

    def submit_name(self):
        global participant_name
        participant_name = self.entry.get()
        self.destroy()

    def get_image_name(self):
        global opponent_image_name
        opponent_image_name = str(filedialog.askopenfilename())

session = UserInput()
session.mainloop()

if participant_name == "":
    participant_name = 'You'
psap(participant_name, opponent_image_name)

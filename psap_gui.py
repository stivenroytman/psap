from tkinter import *
from tkinter import filedialog
from psap_parameters import *
from psap_core import psap

opponent_image_name_list = ['work']

class UserInput(Tk):

    def __init__(self):
        Tk.__init__(self)

        "Setting up the window."
        self.title("PSAP Startup")
        self.geometry("300x250")
        self.count = 0
        self.opponent_list = ['', '', '']

        "Setting up the components."
        self.name_prompt = Label(self, text="Please enter participant's name below: ")
        self.entry = Entry(self)
        self.opponent1_button = Button(self, text="Opponent1", command=self.get_image_name)
        self.opponent1_feedback = Label(self, textvariable=self.opponent_list[0], relief=RAISED)
        self.opponent2_button = Button(self, text="Opponent2", command=self.get_image_name)
        self.opponent2_feedback = Label(self, textvariable=self.opponent_list[1], relief=RAISED)
        self.opponent3_button = Button(self, text="Opponent3", command=self.get_image_name)
        self.opponent3_feedback = Label(self, textvariable=self.opponent_list[2], relief=RAISED)
        self.submit = Button(self, text="Submit", command=self.submit_name)

        "Printing components."
        self.name_prompt.pack()
        self.entry.pack()
        self.opponent1_button.pack()
        self.opponent1_feedback.pack()
        self.opponent2_button.pack()
        self.opponent2_feedback.pack()
        self.opponent3_button.pack()
        self.opponent3_feedback.pack()
        self.submit.pack()

    def submit_name(self):
        global participant_name
        participant_name = self.entry.get()
        self.destroy()

    def get_image_name(self):
        # TODO: this is a really shitty way of implementing this
        # Particularly worried about the incrementor. May lead to strange behavior if picking out of order...
        self.opponent_list[self.count] = filedialog.askopenfilename()
        global opponent_image_name_list
        opponent_image_name_list.append(self.opponent_list[self.count])
        self.count += 1

session = UserInput()
session.mainloop()

if participant_name == "":
    participant_name = 'You'
psap(participant_name, opponent_image_name_list)


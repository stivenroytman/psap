# Point Subtraction Aggression Paradigm (PSAP) Program

## Dependencies

1. python3
2. pygame
3. numpy
4. pandas 
5. Windows PowerShell (if you want to use the .exe files)

## Instructions

If you are running Windows:
1. Download and install [Python3](https://www.python.org/downloads/). 
2. Run the 'SETUP.exe' file if this is your first time running PSAP.
3. Run 'PSAP.exe'.
4. Choose the folder with opponent images.
    * Make sure there are at least 3 images in that folder before you run the program. 
    * The order in which the images are presented can be altered by changing their name ('1.png' comes first, then '2.png', etc).
5. Enter the participant's name. 
6. ...
7. Profit!

If you are running Linux or macOS:

***Instructions coming soon...***
But you can probably figure it out on your own ;)

## Description

The software present in this repository can be used to conduct PSAP experiments as detailed in the following article:
[PSAP Review](https://www.sciencedirect.com/science/article/abs/pii/S0018506X1530218X)

In essence, this experimental paradigm is used to assess levels of reactive aggression. The participant is presented with 3 potential moves:
1. Press 1 on the numpad. After 100 presses, they earn a point.
2. Press 2 on the numpad. After 10 presses, they cause their opponent to lose a point.
3. Press 3 on the numpad. After 10 presses, they acquire protection from their opponent for a variable time interval.

The participant is told that the goal is to acquire more points than their opponent. Though they are lead to believe that their opponent is another human being participating in this experiment remotely, our version of PSAP utilizes a simple AI that either earns, steals, or protects itself semi-randomly. The frequency of each choice is set by the experimentor before conducting a trial. 

After a trial with a specified number of rounds is completed, data such as number of times an option was chosen by a participant or the number of times that they were provoked by the AI is written to the working directory as a set of pickle files. Those pickle files are then compiled into a dataframe with a separate python script by the investigator (future plans are to automate this process).

Currently, there is still a lot of features to add and bugs to fix, but this is a working version of PSAP with a rudimentary user interface!

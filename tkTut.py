''' 
Tk is a cross platform GUI development tool running covering 
Linux, MacOS and Windows 
'''
from tkinter import *       #standar binding to tk
from tkinter import ttk
from typing import Collection     #Newer themed widgets 


# combining everything within an app
class App:
    def __init__(self):
        self.window=Tk()     # intitizlize a tk window
        self.window.title("Length Converter")   # Set title

        # Creating a frame widget inside window which holds the UI content
        # frame gives a more modern look to the window
        self.winFrame=ttk.Frame(self.window, padding="2 2 10 10")
        # Frid places a frame directly inside main app window at the start
        # sticky=(NSEW) means it will expand with expand in window size 
        self.winFrame.grid(column=0, row=0, sticky=(N,S,E,W))
        #These tell Tk that frame should expand alongwith window
        self.window.columnconfigure(0,weight=1)
        self.window.rowconfigure(0,weight=1)

        # Create add var and position text field
        # Text field widget, its called Entry widget
        # These variables should be global
        self.inputCentimeter=StringVar()
        # Create an entry widget and assign it the inputvariable
        # position it inside frame at (1,2)
        ttk.Entry(self.winFrame,width=7,textvariable=self.inputCentimeter).grid(column=2, row=1, sticky=(W,E))
        
        ## Creating other widgets
        self.outputMeters=StringVar()
        # text widget
        ttk.Label(self.winFrame, textvariable=self.outputMeters).grid(column=2,row=2,sticky=(W,E))
        # command is the function to apply
        ttk.Button(self.winFrame, text="Calculate",command=self.calculate ).grid(column=3,row=3,sticky=W)
        ttk.Label(self.winFrame, text="cm").grid(column=3, row=1, sticky=W)       
        ttk.Label(self.winFrame, text="is equal to").grid(column=1, row=2,sticky=E)
        ttk.Label(self.winFrame, text="metres").grid(column=3,row=2,sticky=W)
        
        self.polishApp()
        self.window.mainloop()

    def polishApp(self):
        # add padding to every element inside winframe: A shorcut way
        for widget in self.winFrame.winfo_children():
            widget.grid_configure(padx=5, pady=5)
        
    def calculate(self,*args):
        try:
            # get a variable in tk
            cm=float(self.inputCentimeter.get())
            metres=cm/100
            # set variable
            self.outputMeters.set(metres)
        except ValueError:
            print("ValueError")
            pass


class Application:
    def __init__(self):
        # create window and frame
        self.root=Tk()
        self.root.title("Test algorithms")
        self.frame=ttk.Frame(self.root,padding="5 5 10 10")
        self.frame.grid(column=0,row=0, sticky=(N,S,W,E))
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)

        # start addign widgets
        self.number=StringVar()
        self.fibonacciAns=StringVar()
        self.factorialAns=StringVar()

        ttk.Entry(self.frame,textvariable=self.number,width=10).grid(
            column=1, row=1, sticky=(E,N)
        )
        ttk.Button(self.frame,text="Fibonacci",command=self.fibonacci).grid(column=2, row=1, sticky=(W,E))
        ttk.Button(self.frame, text="Factorial",command=self.factorial).grid(column=3,row=1, sticky=(W))
        ttk.Label(self.frame, textvariable=self.fibonacciAns).grid(
            column=2, row=2, sticky=(W,E)
        )
        self.root.mainloop()


    def fibonacci(self):
        number=int(self.number.get())
        first,second,third=0,1,0
        if(number<2):
            self.fibonacciAns.set(str(number-1))
        i=2
        while(i<number):
            third=first+second
            first=second
            second=third
            i+=1
        self.fibonacciAns.set(str(third))
        

    def factorial(self):
        number=int(self.number.get())
        ans=1
        for i in range(1,number+1):
            ans*=i
        self.factorialAnswer.set(str(ans))       

#Every element is a widget in tk
if __name__=="__main__":
    # app=App()
    app=Application()
    print(app.__dict__)
    



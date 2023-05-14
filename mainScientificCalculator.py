#Main Program for Calculator
import tkinter as tk
import math

#These functions have to be declared outside the Calculator class
def trimZeroes(x): #CUTS ALL LEADING ZEROES AND REMOVES THE DECIMAL IF DECIMAL PART IS EMPTY
    if "." in x:
        y = x.rstrip("0")
        if y[len(y) - 1] == ".":
            y = y[:-1]
        return y
    return x

def trimDecimal(x):
    if "." in x:
        i = 0 #Length of the exponent in the scientific notation
        notation = "" #The notation part of the number (e+ and the numbers after it)
        y = x
        z = 0 #Length of the notation with e+
        a = len((x.split(".")[1]).split("e+")[0])
        if "e+" in x:
            while x[len(x)-2-i:len(x)-i] != "e+":
                notation += x[len(x)-1-i]
                i += 1
            notation = "e+" + notation[::-1]
            y = x[:-i-2]
            z = 2 + i
        b = 0
        while len(y) > (17 - z) and "." in y:
            y = str(round(float(y), a-b))
            b += 1
        return y + notation
    else:
        return x

def scientificNotation(x): #CONVERTS TO SCIENTIFIC NOTATION IF STRING IS MORE THAN 17 CHARACTERS
    if float(x) >= 10**17 and "e+" not in x:
        y = "{:e}".format(float(x))
        return str(y)
    return x

def formatValues(x): #A single function is used to call the 3 other functions that format the number. This is to make the code look less clunky
    return trimZeroes(scientificNotation(trimDecimal(x)))

def degOrRad(x, mode, inverse): #CONVERTS ANGLE TO DEGREES OR RADIANS IF DEGREE MODE IS USED SINCE PYTHON TRIGONOMETRY IS IN RADIANS BY DEFAULT
    if mode == "Deg":
        if inverse == True:
            return math.degrees(x)
        else:
            return math.radians(x)
    elif mode == "Rad":
        return x

#MAIN CLASS FOR CALCULATOR OBJECT
class Calculator:

    #Global Variables
    global canEnter #TO INDICATE IF THE NEXT VALUE INPUTTED WILL OVERWRITE THE SCREEN OR NOT (SINCE THIS WILL BE THE NEXT TERM)
    canEnter = False
    global decimalPressed #TO INDICATE IF THE DECIMAL IS ALREADY USED SINCE OBVIOUSLY THERE CANNOT BE MULTIPLE DECIMAL PERIODS IN A NUMBER
    decimalPressed = False
    global expression #THE STRING EXPRESSION THAT WILL BE EVALUATED WHEN THE EQUALS (=) BUTTON IS PRESSED
    expression = ""
    global nRoot #TO INDICATE IF nth ROOT FUNCTION IS USED. DUE TO HOW IT'S INTERPRETED, IT USES A BRACKET. SO WE MUST CLOSE THE BRACKET BEFORE EVALUATION
    nRoot = False

    def __init__(self):

        #Base Window
        self.display = tk.Tk()
        self.display.title("Calculator")
        self.display.geometry("247x379")
        self.display.grid_propagate(False)
        self.display.resizable(False, False)
        self.display.configure(bg="#a0c8f0")

        #Constant Grid Sizes Declared and Initialized
        self.display.grid_propagate(False)
        for i in range(8):
            self.display.rowconfigure(i, weight=1)
        for j in range(5):
            self.display.columnconfigure(j, weight=1)

        #Label Displaying Selected Trigonometry Mode (Radians or Degrees)
        self.trigMode = tk.Label(self.display, text="Current Mode: Deg", font=('Cascadia Mono SemiLight', 9), anchor='w', bg="#a0c8f0")
        self.trigMode.grid(row=0, column=0, columnspan=5, sticky="news", padx=1, pady=1)

        #Label Displaying Output
        self.output = tk.Label(self.display, text="0", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 18), anchor="e", bg="White")
        self.output.grid(row=1, column=0, columnspan=5, sticky="news", padx=1, pady=1)

        #Row 1 Buttons
        self.alternate = tk.Button(self.display, text="2nd", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12,), bg="#393939", fg="white", activebackground="#535353", activeforeground="white", command=lambda x="2nd": self.alternateMode(x))
        self.alternate.grid(row=2, column=0, sticky="news", padx=1, pady=1)
        self.sin = tk.Button(self.display, text="sin", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white", command=lambda x="sin": self.specialPress(x))
        self.sin.grid(row=2, column=1, sticky="news", padx=1, pady=1) #2ND BUTTON CONVERTS TO ARCSIN
        self.cos = tk.Button(self.display, text="cos", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white", command=lambda x="cos": self.specialPress(x))
        self.cos.grid(row=2, column=2, sticky="news", padx=1, pady=1) #2ND BUTTON CONVERTS TO ARCCOS
        self.tan = tk.Button(self.display, text="tan", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white", command=lambda x="tan": self.specialPress(x))
        self.tan.grid(row=2, column=3, sticky="news", padx=1, pady=1) #2ND BUTTON CONVERTS TO ARCTAN
        self.clearButton = tk.Button(self.display, text="AC", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), anchor="center", bg="#1d3b53", activebackground="#336b91", fg="white", activeforeground="white", command=self.clearOutput)
        self.clearButton.grid(row=2, column=4, sticky="news", padx=1, pady=1)

        #Row 2 Buttons
        self.eX = tk.Button(self.display, text="e\u02e3", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white", command=lambda x="eX": self.specialPress(x))
        self.eX.grid(row=3, column=0, sticky="news", padx=1, pady=1) #2ND BUTTON CONVERTS THIS TO "ln"
        self.tenX = tk.Button(self.display, text="10\u02e3", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white", command=lambda x="tenX": self.specialPress(x))
        self.tenX.grid(row=3, column=1, sticky="news", padx=1, pady=1)
        self.factorial = tk.Button(self.display, text="x!", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white", command=lambda x="!": self.specialPress(x))
        self.factorial.grid(row=3, column=2, sticky="news", padx=1, pady=1)
        self.pi = tk.Button(self.display, text="\u03c0", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white", command=lambda x="pi": self.specialPress(x))
        self.pi.grid(row=3, column=3, sticky="news", padx=1, pady=1)
        self.division = tk.Button(self.display, text="\u00f7", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 18), bg="#ebebeb", activebackground="white", command=lambda x="/": self.arithmeticPress(x))
        self.division.grid(row=3, column=4, sticky="news", padx=1, pady=1)

        #Row 3 Buttons
        self.power = tk.Button(self.display, text="^", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white",command=lambda x="**": self.arithmeticPress(x))
        self.power.grid(row=4, column=0, sticky="news", padx=1, pady=1)
        self.number7 = tk.Button(self.display, text="7", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="7": self.numberPress(x))
        self.number7.grid(row=4, column=1, sticky="news", padx=1, pady=1)
        self.number8 = tk.Button(self.display, text="8", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="8": self.numberPress(x))
        self.number8.grid(row=4, column=2, sticky="news", padx=1, pady=1)
        self.number9 = tk.Button(self.display, text="9", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="9": self.numberPress(x))
        self.number9.grid(row=4, column=3, sticky="news", padx=1, pady=1)
        self.multiplication = tk.Button(self.display, text="\u00d7", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 18), command=lambda x="*": self.arithmeticPress(x))
        self.multiplication.grid(row=4, column=4, sticky="news", padx=1, pady=1)
        
        #Row 4 Buttons
        self.squarePower = tk.Button(self.display, text="x\u00b2", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white", command=lambda x="square": self.specialPress(x))
        self.squarePower.grid(row=5, column=0, sticky="news", padx=1, pady=1) #2ND BUTTON CONVERTS TO SQUARE ROOT
        self.number4 = tk.Button(self.display, text="4", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="4": self.numberPress(x))
        self.number4.grid(row=5, column=1, sticky="news", padx=1, pady=1)
        self.number5 = tk.Button(self.display, text="5", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="5": self.numberPress(x))
        self.number5.grid(row=5, column=2, sticky="news", padx=1, pady=1)
        self.number6 = tk.Button(self.display, text="6", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="6": self.numberPress(x))
        self.number6.grid(row=5, column=3, sticky="news", padx=1, pady=1)
        self.subtraction = tk.Button(self.display, text="-", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 18), bg="#ebebeb", activebackground="white", command=lambda x="-": self.arithmeticPress(x))
        self.subtraction.grid(row=5, column=4, sticky="news", padx=1, pady=1)

        #Row 5 Buttons
        self.answer = tk.Button(self.display, text="ans", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#ebebeb", activebackground="white", command=lambda x=None: self.answerPress(x))
        self.answer.grid(row=6, column=0, sticky="news", padx=1, pady=1) #STORES PREVIOUS CALCULATION'S ANSWER
        self.number1 = tk.Button(self.display, text="1", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="1": self.numberPress(x))
        self.number1.grid(row=6, column=1, sticky="news", padx=1, pady=1)
        self.number2 = tk.Button(self.display, text="2", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="2": self.numberPress(x))
        self.number2.grid(row=6, column=2, sticky="news", padx=1, pady=1)
        self.number3 = tk.Button(self.display, text="3", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="3": self.numberPress(x))
        self.number3.grid(row=6, column=3, sticky="news", padx=1, pady=1)
        self.addition = tk.Button(self.display, text="+", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 18), bg="#ebebeb", activebackground="white", command=lambda x="+": self.arithmeticPress(x))
        self.addition.grid(row=6, column=4, sticky="news", padx=1, pady=1)

        #Row 6 Buttons
        self.trigonometry = tk.Button(self.display, text="Rad", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#b1b1b1", activebackground="#e6e6e6", command=lambda x="Rad": self.changeTrigonometry(x))
        self.trigonometry.grid(row=7, column=0, sticky="news", padx=1, pady=1) #CHANGES BETWEEN DEGREES AND RADIANS
        self.number0 = tk.Button(self.display, text="0", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12), bg="#5ab9ea", activebackground="#77d1ff", command=lambda x="0": self.numberPress(x))
        self.number0.grid(row=7, column=1, sticky="news", padx=1, pady=1)
        self.decimal = tk.Button(self.display, text=".", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12, 'bold'), bg="#ebebeb", activebackground="white", command=self.decimalPress)
        self.decimal.grid(row=7, column=2, sticky="news", padx=1, pady=1)
        self.sign = tk.Button(self.display, text="(-)", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 12, 'bold'), bg="#ebebeb", activebackground="white", command=lambda x="(-)": self.specialPress(x))
        self.sign.grid(row=7, column=3, sticky="news", padx=1, pady=1)
        self.equals = tk.Button(self.display, text="=", borderwidth=1, relief="solid", font=('Cascadia Mono SemiLight', 18), bg="#4d7ea8", activebackground="#649fb7", fg="white", activeforeground="white", command=self.evaluate)
        self.equals.grid(row=7, column=4, sticky="news", padx=1, pady=1)

        #Activate
        self.display.mainloop()
    
    def numberPress(self, value):
        global canEnter
        if self.output['text'] != "0" or value != "0":
            if canEnter == False:
                self.output.config(text="")
                canEnter = True
            if len(self.output['text']) < 17:
                self.clearButton.config(text="C")
                self.output.config(text=self.output['text']+value)

    def answerPress(self, value):
        if value != None:
            global canEnter
            global decimalPressed
            self.output.config(text=value)
            canEnter = False
            decimalPressed = False
    
    def specialPress(self, value): #THESE FUNCTIONS EVALUATE THE CURRENT VALUES ON THE SCREEN INSTEAD OF ADDING THEM TO THE CUMULATIVE "expression" VARIABLE
        global canEnter
        global decimalPressed
        try:
            if value == "sin":
                self.output.config(text=formatValues(str(math.sin(degOrRad(float(self.output['text']), self.trigMode['text'][-3:], False)))))
            elif value =="arcsin":
                self.output.config(text=formatValues(str(degOrRad(math.asin(float(self.output['text'])), self.trigMode['text'][-3:], True))))
            elif value == "cos":
                self.output.config(text=formatValues(str(math.cos(degOrRad(float(self.output['text']), self.trigMode['text'][-3:], False)))))
            elif value =="arccos":
                self.output.config(text=formatValues(str(degOrRad(math.acos(float(self.output['text'])), self.trigMode['text'][-3:], True))))
            elif value == "tan":
                self.output.config(text=formatValues(str(math.tan(degOrRad(float(self.output['text']), self.trigMode['text'][-3:], False)))))
            elif value =="arctan":
                self.output.config(text=formatValues(str(degOrRad(math.atan(float(self.output['text'])), self.trigMode['text'][-3:], True))))
            elif value == "eX": #e to the power of x
                self.output.config(text=formatValues(str(math.e**(float(self.output['text'])))))
            elif value =="ln": #Natural Log
                self.output.config(text=formatValues(str(math.log(float(self.output['text'])))))
            elif value == "tenX": #10 to the power of x
                self.output.config(text=formatValues(str(10**(float(self.output['text'])))))
            elif value =="log": #Log Base 10
                self.output.config(text=formatValues(str((math.log(float(self.output['text'])))/math.log(10))))
            elif value == "!": #Factorial
                self.output.config(text=formatValues(str(math.factorial(int(self.output['text'])))))
            elif value == "pi":
                self.output.config(text=formatValues(str(math.pi)))
            elif value == "square":
                self.output.config(text=formatValues(str(float(self.output['text'])**2)))
            elif value == "squareRoot":
                self.output.config(text=formatValues(str(math.sqrt(float(self.output['text'])))))
            elif value == "(-)" and self.output['text'] != "0":
                if self.output['text'][0] != "-" and len("-" + self.output['text']) <= 17:
                    self.output.config(text="-"+self.output['text'])
                elif self.output['text'][0] == "-":
                    self.output.config(text=self.output['text'][1:])
        except:
            self.output.config(text="ERROR")
        if value != "(-)":
            canEnter = False
            decimalPressed = False
    
    def decimalPress(self):
        global canEnter
        global decimalPressed
        if decimalPressed == False:
            if canEnter == False:
                self.output.config(text="0")
                self.clearButton.config(text="C")
                canEnter = True
            self.output.config(text=trimDecimal(self.output['text']+"."))
            decimalPressed = True
    
    def arithmeticPress(self, symbol):
        global canEnter
        global decimalPressed
        global expression
        global nRoot
        if nRoot == True:
            expression = expression + self.output['text'] + ")" + symbol
            nRoot = False
        else:
            expression = expression + self.output['text'] + symbol
        if symbol == "**(1/":
            nRoot = True
        canEnter = False
        decimalPressed = False
    
    def clearOutput(self):
        global canEnter
        global decimalPressed
        global expression
        self.clearButton.config(text="AC")
        self.output.config(text="0")
        canEnter = False
        decimalPressed = False
        expression = ""
    
    def changeTrigonometry(self, mode):
        if mode == "Rad":
            self.trigMode.config(text="Current Mode: Rad")
            self.trigonometry.config(text="Deg", command=lambda x="Deg": self.changeTrigonometry(x))
        elif mode == "Deg":
            self.trigMode.config(text="Current Mode: Deg")
            self.trigonometry.config(text="Rad", command=lambda x="Rad": self.changeTrigonometry(x))

    def alternateMode(self, mode):
        if mode == "2nd": #CHANGE ALL OF THE DESIGNATED BUTTONS TO THEIR 2ND MODE
            self.sin.config(text="sin\u207b\u00b9", command=lambda x="arcsin": self.specialPress(x))
            self.cos.config(text="cos\u207b\u00b9", command=lambda x="arccos": self.specialPress(x))
            self.tan.config(text="tan\u207b\u00b9", command=lambda x="arctan": self.specialPress(x))
            self.eX.config(text="ln", command=lambda x="ln": self.specialPress(x))
            self.tenX.config(text="log", command=lambda x="log": self.specialPress(x))
            self.power.config(text="\u02e3\u221a", command=lambda x="**(1/": self.arithmeticPress(x))
            self.squarePower.config(text="\u221a", command=lambda x="squareRoot": self.specialPress(x))
            self.alternate.config(text="1st", command=lambda x="1st": self.alternateMode(x))
        elif mode == "1st": #CHANGE ALL OF THE DESIGNATED BUTTONS TO THEIR 1ST MODE
            self.sin.config(text="sin", command=lambda x="sin": self.specialPress(x))
            self.cos.config(text="cos", command=lambda x="cos": self.specialPress(x))
            self.tan.config(text="tan", command=lambda x="tan": self.specialPress(x))
            self.eX.config(text="e\u02e3", command=lambda x="eX": self.specialPress(x))
            self.tenX.config(text="10\u02e3", command=lambda x="tenX": self.specialPress(x))
            self.power.config(text="^", command=lambda x="**": self.arithmeticPress(x))
            self.squarePower.config(text="x\u00b2", command=lambda x="square": self.specialPress(x))
            self.alternate.config(text="2nd", command=lambda x="2nd": self.alternateMode(x))
    
    def evaluate(self): #CALL SEPERATE PYTHON FILE TO EVALUATE THE STRING
        global canEnter
        global decimalPressed
        global expression
        global nRoot
        expression = expression + self.output['text']
        if nRoot == True:
            expression = expression + ")"
            nRoot = False
        try:
            finalAnswer = formatValues(str(eval(expression)))
            self.answer.config(command=lambda x=finalAnswer: self.answerPress(x))
            self.output.config(text=finalAnswer)
        except:
            self.output.config(text="ERROR")
        canEnter = False
        decimalPressed = False
        expression = ""

if __name__ == "__main__":
    Calculator()
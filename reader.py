import tkinter as tk
import time
from card import Card
import base64



class Reader:
    def __init__(self, root):
        self.card = Card("CAP READER")
        self.isCardInserted = False
        self.mode = "nocard"
        self.okCounter = 0
        self.challenge = ""
        self.amount = ""
        self.code = ""

        self.root = root
        root.title("CAP reader")

        self.screen = tk.Text(root, state="disabled", width=20, height=2, background ="gray", foreground="black")
        self.screen.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.screen.configure(state='normal', font=("Times New Roman", 18))

        self.displayText = ''

        b0 = self.createButton(0)
        b1 = self.createButton(1)
        b2 = self.createButton(2)
        b3 = self.createButton(3)
        b4 = self.createButton(4)
        b5 = self.createButton(5)
        b6 = self.createButton(6)
        b7 = self.createButton(7)
        b8 = self.createButton(8)
        b9 = self.createButton(9)
        m1b = self.createButton('m1',None,10,'red')
        m2b = self.createButton('m2',None,10,'blue')
        okb = self.createButton('OK',None,10,'green')
        cb = self.createButton('C',None,10,'yellow')
        self.insertb = self.createButton('Insert', None, 10, 'orange')

        collectionOfButtons = [m1b,self.insertb,m2b,b1,b2,b3,b4,b5,b6,b7,b8,b9,cb,b0,okb]

        count = 0

        for row in range(1,6):
            for column in range(3):
                if(collectionOfButtons[count] != None):
                    collectionOfButtons[count].grid(row=row, column=column)
                count += 1


    def createButton(self, val, write=True, width=10, color=None):
        return tk.Button(self.root, text=val, command = lambda:self.click(val,write), width=width, background=color)


    def click(self, text, write):
        if(write==None):
            #TODO
            if(text == 'm1'):
                self.handle_m1()
            elif(text == 'm2'):
                self.handle_m2()
            elif(text == "Insert"):
                if self.isCardInserted:
                    print("CAP READER: Card removed")
                    self.clear_screen()
                    self.mode = "noCard"
                    self.okCounter = 0
                    self.isCardInserted = False
                    self.insertb["text"] = "Insert"
                else:
                    self.insertb["text"] = "Remove"
                    self.isCardInserted = True
                    self.card_inserted()
            elif(text == 'OK'):
                self.handle_ok()
            elif(text == 'C'):
                self.delete_entry()
        else:
            self.insert_screen(text)


    def insert_screen(self, value, newline=False):
        self.screen.configure(state='normal', font=("Times New Roman", 18))
        self.screen.insert(tk.END, value)
        self.displayText += str(value)
        if newline:
            self.displayText += "\n"
        self.screen.configure(state ='disabled', font=("Times New Roman", 18))


    def get_screen_input(self):
        txt = self.displayText
        txt = txt.split("\n")
        return txt[1]


    def clear_screen(self):
        self.displayText = ''
        self.screen.configure(state='normal', font=("Times New Roman", 18))
        self.screen.delete('1.0', tk.END)


    def delete_entry(self):
        self.displayText = self.displayText[:-1]
        self.screen.configure(state='normal', font=("Times New Roman", 18))
        self.screen.delete('1.0',tk.END)
        self.screen.insert('1.0', self.displayText)


    def card_inserted(self):
        self.mode = "Woops"
        self.okCounter = 0
        print("CAP READER: Card inserted: " + self.card.cardNr, flush=True)
        self.clear_screen()
        self.insert_screen("Choose M1 or M2")

    #M1: Start M1 & ask for Challenge
    def handle_m1(self):
        print("CAP READER: Starting M1 procedure....")
        self.mode = "m1"
        self.ask_challenge()

    #M2: Start M2 & ask for PIN
    def handle_m2(self):
        print("CAP READER: Starting M2 procedure....")
        self.mode = "m2"
        self.ask_pin()


    def handle_ok(self):
        self.okCounter = self.okCounter + 1
        #M1: store challenge & Ask for pin code
        if self.mode == "m1" and self.okCounter == 1:
            self.challenge = self.get_screen_input()
            print("CAP READER: challenge entered: " + self.challenge)
            self.ask_pin()
        #M1: Verify pin & calc cryptograph
        elif self.mode == "m1" and self.okCounter == 2:
            print("CAP READER: verifying pin")
            if self.verify_pin():
                print("CAP READER: pin approved")
                self.calculate_m1_cryptograph()
            else:
                print("CAP READER: pin refused")
                self.wrong_pin()
        #M2: Verify pin & ask for Amount 
        elif self.mode == "m2" and self.okCounter == 1:
            print("CAP READER: verifying pin")
            if self.verify_pin():
                print("CAP READER: pin approved")
                self.ask_amount()
            else:
                print("CAP READER: pin refused")
                self.wrong_pin()
        #M2: Store amount & Ask for Valuta code
        elif self.mode == "m2" and self.okCounter == 2:
            self.amount = self.get_screen_input()
            self.amount = "00000000" + self.amount
            print("CAP READER: Amount entered: " + self.amount)
            self.ask_valuta_code()
        #M2 Store valuta code & show confirmation
        elif self.mode == "m2" and self.okCounter == 3:
            self.code = "0000" + self.get_screen_input()
            print("CAP READER: Valuta code entered: " + self.code)            
            self.ask_confirmation()
        #M2 Calc cryptograph
        elif self.mode == "m2" and self.okCounter == 4:
            self.clear_screen()
            self.calculate_m2_cryptograph()
        else:
            self.card_inserted()


    def calculate_m1_cryptograph(self):
        print("CAP READER: start calculating cryptograph")
        self.clear_screen()
        print("CAP READER: cryptograph: call generate_ac()")
        arqc, aac = self.card.generate_ac("arqc", self.challenge)
        response = self.calc_response(arqc)
        self.insert_screen("Response: \n" + str(response))


    def calculate_m2_cryptograph(self):
        print("CAP READER: start calculating cryptograph")
        self.clear_screen()
        print("CAP READER: cryptograph: call generate_ac()")
        arqc, aac = self.card.generate_ac("arqc", self.code, self.amount)
        response = self.calc_response(arqc)
        self.insert_screen("Response: \n" + str(response))


    def ask_pin(self):
        self.clear_screen()
        self.insert_screen("Pin code: \n")


    def verify_pin(self):
        pin = self.get_screen_input()
        return self.card.check_PIN(pin)


    def wrong_pin(self):
        self.okCounter = self.okCounter - 1
        self.clear_screen()
        self.insert_screen("Wrong pin!")
        time.sleep(3)
        self.ask_pin()


    def ask_challenge(self):
        self.clear_screen()
        self.insert_screen("Challenge: \n")


    def ask_amount(self):
        self.clear_screen()
        self.insert_screen("Amount: \n")


    def ask_valuta_code(self):
        self.clear_screen()
        self.insert_screen("Valuta code: \n")


    def ask_confirmation(self):
        self.clear_screen()
        self.insert_screen("Complete online \ntransaction?")


    def calc_response(self, arqc):
        print("CAP READER: Craft response with ARQC by XOR with unique bitmap")
        arqc = arqc.hex()
        arqc = "0x" + arqc
        arqc = int(arqc, 16)
        cardNr = "0x" + self.card.cardNr
        cardNr = int(cardNr, 16)
        result = hex(arqc ^ self.card.bitmask ^ cardNr)
        result = str(int(result, 16))[0:8]
        print("CAP READER: Response code: ", result)
        return result
        
root = tk.Tk()
cardReader = Reader(root)
root.mainloop()

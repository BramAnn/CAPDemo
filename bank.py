import tkinter as tk
from tkinter import ttk 
from card import Card
import random

class Bank:
    def __init__(self, root):
        self.userDetails = Card("BANKING APPLICATION")

        self.root = root
        self.challenge = self.generate_random_challenge()
        self.amount = self.generate_random_amount()
        self.code = "0709"
        root.title("Bank")
        root.geometry("600x560")

        tabControl = ttk.Notebook(root) 
        self.loginTab = ttk.Frame(tabControl) 
        self.transactionTab = ttk.Frame(tabControl)

        tabControl.add(self.loginTab, text ='Login') 
        tabControl.add(self.transactionTab, text ='Start transaction') 
        tabControl.pack(expand = 1, fill ="both") 

        self.initialize_login()
        self.initialize_transaction()
        

    def initialize_login(self):
        label = tk.Label(self.loginTab, text="Login", font=("Times New Roman", 20))
        label.place(x=40, y=20)

        bankNummerLabel = tk.Label(self.loginTab, text="1. Please enter Card Number:", font=("Times New Roman", 14))
        bankNummerLabel.place(x=30, y=60)

        self.bankNummerTextField = tk.Text(self.loginTab, font=("Times New Roman", 14), width=30, height=1)
        self.bankNummerTextField.place(x=30, y=90)
        
        insertCardLabel = tk.Label(self.loginTab, text="2. Please insert card into CAP reader", font=("Times New Roman", 14))
        insertCardLabel.place(x=30, y=130)

        pressM1Label = tk.Label(self.loginTab, text="3. Press M1 button", font=("Times New Roman", 14))
        pressM1Label.place(x=30, y=170)
        
        insertChallengeLabel = tk.Label(self.loginTab, text="4. Insert following challenge into CAP reader and press OK:", font=("Times New Roman", 14))
        insertChallengeLabel.place(x=30, y=210)
        
        self.challengeTextField = tk.Text(self.loginTab, font=("Times New Roman", 14), state="disabled", width=30, height=1, bg="gainsboro", foreground="black")
        self.set_challenge_Code(self.challenge)
        self.challengeTextField.place(x=30, y=240)

        insertPinLabel = tk.Label(self.loginTab, text="5. Insert your PIN on CAP reader and press OK:", font=("Times New Roman", 14))
        insertPinLabel.place(x=30, y=280)

        insertResponseLabel = tk.Label(self.loginTab, text="6. Type the response from the CAP reader:", font=("Times New Roman", 14))
        insertResponseLabel.place(x=30, y=320)
        
        self.responseTextField = tk.Text(self.loginTab, font=("Times New Roman", 14), width=30, height=1)
        self.responseTextField.place(x=30, y=350)

        tryLoginButton = tk.Button(self.loginTab, text="Login", width=25, height=3, bg="chartreuse3", command=lambda:self.verify_login_response())
        tryLoginButton.place(x=200, y=390)


    def set_challenge_Code(self, value):
        self.challengeTextField.configure(state='normal', font=("Times New Roman", 14))
        self.challengeTextField.insert(tk.END, value, "center")
        self.challengeTextField.tag_configure("center", justify='center')
        self.challengeTextField.tag_add("center", 1.0, "end")
        self.challengeTextField.configure(state ='disabled', font=("Times New Roman", 14))


    def initialize_transaction(self):
        label = tk.Label(self.transactionTab, text="Transaction", font=("Times New Roman", 20))
        label.place(x=40, y=20)

        bankNummerLabel2 = tk.Label(self.transactionTab, text="1. Please enter Card Number:", font=("Times New Roman", 14))
        bankNummerLabel2.place(x=30, y=60)

        self.bankNummerTransactionTextField = tk.Text(self.transactionTab, font=("Times New Roman", 14), width=30, height=1)
        self.bankNummerTransactionTextField.place(x=30, y=90)

        insertCardLabel = tk.Label(self.transactionTab, text="2. Please insert card into CAP reader", font=("Times New Roman", 14))
        insertCardLabel.place(x=30, y=130)
        
        pressM2Label = tk.Label(self.transactionTab, text="3. Press M2 button", font=("Times New Roman", 14))
        pressM2Label.place(x=30, y=170)

        insertPinLabel = tk.Label(self.transactionTab, text="4. Insert your PIN on CAP reader and press OK:", font=("Times New Roman", 14))
        insertPinLabel.place(x=30, y=210)
        
        insertAmountLabel = tk.Label(self.transactionTab, text="5. Insert the amount in the CAP reader and press OK", font=("Times New Roman", 14))
        insertAmountLabel.place(x=30, y=250)

        self.amountTextField = tk.Text(self.transactionTab, font=("Times New Roman", 14), state="disabled", width=30, height=1, bg="gainsboro", foreground="black")
        self.set_amount_field(self.amount)
        self.amountTextField.place(x=30, y=280)

        insertCodeLabel = tk.Label(self.transactionTab, text="6. Insert following code in the CAP reader and press OK 2 times:", font=("Times New Roman", 14))
        insertCodeLabel.place(x=30, y=320)

        self.codeTextField = tk.Text(self.transactionTab, font=("Times New Roman", 14), state="disabled", width=30, height=1, bg="gainsboro", foreground="black")
        self.set_code_field(self.code)
        self.codeTextField.place(x=30, y=350)
        
        insertResponseLabel = tk.Label(self.transactionTab, text="7. Type the response from the CAP reader:", font=("Times New Roman", 14))
        insertResponseLabel.place(x=30, y=390)
        
        self.responseTransactionTextField = tk.Text(self.transactionTab, font=("Times New Roman", 14), width=30, height=1)
        self.responseTransactionTextField.place(x=30, y=420)

        checkResponseButton = tk.Button(self.transactionTab, text="Check transaction", width=25, height=3, bg="chartreuse3", command=lambda:self.verify_transaction_response())
        checkResponseButton.place(x=200, y=460)


    def set_amount_field(self, value):
        self.amountTextField.configure(state='normal', font=("Times New Roman", 14))
        self.amountTextField.insert(tk.END, value, "center")
        self.amountTextField.tag_configure("center", justify='center')
        self.amountTextField.tag_add("center", 1.0, "end")
        self.amountTextField.configure(state = 'disabled', font=("Times New Roman", 14))

    def set_code_field(self, value):
        self.codeTextField.configure(state='normal', font=("Times New Roman", 14))
        self.codeTextField.insert(tk.END, value, "center")
        self.codeTextField.tag_configure("center", justify='center')
        self.codeTextField.tag_add("center", 1.0, "end")
        self.codeTextField.configure(state ='disabled', font=("Times New Roman", 14))


    def verify_login_response(self):
        cardnr = self.read_card_nr()
        print("BANKING APPLICATION: card number entered: " + str(cardnr))
        arqc, aac = self.userDetails.generate_ac("arqc", self.challenge)
        bankResponse = self.calc_response(arqc)
        userResponse = self.read_login_response()
        print("BANKING APPLICATION: Comparing response....")
        if bankResponse == userResponse:
            print("BANKING APPLICATION: Succes: user authenticated")
        else:
            print("BANKING APPLICATION: Failed: user NOT authenticated")

    def verify_transaction_response(self):
        cardNr = self.read_card_nr_transcation()
        print("BANKING APPLICATION: card number entered: " + str(cardNr))
        self.amount = "00000000" + self.amount
        self.code = "0000" + self.code
        arqc, aac = self.userDetails.generate_ac("arqc", self.code, self.amount)
        bankResponse = self.calc_response(arqc)
        userResponse = self.read_transaction_response()
        print("BANKING APPLICATION: Comparing response....")
        if(bankResponse == userResponse):
            print("BANKING APPLICATION: Succes: transaction authorised")
        else:
            print("BANKING APPLICATION: Failed: transaction NOT authorised")

    def read_card_nr(self):
        text = self.bankNummerTextField.get("1.0","end-1c")
        self.userDetails.cardNr = text
        return text
    
    def read_card_nr_transcation(self):
        text = self.bankNummerTransactionTextField.get("1.0", "end-1c")
        self.userDetails.cardNr = text
        return text
    
    def read_login_response(self):
        response = self.responseTextField.get("1.0","end-1c")
        return response

    def read_transaction_response(self):
        response = self.responseTransactionTextField.get("1.0", "end-1c")
        return response


    def generate_random_challenge(self):
        challenge = random.randint(10000000, 99999999)
        return challenge

    
    def generate_random_amount(self):
        amount = random.randint(10,99)
        return "00" + str(amount)


    def calc_response(self, arqc):
        print("BANKING APPLICATION: Craft response with ARQC by XOR with unique bitmap")
        arqc = arqc.hex()
        arqc = "0x" + arqc
        arqc = int(arqc, 16)
        cardNr = "0x" + self.userDetails.cardNr
        cardNr = int(cardNr, 16)
        result = hex(arqc ^ self.userDetails.bitmask ^ cardNr)
        result = str(int(result, 16))[0:8]
        print("BANKING APPLICATION: Correct response code: ", result)

        return result



root = tk.Tk()
BankApp = Bank(root)
root.mainloop()

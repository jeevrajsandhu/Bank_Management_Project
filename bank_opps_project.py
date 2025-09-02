# New Bank Account (acco unt_number, account_holder_name, balance)
# Deposit money
# Withdraw money
# Check Details
# Update account details
# Close account

import json
import random
import string
from pathlib import Path




class Bank:
    database = 'bank_data.json'
    data = [] # Dummy Data for future updates in accounts
    
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.load(fs)
        else: 
            print("No such file exists")                
    except Exception as err:
        print(f"An error occurred while reading the database: {err}")

    @classmethod
    def __update(cls): # For saving the data into json format ///// cls means Bank class
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgernate(account_no):
        alpha = random.choices(string.ascii_letters, k=3) # small a to z and big A to Z randomly selected 3 times
        num = random.choices(string.digits, k=3) # 0 to 9 randomly selected 4 times
        special = random.choice(string.punctuation ) # randomly selected one special character like '@', '#', '$', '%', etc.
        
        # alpha= ['a', 'b', 'c'] , num= ['1', '2', '3'] and special= '#' 
        # List + String through error thats why we convert special into list to concatenate
        id = alpha + num + [special] 
        random.shuffle(id)
        return ''.join(id) # it convert list[1,2,3] into string '123'



    def create_account(self):
        info = {
            "name": input("Enter your name: "),
            "age": int(input("Enter your age:")),
            "email": input("Enter your email: "),
            "pin": int(input("Enter your 4 digit PIN: ")),
            "account_no": Bank.__accountgernate(),
            "balance": 0
        }

        if info["age"]<18 or len(str(info['pin'])) != 4:
            print("You are not eligible to create an account")
        
        else:
            print("Account created successfully!")

        for i in info:
            print(f"{i}: {info[i]}")
        print("Plese note down your account number for future transactions.")

        Bank.data.append(info)
        Bank.__update()


    def deposit_money(self):
        acc_no = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))
        
        userdata = [i for i in Bank.data if i['account_no'] == acc_no and i['pin'] == pin]

        if not userdata:
            print("Invalid account number or PIN")

        else:
            amount = int(input("Enter the amount to deposit: "))
            if amount>100000:
                print("Deposit amount is too high")
            elif amount<0:
                print("Invalid deposit amount")        
            else:
                userdata[0]['balance'] += amount 
                # our data is in list [{name:John,etc}, #Random] so we use userdata[0] to access the dictionary 
                # userdata[1] access Random but we need to access the dictionary of userdata[0]
                Bank.__update()
                print(f"Deposited {amount} successfully!") 
                print(f"Total Balance: {userdata[0]['balance']}")               


    def withdraw_money(self):
        acc_no = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))

        userdata = [i for i in Bank.data if i['account_no'] == acc_no and i['pin'] == pin]

        if not userdata:
            print("Invalid account number or PIN")

        
        else:
            print(f"Your current balance is: {userdata[0]['balance']}")
            amount = int(input("Enter the amount to withdraw: "))
            if amount>userdata[0]['balance']:
                print("Insufficient balance")
            elif amount<0:
                print("Invalid withdrawal amount")
            else:
                userdata[0]['balance'] -= amount 
                Bank.__update()
                print(f"Withdrew {amount} successfully!") 
                print(f"Total Balance: {userdata[0]['balance']}")

 
    def show_details(self):
        acc_no = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))

        userdata = [i for i in Bank.data if i['account_no'] == acc_no and i['pin'] == pin]

        if not userdata:
            print("Invalid account number or PIN")
        else:
            print("Account Details:")
            for i in userdata[0]:
                print(f"{i}: {userdata[0][i]}")


    def update_account_details(self):
        acc_no = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))
        userdata = [i for i in Bank.data if i['account_no']== acc_no and i['pin'] == pin]
        if not userdata:
            print("Invalid account number or PIN")

        else:
            print("You cannot change your account number, age, balance")
            print("Enter the new details:")
            newdata = {
                "name": input("Enter your name: "),
                "email": input("Enter your email: "),
                "pin": int(input("Enter your 4 digit PIN: "))
            }
            if newdata['name'] == '':
                newdata['name'] = userdata[0]['name']
            if newdata['email'] == '':
                newdata['email'] = userdata[0]['email']
            if newdata['pin'] == '':
                newdata['pin'] = userdata[0]['pin']     

            newdata['age'] = userdata[0]['age']
            newdata['account_no'] = userdata[0]['account_no']
            newdata['balance'] = userdata[0]['balance'] 

            if type(newdata['pin'])== str:
                newdata['pin'] == int(newdata['pin'])


            userdata[0].update(newdata)
            Bank.__update()
            print("Account details updated successfully!")    
        #     print("Your new account details:")        
        # self.show_details()

    def delete_account(self):
        acc_no = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))
        userdata = [i for i in Bank.data if i['account_no']== acc_no and i['pin'] == pin]
        if not userdata:
            print("Invalid account number or PIN")
        else:
            check = input("Press y to delete the account. Otherwise, press any other key: ")
            if check.lower() != 'y':
                print("Account not deleted!")

            else:
                Bank.data.remove(userdata[0])
                Bank.__update()
                print("Account deleted successfully!")     

user = Bank()
print("Press 1 for creating a new account")
print("Press 2 for depositing money")
print("Press 3 for withdrawing money")
print("Press 4 for checking account details")
print("Press 5 for updating account details")
print("Press 6 for deleting the account")

check = int(input("Enter your choice: "))

if check == 1:
    user.create_account()

if check == 2:
    user.deposit_money()

if check == 3:
    user.withdraw_money()    

if check == 4:
    user.show_details()    

if check == 5:
    user.update_account_details()    

if check == 6:
    user.delete_account()    

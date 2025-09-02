import json
import random
import string
from pathlib import Path
import streamlit as st


class Bank:
    database = 'bank_data.json'
    data = []  
    
    # Load data
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.load(fs)
        else:
            data = []
    except Exception as err:
        st.error(f"Error reading database: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgernate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        special = random.choice(string.punctuation)
        id = alpha + num + [special]
        random.shuffle(id)
        return ''.join(id)

    def create_account(self, name, age, email, pin):
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_no": Bank.__accountgernate(),
            "balance": 0
        }

        if age < 18 or len(str(pin)) != 4:
            return None, "❌ You are not eligible to create an account"
        else:
            Bank.data.append(info)
            Bank.__update()
            return info, "✅ Account created successfully!"

    def deposit_money(self, acc_no, pin, amount):
        userdata = [i for i in Bank.data if i['account_no'] == acc_no and i['pin'] == pin]
        if not userdata:
            return None, "❌ Invalid account number or PIN"
        if amount <= 0:
            return None, "❌ Invalid deposit amount"
        if amount > 100000:
            return None, "❌ Deposit amount is too high"

        userdata[0]['balance'] += amount
        Bank.__update()
        return userdata[0], f"✅ Deposited {amount} successfully!"

    def withdraw_money(self, acc_no, pin, amount):
        userdata = [i for i in Bank.data if i['account_no'] == acc_no and i['pin'] == pin]
        if not userdata:
            return None, "❌ Invalid account number or PIN"
        if amount <= 0:
            return None, "❌ Invalid withdrawal amount"
        if amount > userdata[0]['balance']:
            return None, "❌ Insufficient balance"

        userdata[0]['balance'] -= amount
        Bank.__update()
        return userdata[0], f"✅ Withdrew {amount} successfully!"

    def show_details(self, acc_no, pin):
        userdata = [i for i in Bank.data if i['account_no'] == acc_no and i['pin'] == pin]
        if not userdata:
            return None, "❌ Invalid account number or PIN"
        return userdata[0], "✅ Account details fetched!"

    def update_account_details(self, acc_no, pin, name, email, new_pin):
        userdata = [i for i in Bank.data if i['account_no']== acc_no and i['pin'] == pin]
        if not userdata:
            return None, "❌ Invalid account number or PIN"

        userdata[0]['name'] = name if name else userdata[0]['name']
        userdata[0]['email'] = email if email else userdata[0]['email']
        userdata[0]['pin'] = new_pin if new_pin else userdata[0]['pin']

        Bank.__update()
        return userdata[0], "✅ Account details updated successfully!"

    def delete_account(self, acc_no, pin):
        userdata = [i for i in Bank.data if i['account_no']== acc_no and i['pin'] == pin]
        if not userdata:
            return None, "❌ Invalid account number or PIN"

        Bank.data.remove(userdata[0])
        Bank.__update()
        return None, "✅ Account deleted successfully!"


# ------------------- STREAMLIT UI ---------------------
bank = Bank()

st.title("🏦 Simple Bank Management System")

menu = st.sidebar.selectbox("Choose an action", 
    ["Create Account", "Deposit Money", "Withdraw Money", "Show Details", "Update Account", "Delete Account"]
)

# 1️⃣ Create account
if menu == "Create Account":
    st.subheader("🆕 Create New Account")
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0)
    email = st.text_input("Enter your email")
    pin = st.text_input("Enter 4-digit PIN", type="password")

    if st.button("Create Account"):
        if not pin.isdigit() or len(pin) != 4:
            st.error("❌ PIN must be 4 digits")
        else:
            info, msg = bank.create_account(name, int(age), email, int(pin))
            st.info(msg)
            if info:
                st.json(info)

# 2️⃣ Deposit money
elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")
    acc_no = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    amount = st.number_input("Enter Amount", min_value=0)
    if st.button("Deposit"):
        info, msg = bank.deposit_money(acc_no, int(pin), int(amount))
        st.info(msg)
        if info:
            st.json(info)

# 3️⃣ Withdraw money
elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")
    acc_no = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    amount = st.number_input("Enter Amount", min_value=0)
    if st.button("Withdraw"):
        info, msg = bank.withdraw_money(acc_no, int(pin), int(amount))
        st.info(msg)
        if info:
            st.json(info)

# 4️⃣ Show details
elif menu == "Show Details":
    st.subheader("📑 Account Details")
    acc_no = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    if st.button("Show"):
        info, msg = bank.show_details(acc_no, int(pin))
        st.info(msg)
        if info:
            st.json(info)

# 5️⃣ Update account
elif menu == "Update Account":
    st.subheader("✏️ Update Account")
    acc_no = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    name = st.text_input("Enter new name (leave blank to keep old)")
    email = st.text_input("Enter new email (leave blank to keep old)")
    new_pin = st.text_input("Enter new 4-digit PIN (leave blank to keep old)")
    if st.button("Update"):
        new_pin_val = int(new_pin) if new_pin.isdigit() else None
        info, msg = bank.update_account_details(acc_no, int(pin), name, email, new_pin_val)
        st.info(msg)
        if info:
            st.json(info)

# 6️⃣ Delete account
elif menu == "Delete Account":
    st.subheader("🗑 Delete Account")
    acc_no = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    if st.button("Delete"):
        _, msg = bank.delete_account(acc_no, int(pin))
        st.info(msg)

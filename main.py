from tkinter import *
import tkinter.ttk as ttk
import pandas
from pathlib import Path
import random
from tkinter import messagebox
import pyperclip

# ----- PASSWORD GENERATOR ----- #
def gen_btt_press():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_list = [random.choice(letters) for char in range(1, 8 + 1)] + [random.choice(symbols) for char in range(1, 4 + 1)] + [random.choice(numbers) for char in range(1, 2 + 1)]
    random.shuffle(password_list)
    password = ''.join(password_list)
    pwd_ent.delete(0, 'end')
    pwd_ent.insert(0, password)
    pyperclip.copy(password)
# ----- encryption ----- #
mix = ['g', '6', 'I', 'O', ' ', 'M', 'R', 'p', '0', '7', '@', '.', 'L', 'E', 'v', 'e', '!', 'D', 'h', '4', 'l', 'A', '+', 'q', 'y', 'S', 'K', 'P', 'H', '1', 'a', 'j', 'u', 'Y', 'J', ')', 'C', 'N', '$', 'd', '&', 'm', 'n', 'k', 'W', 'X', '%', '2', '(', 'b', 'i', '*', 'T', 'o', 'B', 'U', 'Q', '5', '3', 'x', 'G', 'c', 'Z', '9', 'w', 'F', 'z', 't', 'f', '#', 'r', 's', 'V', '8']

def cy(text, direction):
    text_list = []
    new_text = ''
    shift = len(text)
    for characters in text:
        text_list += characters
    if direction == 1:
        shift *= -1
    for characters in text_list:
        index = mix.index(characters)
        new_text += mix[(index + shift) % len(mix)]
    direction = ""
    shift = 0
    return new_text
# ----- SEARCH PASSWORD ----- #
def search_btn_press():
    entries = pandas.read_csv('passwords.csv')
    for (index, row) in entries.iterrows():
        if row.web == cy(web_ent.get(), 0):
            email_ent.delete(0, 'end')
            email_ent.insert(0, cy(row.email, 1))
            pwd_ent.delete(0, 'end')
            pwd_ent.insert(0, cy(row.pwd, 1))
# ----- SAVE DATA ----- #
def add_btn_press():
    if web_ent.get == '' or email_ent.get == '' or pwd_ent.get() == '':
        messagebox.showinfo(title='Empty detals', message='Please fill all boxes')
    else:
        with open('passwords.csv', 'a+') as passwords_file:
            entries = pandas.read_csv('passwords.csv')
            for (index, row) in entries.iterrows():
                if row.web == cy(web_ent.get(), 0):
                    messagebox.askretrycancel(title='Duplicate', message='Theres already an entry for this website')
                    break
                else:
                    is_ok = messagebox.askokcancel(title=web_ent.get(), message=f'Are you sure you want to save this entry?:\nEmail: {email_ent.get()}\nPassword:{pwd_ent.get()}')
                    if is_ok:
                        dic = {}
                        default_email()
                        passwords_file.write(f",{cy(web_ent.get(), 0)},{cy(email_ent.get(), 0)},{cy(pwd_ent.get(), 0)}\n")
                        stt_lbl.config(text='Entry added successfully')
                        break
                        web_ent.delete(0, 'end')
                        pwd_ent.delete(0, 'end')
                        pwd_ent.clipboard_append(pwd_ent.get())
# ----- SAVE DEFAULT PWD ----- #
def default_email():
    with open('default_email.txt', mode='w') as def_email_file:
        def_email_file.write(email_ent.get())
# ----- UI SETUP ----- #
# window -----
window = Tk()
window.title('My Password Manager')
window.config(padx=20, pady=20, bg='white', highlightthickness=0)
# images -----
    # logo
logo = Canvas()
logo_image = PhotoImage(file='./logo.png')
logo.config(width=200, height=200, bg='white', highlightthickness=0)
logo.create_image(100, 100,  image = logo_image)
logo.grid(column=1, row=0, )
# labels -----
    # status
stt_lbl = Label(bg='white', highlightthickness=0)
stt_lbl.grid(column=0, row=6, columnspan=3)
    # website
web_lbl = Label(text='Website:', bg='white', highlightthickness=0)
web_lbl.grid(column=0, row=1, sticky=E)
    # email
email_lbl = Label(text='Email/Username:', bg='white', highlightthickness=0)
email_lbl.grid(column=0, row=2, sticky=E)
    # pwd
pwd_lbl = Label(text='Password', bg='white', highlightthickness=0)
pwd_lbl.grid(column=0, row=3, sticky=E)
# entries -----
    # website
web_ent = ttk.Entry(width=52)
web_ent.focus()
web_ent.grid(column=1, row=1, columnspan=2)
    # email
email_ent = ttk.Entry(width=52)
path = Path('./default_email.txt')
if not path.is_file():
    default_email()
else:
    with open('default_email.txt') as file:
        email = file.read()
        email_ent.insert(0, email)
email_ent.grid(column=1, row=2, columnspan=2)
    # pwd
pwd_ent = ttk.Entry(width=34)
pwd_ent.grid(column=1, row=3)
# buttons -----
    # add
add_btn = ttk.Button(text='Add', width=52, command=add_btn_press)
add_btn.grid(column=1, row=4, columnspan=2)
    # search
add_btn = ttk.Button(text='Search', width=16, command=search_btn_press)
add_btn.grid(column=2, row=1)
    # generate
gen_btn = ttk.Button(text='Generate Password', command=gen_btt_press)
gen_btn.grid(column=2, row=3)












window.mainloop()
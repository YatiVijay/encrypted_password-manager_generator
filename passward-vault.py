#import required libraries
import sqlite3,hashlib
import string
import random
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter import messagebox
from functools import partial

#create database and table in it 
with sqlite3.connect("Password_Vault.db") as db:
    cursor=db.cursor()   #initialize daatbase

#create table to store signup password(only one)
cursor.execute("""
CREATE TABLE IF NOT EXISTS signup_password(
Id INTEGER PRIMARY KEY,
Password TEXT NOT NULL);
""")

#create table to store the added or generated password along with the username and site
cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
Id INTEGER PRIMARY KEY,
Website TEXT NOT NULL,
Username TEXT NOT NULL,
Password TEXT NOT NULL);
""")

#create popup to add rows of password into database
def popup(text):
    result=askstring("Input string",text)
    return result

#initialize tinker window
window =Tk()
window.title("Password Vault - YATI")
myfont=("Comic Sans MS",10,"bold")

#encrypt the signup password 
def hashed_password(text):
    hashed=hashlib.md5(text)
    hashed=hashed.hexdigest()
    return hashed


def signup():
    #design of window
    window.geometry("470x350")
    window.configure(background="#383736")
    window.maxsize(550,380)
    window.minsize(450,350)

    #frame for text - create password
    label=Label(window,bg="#383736",fg="white",text="Create Password", font=10)
    label.config(anchor=CENTER)
    label.pack(pady=15)

    #frame for user input for new password
    text=Entry(window,bg="#6B6A69",fg="#D4D4D4",width=20,bd=4,show="*",font=3)
    text.pack(ipady=5,pady=8)
    text.focus()

    #frame for text - re enter password
    label1=Label(window,bg="#383736",fg="white",text="Re-Enter Password", font=10)
    label1.config(anchor=CENTER)
    label1.pack(pady=15)

    #frame for user input for re enter password
    text1=Entry(window,bg="#6B6A69",fg="#D4D4D4",width=20,bd=4,show="*",font=3)
    text1.pack(ipady=5,pady=8)
    text1.focus()

    #frame for text if re enter and new password do not match 
    label2=Label(window,bg="#383736",fg="#C3C3C2",font=10)
    label2.pack(pady=7)

    #check if new and re enter password are same
    #if same then password get insert into the signup_password table in the database
    #if not then re enter password get deleted and label execute - Password do not match
    def save_password():
        if text.get()==text1.get():
            hash_password=hashed_password((text.get()).encode("utf-8"))
            insert_password="""INSERT INTO signup_password(Password) VALUES(?)"""
            cursor.execute(insert_password,[(hash_password)])
            db.commit()
            
            #if re enter and new password match then it redirect to window where password list is there
            #after inserting the signup password into the database signup_password table
            password_vault()
        else:
            text1.delete(0,"end")
            label2.config(text="Password do not match")

        
    #submit button which redirect to the save password 
    button=Button(window,bg="#807F7F",fg="white",text="Submit",bd=4,command=save_password,font=10)
    button.pack(pady=13)


def login_screen():
    #design of window
    window.geometry("370x250")
    window.configure(background="#383736")
    window.maxsize(400,250)
    window.minsize(300,250)

    #frame for text - enter password
    label=Label(window,bg="#383736",fg="white",text="Enter Password to Login", font=10)
    label.config(anchor=CENTER)
    label.pack(pady=15)

    #frame for user input for password
    text=Entry(window,bg="#6B6A69",fg="#D4D4D4",width=20,bd=4,show="*",font=3)
    text.pack(ipady=5,pady=10)
    text.focus()

    #frame for text - wrong password, comes when user password doesn't match to the database password
    label1=Label(window,bg="#383736",fg="#C3C3C2",font=10)
    label1.pack(pady=5)

    #get the password from signup_password table which is similar to the user enter password in login screen
    def get_signup_password():
        user_enter_password=hashed_password((text.get()).encode("utf-8"))
        cursor.execute("SELECT * FROM signup_password WHERE Id=1 AND Password=?",[(user_enter_password)])
        print(user_enter_password)   #user enter password encoded
        return cursor.fetchall()

    #after clicking submit, program check the user password is matching to the
    #existing password in the database at the time of sign up
    def check_password():
        match=get_signup_password()
        print(match)                 #stored password in the database encoded
                                    
        if match:                   #if match has a password similar to the user enter password
            password_vault()        #then redirect to the password_vault function
        else:
            text.delete(0,"end")    #if match is null then delete the user text
            label1.config(text="Wrong Password") #and give wrong passowrd at the place of label1


    #frame for submit button which redirect to check_password function
    #if its correct then will redirect to the vault window
    button=Button(window,bg="#807F7F",fg="white",text="Submit",bd=4,command=check_password,font=10)
    button.pack(pady=12)

#generate tough password after getting users values for website, username and length
#and the generated password will popup as information and the whole field will add to database
def generate_password(length):
    upper = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    lower = list("abcdefghijklmnopqrstuvwxyz")
    chars = list("@#%&()\"?!")
    numbers = list("1234567890")
    u=random.randint(1,length-3)
    l = random.randint(1, length-2-u)
    c = random.randint(1, length-1-u-l)
    n = length-u-l-c
    field = random.sample(upper, u)+random.sample(lower, l)+random.sample(chars, c)+random.sample(numbers, n)
    random.shuffle(field)
    password = "".join(field)
    
    messagebox.showinfo("Generated Password",password)
    return password

#if password correct then will redirect to the window where we can add,
#recover and see the list of password along with the other information 
def password_vault():
    for widget in window.winfo_children():
        widget.destroy()                   #destroy the login window 

    #add password username and website on ur own
    #which will add into the vault table 
    def add_entry():
        text1="Website"
        text2="Username"
        text3="Password"

        website=popup(text1)
        if website=="":
            messagebox.showerror("Error","Website field cannot be empty")
            return
        username=popup(text2)
        if username=="":
            messagebox.showerror("Error","Username field cannot be empty")
            return
        cursor.execute("SELECT Website,Username FROM vault")
        website_username=cursor.fetchall()
        for i in website_username:
            if i[0]==website and i[1]==username:
                messagebox.showwarning("Error","Entry already exist")
                break 
        password=popup(text3)
        if password=="":
            messagebox.showerror("Error","Password field cannot be empty")
            return
        

        insert_entry="""INSERT INTO vault(Website,Username,Password) VALUES(?,?,?)"""
        cursor.execute(insert_entry,(website,username,password))
        db.commit()

        #refresh to the previous window
        password_vault()
        
    #after clicking generate will redirect to generate function where will 
    #give website, username and length of password to get our own tough password
    def generate():
        text1="Website"
        text2="Username"
        text3="Password"
        text4="Length"
        #website and username can't be null
        #lenght can't be less than eight
        #length should be integer
        #give warning if website and username exist
        website=popup(text1)
        if website=="":
            messagebox.showerror("Error","Website field cannot be empty")
            return
        username=popup(text2)
        if username=="":
            messagebox.showerror("Error","Username field cannot be empty")
            return
        cursor.execute("SELECT Website,Username FROM vault")
        website_username=cursor.fetchall()
        for i in website_username:
            if i[0]==website and i[1]==username:
                messagebox.showwarning("Error","Entry already exist")
                break 
            
        Length=popup(text4)
        if Length.isdigit()==False:
            messagebox.showerror("Error","Length must be a integer")
            return
        if int(Length)<8:
            messagebox.showerror("Error","Password must be atleast 8 characters long")
            return
        
        password=generate_password(int(Length))
        insert_entry="""INSERT INTO vault(Website,Username,Password) VALUES(?,?,?)"""
        cursor.execute(insert_entry,(website,username,password))
        db.commit()
        password_vault()

    #delete the stored password into the database or window
    def delete_entry(text):
        #ask question if we really wnat to delete the field
        result=messagebox.askquestion("Delete","Are you sure?",icon='warning')
        if result=='yes':
            cursor.execute("DELETE FROM vault WHERE Id=?",[(text)])
            db.commit()
        else:
            pass

        #refresh to the previous window
        password_vault()

    #create password vault window
    window.geometry("970x500")
    window.configure(background="#2A2D35")
    window.maxsize(970,800)
    window.minsize(970,300)
        
    #frame for the text - heading(password vault)
    label=Label(window,bg="#343942",fg="#697285",text=" Password Vault ", font=("Comic Sans MS",35,"bold"))
    label.grid(row=0,column=1,pady=10,columnspan=2)

    #frame for the add button
    button=Button(window,font=("Times",11,"bold"),width=12,bg="#807F7F",fg="white",text="Add",bd=4,command=add_entry)
    button.grid(row=1,column=1,pady=25,padx=5)

    button=Button(window,font=("Times",11,"bold"),width=12,bg="#807F7F",fg="white",text="Generate",bd=4,command=generate)
    button.grid(row=1,column=2,pady=25,padx=5)

    #frame for the text under which entry get listed
    label=Label(window,bg="#2A2D35",fg="#F7F8FB",text=" Website ",font=("Helvetica",15,"bold italic"))
    label.grid(row=2,column=0,padx=80,pady=10)
    label=Label(window,bg="#2A2D35",fg="#F7F8FB",text=" Username ",font=("Helvetica",15,"bold italic"))
    label.grid(row=2,column=1,padx=80,pady=10)
    label=Label(window,bg="#2A2D35",fg="#F7F8FB",text=" Password ",font=("Helvetica",15,"bold italic"))
    label.grid(row=2,column=2,padx=80,pady=10)

    #check if the tabel contains entry to list out 
    cursor.execute("SELECT * FROM vault")
    if cursor.fetchall()!=None:
        i=0
        while True:
            cursor.execute("SELECT * FROM vault")
            entry_list=cursor.fetchall()

            #list out entry iteratively
            label1 = Label(window,bg="#2A2D35",fg="#9EABC8",text=entry_list[i][1],font=("Helvetica",12,"bold"))
            label1.grid(column=0,row=i+3)
            label1 = Label(window,bg="#2A2D35",fg="#9EABC8",text=entry_list[i][2],font=("Helvetica",12,"bold"))
            label1.grid(column=1,row=i+3)
            label1 = Label(window,bg="#2A2D35",fg="#9EABC8",text=entry_list[i][3],font=("Helvetica",12,"bold"))
            label1.grid(column=2,row=i+3)

            #delete vutton to delete the entry according to the id of entry 
            button=Button(window,font=("Times",10,"bold"),width=8,bg="#807F7F",fg="white",text="Delete",bd=4,command=partial(delete_entry,entry_list[i][0]))
            button.grid(column=3,row=i+3,pady=10)

            i=i+1

            #if all entry get list out then hold come out of the loop
            cursor.execute("SELECT * FROM vault")
            if (len(cursor.fetchall())<=i):
                break
            

            
    

#get the stored password - if null then redirect to signup else login
#password_vault()
cursor.execute("SELECT * FROM signup_password")
if cursor.fetchall():
    login_screen()
else:
    signup()

#run the window program
window.mainloop()

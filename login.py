import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import mysql.connector
from PIL import ImageTk
global_username = ""
# Connect to MySQL database
db = mysql.connector.connect(
    host ='localhost',
    username = 'root',
    password = '************',
    #database = 'studentmanagementsystem'
    )
cursor = db.cursor()
try:
    query='create database studentmanagementsystem'
    cursor.execute(query)
    query='use studentmanagementsystem'
    cursor.execute(query)
except:
    query='use studentmanagementsystem'
    cursor.execute(query)

root = tk.Tk()
root.title("Login and Create Account")
root.geometry('1280x700+0+0')

root.resizable(False,False)

def create_table():
    global_username = create_username_entry.get()
    table_name = create_username_entry.get()
    query=f'create table {table_name}(id int, name varchar(30),mobile varchar(10),email varchar(30),' \
                  'address varchar(100),gender varchar(20),dob varchar(20),date varchar(50), time varchar(50))'
   # query = f"CREATE TABLE {table_name} (id varchar(10) PRIMARY KEY, name VARCHAR(25), mobile varchar(10), email  varchar(30), address varchar(100), gender varchar(10),dob varchar(20), date varchar(50), time varchar(50))"
    cursor = db.cursor()
    try:
        cursor.execute(query)
        db.commit()
        messagebox.showinfo("Success", f"account '{table_name}' created successfully now login.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error creating table: {err}")
    cursor.close()
    return
   


def show_login_frame():
    login_frame.place(x=480,y=400)
    create_account_frame.place_forget()

def show_create_account_frame():
    login_frame.place_forget()
    create_account_frame.place(x=480,y=400)

def login():
    global global_username
    username = login_username_entry.get()
    password = login_password_entry.get()

    cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
    account = cursor.fetchone()

    if account:
        global_username = login_username_entry.get()
        result_label.config(text="Logging in as: " + username)
        root.destroy()
        #import test
    else:
        result_label.config(text="Invalid username or password.")

def create_account():
    new_username = create_username_entry.get()
    new_password = create_password_entry.get()
    confirm_new_password = confirm_password_entry.get()
    
    if new_username=='' or new_password=='':
        messagebox.showerror('Error','Fields cannot be empty')    
    else:
        # Check if the username already exists
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (new_username,))
        existing_account = cursor.fetchone()
        if existing_account:
            messagebox.showerror('Error',"Username already exists.") 
            result_label.config(text="Username already exists.")
            return

    if new_password != confirm_new_password:
        messagebox.showerror('Error',"Passwords do not match.") 
        result_label.config(text="Passwords do not match.")
        return

    cursor.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (new_username, new_password))
    db.commit()
    #var =  create_username_entry.get()
    create_table()  
    #root.destroy()
    #result_label.config(text="Account created for: " + new_username)


# Set up background image
backgroundImage=ImageTk.PhotoImage(file="bg.jpg")
bgLabel=tk.Label(image=backgroundImage)
bgLabel.place(x=0,y=0 )

# Set up logo image
logo_image = PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=logo_image , bg='white')
logo_label.place(x=500,y=90)

# Create login frame
login_frame = tk.Frame(root , bg= 'white')
login_label = tk.Label(login_frame, text="Login")
login_label.place(x=500,y=300)
usernameImage=PhotoImage(file="user.png")
login_username_label = tk.Label(login_frame,image=usernameImage, text="Username:", compound=tk.LEFT,font=('times new roman',20,'bold'),bg='white')
login_username_label.pack()
login_username_entry = tk.Entry(login_frame, font=('times new roman',20,'bold'),bd=5,fg='royalblue')
login_username_entry.pack()

passwordImage=PhotoImage(file="password.png")
login_password_label = tk.Label(login_frame, image=passwordImage, text="Password:",font=('times new roman',20,'bold'),bg='white', compound=tk.LEFT)
login_password_label.pack()
login_password_entry = tk.Entry(login_frame, show="*",  font=('times new roman',20,'bold'),bd=5,fg='royalblue')
login_password_entry.pack()

login_button = tk.Button(login_frame, text="Login", command=login,font=('times new roman',14,'bold'),width=15
                   ,fg='white',bg='cornflowerblue',activebackground='cornflowerblue',
                   activeforeground='white',cursor='hand2')
login_button.pack()

# Create create account frame
create_account_frame = tk.Frame(root, bg= 'white')



create_username_label = tk.Label(create_account_frame, text="Username:", image=usernameImage,font=('times new roman',20,'bold'),bg='white', compound=tk.LEFT)
create_username_label.pack()
create_username_entry = tk.Entry(create_account_frame, font=('times new roman',20,'bold'),bd=5,fg='royalblue')
create_username_entry.pack()


create_password_label = tk.Label(create_account_frame,image=passwordImage, text="Set Password:",font=('times new roman',20,'bold'),bg='white', compound=tk.LEFT)
create_password_label.pack()
create_password_entry = tk.Entry(create_account_frame, show="*", font=('times new roman',20,'bold'),bd=5,fg='royalblue')
create_password_entry.pack()

confirm_password_label = tk.Label(create_account_frame, text="Confirm Password:",font=('times new roman',20,'bold'),bg='white')
confirm_password_label.pack()
confirm_password_entry = tk.Entry(create_account_frame, show="*", font=('times new roman',20,'bold'),bd=5,fg='royalblue')
confirm_password_entry.pack()

create_button = tk.Button(create_account_frame, text="Create Account",font=('times new roman',14,'bold'),width=15
                   ,fg='white',bg='cornflowerblue',activebackground='cornflowerblue',
                   activeforeground='white',cursor='hand2', command=create_account)
create_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

login_button = tk.Button(root, text="Login",font=('times new roman',14,'bold'),width=15
                   ,fg='white',bg='cornflowerblue',activebackground='cornflowerblue',
                   activeforeground='white',cursor='hand2', command=show_login_frame)
login_button.place(x=540,y=290)

create_account_button = tk.Button(root, text="Create Account",font=('times new roman',14,'bold'),width=15
                   ,fg='white',bg='cornflowerblue',activebackground='cornflowerblue',
                   activeforeground='white',cursor='hand2', command=show_create_account_frame)
create_account_button.place(x=540,y=350)

root.mainloop()

# Close the database connection
db.close()

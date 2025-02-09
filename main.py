from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
from tkcalendar import DateEntry 
from PIL import ImageTk
#import pymysql
import pandas
import mysql.connector
from tkinter import PhotoImage
from PIL import Image, ImageTk
from login import global_username


# Now you can use the global_username variable in this file
print("Username from the first file:", global_username)

conn = mysql.connector.connect (
    host ='localhost',
    username = 'root',
    password = '************',
    database = 'studentmanagementsystem'
    )
mycursor=conn.cursor()

#functionality Part
def view_details(event):
    item = studentTable.identify("item", event.x, event.y)
    if item:
         student_id = studentTable.item(item, "values")[0]
        
         view_student_details(student_id)



def view_student_details(student_id):
    student_info_screen = Toplevel(root)
    student_info_screen.title("Student Details")
    student_info_screen.geometry("400x350")

    query = f"SELECT * FROM {global_username} WHERE id = %s"
    values = (student_id,)
    mycursor.execute(query, values)
    student_data = mycursor.fetchone()

    if student_data:
        image_path = f"studentimg/{student_data[1]}.jpeg"  # Replace with actual image path
        try:
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            image_label = Label(student_info_screen, image=photo)
            image_label.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected
            image_label.pack()
        except Exception as e:
            print("Error loading image:", e)
        Label(student_info_screen, text=f"Student ID: {student_data[0]}").pack()
        Label(student_info_screen, text=f"Name: {student_data[1]}").pack()
        Label(student_info_screen, text=f"Mobile: {student_data[2]}").pack()
        Label(student_info_screen, text=f"Email: {student_data[3]}").pack()
        Label(student_info_screen, text=f"Address: {student_data[4]}").pack()
        Label(student_info_screen, text=f"Gender: {student_data[5]}").pack()
        Label(student_info_screen, text=f"Date of Birth: {student_data[6]}").pack()

        # Load the student's image and display it
        
    else:
        Label(student_info_screen, text="Student data not found.").pack()


def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass


def toplevel_data(title,button_text,command):
    global idEntry,phoneEntry,nameEntry,emailEntry,addressEntry,genderEntry,dob_var,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)
    

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    gender_var = StringVar()
    gender_choices = ['Male', 'Female', 'Other']
    genderEntry = ttk.Combobox(screen, textvariable=gender_var, values=gender_choices)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dob_var = StringVar()
    dob_cal = DateEntry(screen, textvariable=dob_var, date_pattern="yyyy-mm-dd", locale="en_US")
    dob_cal.grid(row=6, column=1, pady=15, padx=30)
    
    #dob_var = Entry(screen, font=('roman', 15, 'bold'), width=24)
    #dob_var.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)
    if title=='Update Student':
        indexing = studentTable.focus()

        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dob_var.insert(0, listdata[6])


def update_data(): 
    query = f'update {global_username} set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s'
    values = (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
              genderEntry.get(), dob_var.get(), date, currenttime, idEntry.get())
    mycursor.execute(query, values)
    conn.commit()
    messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_student()



def show_student():
    query = f"select * from {global_username}"
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)



def delete_student():
    indexing=studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id=content['values'][0]
    query=f'delete from {global_username} where id=%s'
    values = (content_id,)
    mycursor.execute(query,values)
    conn.commit()
    messagebox.showinfo('Deleted',f'Id {content_id} is deleted succesfully')
    query=f'select * from {global_username}'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)




def search_data():
    query=f'select * from {global_username} where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    values = (idEntry.get(),nameEntry.get(),emailEntry.get(),phoneEntry.get(),addressEntry.get(),genderEntry.get(),dob_var.get())
    mycursor.execute(query, values)
    studentTable.delete(*studentTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('',END,values=data)




def add_data():
    if idEntry.get()=='' or nameEntry.get()=='' or phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderEntry.get()=='' or dob_var.get()=='':
        messagebox.showerror('Error','All Feilds are required',parent=screen)

    else:
        #try:
        query= f'insert into {global_username} values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values =(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),
                                genderEntry.get(),dob_var.get(),date,currenttime)
        mycursor.execute(query,values)
        conn.commit()
        result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?',parent=screen)
        if result:
            idEntry.delete(0,END)
            nameEntry.delete(0,END)
            phoneEntry.delete(0,END)
            emailEntry.delete(0,END)
            addressEntry.delete(0,END)
            genderEntry.delete(0,END)
            #dob_var.delete(0,END)
        else:
            pass
        #except:
           # messagebox.showerror('Error','Id cannot be repeated',parent=screen)
           # return


        query=f'select *from {global_username}'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('',END,values=data)


count=0
text=' '
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)




def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)



#GUI Part
root=ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('radiance')

root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('Student Management System')

datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()
s='Student Management System' #s[count]=t when count is 1
sliderLabel=Label(root,font=('arial',28,'italic bold'),width=30)
sliderLabel.place(x=200,y=0)
slider()



leftFrame=Frame(root)
leftFrame.place(x=920,y=-10,width=300,height=800)

logo_image=PhotoImage(file='logo.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)

addstudentButton=ttk.Button(leftFrame,text='Add Student',width=25,command=lambda :toplevel_data('Add Student','Add',add_data))
addstudentButton.grid(row=1,column=0,pady=20)

searchstudentButton=ttk.Button(leftFrame,text='Search Student',width=25,command=lambda :toplevel_data('Search Student','Search',search_data))
searchstudentButton.grid(row=2,column=0,pady=20)

deletestudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,command=delete_student)
deletestudentButton.grid(row=3,column=0,pady=20)

updatestudentButton=ttk.Button(leftFrame,text='Update Student',width=25,command=lambda :toplevel_data('Update Student','Update',update_data))
updatestudentButton.grid(row=4,column=0,pady=20)

showstudentButton=ttk.Button(leftFrame,text='Show Student',width=25,command=show_student)
showstudentButton.grid(row=5,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=6,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=10,y=100,width=920,height=550)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)



studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile','Email','Address','Gender',
                                 'D.O.B','Added Date','Added Time','View Details'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)



scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(expand=1,fill=BOTH)

studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile',text='Mobile No')
studentTable.heading('Email',text='Email Address')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')
studentTable.heading('Added Date',text='Added Date')
studentTable.heading('Added Time',text='Added Time')
studentTable.heading('View Details',text='View Details')


studentTable.column('Id',width=50,anchor=CENTER)
studentTable.column('Name',width=200,anchor=CENTER)
studentTable.column('Email',width=300,anchor=CENTER)
studentTable.column('Mobile',width=200,anchor=CENTER)
studentTable.column('Address',width=300,anchor=CENTER)
studentTable.column('Gender',width=100,anchor=CENTER)
studentTable.column('D.O.B',width=200,anchor=CENTER)
studentTable.column('Added Date',width=200,anchor=CENTER)
studentTable.column('Added Time',width=200,anchor=CENTER)
studentTable.column('View Details',width=200,anchor=CENTER)
studentTable.bind("<Button-1>", view_details)
style=ttk.Style()

#style.configure('Treeview', rowheight=40,font=('arial', 12, 'bold'), fieldbackground='white', background='white',)
#style.configure('Treeview.Heading',font=('arial', 14, 'bold'),foreground='red')
# Update the style to change the text color of the button and Treeview
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')
style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), fieldbackground='white', background='white', foreground='black')


studentTable.config(show='headings')

root.mainloop()

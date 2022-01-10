import pymongo
from tkinter import *
from tkinter import messagebox

root=Tk()
root.geometry('350x470')
root['background']="#68eddb"
root.title("Student Record")
root.iconbitmap('image/favicon.ico')
# =================Creating Databases Connection================
client=pymongo.MongoClient('mongodb+srv://student_manage:vishal@cluster0.foa5b.mongodb.net/student?retryWrites=true&w=majority')
db=client['student']
collections=db['cse']

# =================Creating Button and lable for Show,update,delete,search student record===========
main_frame=LabelFrame(root,text="Main frame",bd=2,pady=10,padx=5,bg='#68eddb')
main_frame.grid(row=1,column=0,sticky=E+W,padx=30,pady=10)
# ==========Displaying Student record in a new window==========
def student_record():
    std_record=Toplevel()
    # std_record.geometry('300x300')
    std_record.configure(bg="#68eddb")
    std_record['bg']='#8c94ed'
    std_record.title('Student Record')
    std_record.iconbitmap('image/favicon.ico')
    header_frame=LabelFrame(std_record,padx=10,pady=5,bg='#f7d04d')
    header_frame.grid(row=0,column=0,sticky=W+E)
    header_name=Label(header_frame,text="STUDENT RECORD",font=("italic",20,"bold"),border=5,padx=10,pady=10,bg="grey",fg="#faf8dc")
    header_name.grid(row=0,column=0,padx=2,pady=20)

    data_frame=LabelFrame(std_record,padx=10,pady=10,bg='#8c94ed')
    data_frame.grid(row=1,column=0,sticky=W+E,padx=10,pady=10)


    dictionary = collections.find()
    row,column=1,0
    for i in dictionary:
        # print(i)
        detail=f'''Id : {i['_id']} \nName : {i['name']}\nRoll No : {i['roll']}\nFee : {i['fee']}\n Mark : {i['mark']}'''
        if row>4:
            row =1
            column +=1
        show_lable=Label(data_frame,text=detail,borderwidth=4,bg='grey',width=20,fg='#fff',font=("MS Sans Serif",13,'normal'))
        show_lable.grid(row=row,column=column,padx=10,pady=10)
        row +=1

show_button=Button(main_frame,text="SHOW STUDENT RECORD",command=student_record,padx=10,pady=5)
show_button.grid(row=0,column=0,sticky=E+W,columnspan=2,padx=10)

lable_name=Label(main_frame,text="Enter Name/Roll/Id ").grid(row=1,column=0)

input_lable=Entry(main_frame,font=('arial',10,'normal'))
input_lable.grid(row=1,column=1,sticky=E+W,padx=10,pady=10,ipady=5)

# =======================Searching student===============]
searched_f = LabelFrame(root, bd=1, pady=10, padx=5, bg='#68eddb')
searched_f.grid(row=2, column=0, sticky=E + W,padx=30,pady=10)
show_lable = Label(searched_f, text="No Records !!", borderwidth=4, bg='grey', width=20, fg='#eb042d',
                               font=("MS Sans Serif", 13, 'normal'),padx=5,pady=5)
show_lable.grid(row=0, column=0, padx=30, pady=10)
def search():

    check=0
    item_id=input_lable.get()

    try:
        item_id = int(item_id)
        status = collections.find_one({"$or": [{"_id": item_id}, {"roll": item_id}]})
        check = collections.count_documents({"$or": [{"_id": item_id}, {"roll": item_id}]})
    except Exception:
        item_id=item_id.upper()
        status = collections.find_one({"name": item_id})
        check = collections.count_documents({"name": item_id})

    finally:
        if check:
            i = status
            detail = f'''Id : {i['_id']} \nName : {i['name']}\nRoll No : {i['roll']}\nFee : {i['fee']}\n Mark : {i['mark']}'''

            show_lable.configure(text=detail,fg='#f1f394')
            return status
        else:
            show_lable.configure(text="Sorry No Record Found !!",fg='#eb042d')
            return check





search_button=Button(main_frame,text="SEARCH STUDENT",command=search,padx=10,pady=5)
search_button.grid(row=2,column=0,sticky=E+W,columnspan=2,padx=10)

# ================================= Updating student record================

def update():
    update_window=Toplevel()
    status=search()
    if status==0:
        update_window.destroy()
    update_window.configure(bg="#68eddb")
    update_window['bg'] = '#8c94ed'
    update_window.title('Update Student Record')
    update_window.iconbitmap('image/favicon.ico')


    data_frame = LabelFrame(update_window, padx=10, pady=10, bg='#8c94ed')
    data_frame.grid(row=1, column=0, sticky=W + E, padx=10, pady=10)

    update_name = Label(data_frame, text="Name", padx=10, pady=5)
    update_name.grid(row=0, column=0, sticky=E + W, columnspan=2, pady=10, padx=10)
    update_roll = Label(data_frame, text="Roll", padx=10, pady=5)
    update_roll.grid(row=1, column=0, sticky=E + W, columnspan=2, pady=10, padx=10)
    update_fee = Label(data_frame, text="Fee", padx=10, pady=5)
    update_fee.grid(row=2, column=0, sticky=E + W, columnspan=2, pady=10, padx=10)
    update_mark = Label(data_frame, text="Marks", padx=10, pady=5)
    update_mark.grid(row=3, column=0, sticky=E + W, columnspan=2, pady=10, padx=10)
    name=StringVar()
    name.set(status['name'])
    input_lable = Entry(data_frame,text=name, font=('arial', 10, 'normal'))
    input_lable.grid(row=0, column=2, sticky=E + W, padx=10, pady=10, ipady=5)
    roll=IntVar()
    roll.set(status['roll'])
    input_lable = Entry(data_frame,text=roll, font=('arial', 10, 'normal'))
    input_lable.grid(row=1, column=2, sticky=E + W, padx=10, pady=10, ipady=5)
    fee=StringVar()
    ls=['FULLY PAID','PENDING']
    fee.set(status['fee'])
    input_lable=OptionMenu(data_frame,fee,*ls)
    input_lable.grid(row=2, column=2, sticky=E + W, padx=10, pady=10, ipady=5)
    mark=StringVar()
    mark.set(status['mark'])
    input_lable = Entry(data_frame,text=mark, font=('arial', 10, 'normal'))
    input_lable.grid(row=3, column=2, sticky=E + W, padx=10, pady=10, ipady=5)

    def insert_new():
        try:
            collections.update_one({"_id":status['_id']},{'$set':{"name":name.get(),'roll':roll.get(),'fee':fee.get(),'mark':mark.get()}})
            print("Successfully completed")
            messagebox.showinfo('Status',"Successfully Updated")
            update_window.destroy()
            search()
        except TclError as e:
            messagebox.showwarning('Status',"Please enter valid Roll Number")


    submit_button = Button(data_frame, text="UPDATE", command=insert_new, padx=10, pady=5)
    submit_button.grid(row=4, column=0, sticky=E + W, columnspan=3, padx=10)
    submit_button.focus()
    cancel_button = Button(data_frame, text="CANCEL", command=update_window.destroy, padx=10, pady=5,fg="red")
    cancel_button.grid(row=5, column=0, sticky=E + W, columnspan=3, padx=10,pady=10)

update_button=Button(main_frame,text="UPDATE STUDENT",command=update,padx=10,pady=5)
update_button.grid(row=3,column=0,sticky=E+W,columnspan=2,pady=10,padx=10)

def delete():
    status=search()
    if status==0:
        messagebox.showwarning("Warning","Please enter Id/Name/Roll to delete only one student record")
    else:
        message=f"""       Name : {status['name']}
        Roll No: {status['roll']}
        Fee: {status['fee']}
        Mark: {status['mark']}"""
        delete_option=messagebox.askokcancel("Deletion warning",message)
        if delete_option:
            collections.delete_one({'_id':status['_id']})
            messagebox.showinfo("Status",status['name']+" is delete successfully")
            search()


delete_button=Button(main_frame,text="DELETE STUDENT",command=delete,padx=10,pady=5)
delete_button.grid(row=4,column=0,sticky=E+W,columnspan=2,pady=10,padx=10)



# client.close()
root.mainloop()

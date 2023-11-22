import ttkbootstrap as ttk
import tkinter as tk
from tkinter import PhotoImage
from ttkbootstrap import Style
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import messagebox
import socket
import json
import re


HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(data):
    message = json.dumps(data).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    response = client.recv(2048).decode(FORMAT)
    return response

#==========================================================================================
def isValidEmail(email):
    if len(email) > 7:
        if re.match(r"^.+@([a-zA-Z0-9-.]+\.[a-zA-Z]{2,3}|[0-9]{1,3})$", email) is not None:
            return True
    return False
SCREEN_WIDTH_REG = 700
SCREEN_HEIGHT_REG = 780

def registration(parent_window):
    
    
    def create_base(first_name, last_name, email, password, confirm_password, selected_month, selected_day, selected_year, gender):

        data = {
        "execution": 1,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "month": selected_month,
        "day": selected_day,
        "year": selected_year,
        "gender": gender}
    
        if isValidEmail(email) and len(email) !=0 and len(first_name) !=0 and len(last_name) !=0 and len(password) >= 8 and len(confirm_password) >= 8 and len(selected_day) !=0 and len(selected_month) !=0 and len(selected_year) !=0 and len(gender) !=0 and confirm_password == password:
            send(data)
            registration_window.destroy()
    
    
    registration_window = tk.Toplevel(parent_window)
    registration_window.title("Registration")

    screen_width = parent_window.winfo_screenwidth()
    screen_height = parent_window.winfo_screenheight()

    x_reg = (screen_width - SCREEN_WIDTH_REG) // 2
    y_reg = (screen_height - SCREEN_HEIGHT_REG) // 2

    registration_window.geometry(f"{SCREEN_WIDTH_REG}x{SCREEN_HEIGHT_REG}+{x_reg}+{y_reg}")
    top_label = ttk.Label(registration_window, text="Registration", font=("Comic Sans MS", 50))
    top_label.pack(side="top", pady=20)
#============================================================================
    first_name_var = tk.StringVar()
    last_name_var = tk.StringVar()
    email_var = tk.StringVar()
    password_var = tk.StringVar()
    confirm_password_var = tk.StringVar()
    month_var = tk.StringVar()
    day_var = tk.StringVar()
    year_var = tk.StringVar()
    gender_var = tk.StringVar()

#======================================================================================================
    first_name_entry = ttk.Entry(registration_window, font=("Arial", 14), textvariable=first_name_var)
    first_name_entry.pack(pady=10)
    first_name_var.set("First Name")
    first_name_entry.bind("<FocusIn>", lambda event, widget=first_name_var: widget.set("") if widget.get() == "First Name" else None)
    first_name_entry.bind("<FocusOut>", lambda event, widget=first_name_var: widget.set("First Name") if widget.get() == "" else None)
#======================================================================================================
    last_name_entry = ttk.Entry(registration_window, font=("Arial", 14), textvariable=last_name_var)
    last_name_var.set("Last Name")
    last_name_entry.pack(pady=10)
    last_name_entry.bind("<FocusIn>", lambda event, widget=last_name_var: widget.set("") if widget.get() == "Last Name" else None)
    last_name_entry.bind("<FocusOut>", lambda event, widget=last_name_var: widget.set("Last Name") if widget.get() == "" else None)
#======================================================================================================
    email_entry = ttk.Entry(registration_window, font=("Arial", 14), textvariable=email_var)
    email_var.set("Email")
    email_entry.pack(pady=10)
    email_entry.bind("<FocusIn>", lambda event, widget=email_var: widget.set("") if widget.get() == "Email" else None)
    email_entry.bind("<FocusOut>", lambda event, widget=email_var: widget.set("Email") if widget.get() == "" else None)
#======================================================================================================
    password_entry = ttk.Entry(registration_window, font=("Arial", 14), textvariable=password_var, show="")
    password_var.set("Password")
    password_entry.pack(pady=10)
    password_entry.bind("<FocusIn>", lambda event, widget=password_var: widget.set("") if widget.get() == "Password" else None)
    password_entry.bind("<FocusOut>", lambda event, widget=password_var: widget.set("Password") if widget.get() == "" else None)
#======================================================================================================
    confirm_password_entry = ttk.Entry(registration_window, font=("Arial", 14), textvariable=confirm_password_var, show="")
    confirm_password_var.set("Confirm Password")
    confirm_password_entry.pack(pady=10)
    confirm_password_entry.bind("<FocusIn>", lambda event, widget=confirm_password_var: widget.set("") if widget.get() == "Confirm Password" else None)
    confirm_password_entry.bind("<FocusOut>", lambda event, widget=confirm_password_var: widget.set("Confirm Password") if widget.get() == "" else None)
#======================================================================================================
    date_frame = ttk.Frame(registration_window)
    date_frame.pack()
#======================================================================================================
    selected_month_label = tk.Label(date_frame, text="Month")
    selected_day_label = tk.Label(date_frame, text="Day")
    selected_year_label = tk.Label(date_frame, text="Year")
    
    selected_month_label.grid(column=0, row=0)
    selected_day_label.grid(column=1, row=0)
    selected_year_label.grid(column=2, row=0)

    month_button = ttk.Menubutton(date_frame, text="Month")
    day_button = ttk.Menubutton(date_frame, text="Day")
    year_button = ttk.Menubutton(date_frame, text="Year")

    month_button.menu = tk.Menu(month_button, tearoff=0)
    day_button.menu = tk.Menu(day_button, tearoff=0)
    year_button.menu = tk.Menu(year_button, tearoff=0)

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    days = [str(i) for i in range(1, 32)]
    years = [str(i) for i in range(1970, 2025)]

    def update_selected_month(value):
        selected_month_label.config(text=value)

    def update_selected_day(value):
        selected_day_label.config(text=value)

    def update_selected_year(value):
        selected_year_label.config(text=value)

    for month in months:
        month_button.menu.add_radiobutton(label=month, variable=month_var, value=month, command=lambda m=month: update_selected_month(m))
    for day in days:
        day_button.menu.add_radiobutton(label=day, variable=day_var, value=day, command=lambda d=day: update_selected_day(d))
    for year in years:
        year_button.menu.add_radiobutton(label=year, variable=year_var, value=year, command=lambda y=year: update_selected_year(y))

    month_var.set("Month")
    day_var.set("Day")
    year_var.set("Year")

    month_button["menu"] = month_button.menu
    day_button["menu"] = day_button.menu
    year_button["menu"] = year_button.menu

    month_button.grid(column=0, row=1, pady=10)
    day_button.grid(column=1, row=1, pady=10)
    year_button.grid(column=2, row=1, pady=10)
#======================================================================================================
    gender_frame = ttk.Frame(registration_window)
    gender_frame.pack()

    male_radio = ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male")
    female_radio = ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female")
    custom_radio = ttk.Radiobutton(gender_frame, text="Custom", variable=gender_var, value="Custom")

    male_radio.grid(row=0, column=0, pady=10, padx=10)
    female_radio.grid(row=0, column=1, pady=10, padx=10)
    custom_radio.grid(row=0, column=2, pady=10, padx=10)
#======================================================================================================
    
 
       
    
    style = Style(theme="solar")
    style.configure('TButton', font=('Comic Sans MS', 20))
    
    reg_button = ttk.Button(registration_window, text="Sign up", command=lambda: create_base(first_name_var.get(), last_name_var.get(), email_var.get(), password_var.get(), confirm_password_var.get(), month_var.get(), day_var.get(), year_var.get(), gender_var.get()))
    reg_button.pack(pady=20)
    registration_window.mainloop()
    
    
#======================================================================================================

def on_entry_focus_in(event):
    print("Entry widget focused in")
    if login_entry.get() == "Email or Phone":
        login_entry.delete(0, "end")
        login_entry.config(foreground="black")

def on_entry_focus_out(event):
    print("Entry widget focused out")
    if not login_entry.get():
        login_entry.insert(0, "Email or Phone")
        login_entry.config(foreground="gray")

def on_password_focus_in(event):
    if password_entry.get() == "Password":
        password_entry.delete(0, "end")
        password_entry.config(show="*", foreground="black")

def on_password_focus_out(event):
    if not password_entry.get():
        password_entry.config(show="", foreground="gray")
        password_entry.insert(0, "Password")

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 780

window = ttk.Window("Data Entry", "solar", resizable=(False, False))
window.title("Welcome To QuickChat")
window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - SCREEN_WIDTH) // 2
y = (screen_height - SCREEN_HEIGHT) // 2

window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+{x}+{y}")
 

center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

login_frame = ttk.LabelFrame(window, padding=25, width=600, height=400)
login_frame.place(x=center_x - 430, y=center_y - 330)

login_label = ttk.Label(login_frame, text='Log into QuickChat', font=("Comic Sans MS", 36), foreground="#1877F2")
login_label.pack(pady=30)
#========================================================================================================================  
def login(parent, email, password):
    def direct_send(sender_id, receiver_id, messege):
        send_data_0 = {
            "execution":7,
            "sender_id":sender_id,
            "receiver_id":receiver_id,
            "messege":messege
        }
        send(send_data_0)
        
    
    
    def confirm(receiver_me, sender_other):
        print(f"this is receiver {receiver_me}")
        print(f"this is sender {sender_other}")
        
        add_data = {
            "execution":6,
            "receiver_me":receiver_me,
            "sender_other":sender_other
        }
        send(add_data)
  
    def send_friendship(receiver_id, sender_id):
        
        data = {
            "execution": 5,
            "sender_id": sender_id,
            "receiver_id": receiver_id
        }
        send(data)
        
    def search_people(person):
        
        for label in search_box_frame_2.winfo_children():
            label.destroy()

        data = {
            "execution":4,
            "sender":email,
            "person":person
        }
        send(data)
        search_response = client.recv(1024).decode(FORMAT)
        print(search_response) 

        response = json.loads(search_response)
        print(response)
        n = 0

        for data in response:
            full_name = data.get("full_name")
            receiver_id = data.get("receiver_num")
            sender_id = data.get("sender_num")

            is_friend = any(receiver_id == friend["id"] for friend in my_friends)

            label_text = "Friend" if is_friend else full_name

            label = ttk.Label(search_box_frame_2, text=label_text, font=("Arial", 15), anchor="w", justify="left")
            label.grid(row=n, column=0, padx=5, pady=5)

            button_text = "Friend" if is_friend else "Send Friendship"
            button_command = lambda r=receiver_id: send_friendship(r, user_id) if not is_friend else None

            button = ttk.Button(search_box_frame_2, text=button_text, command=button_command, state="disabled" if is_friend else "normal")
            button.grid(row=n, column=1, padx=5, pady=5)
            
            n += 1

                 
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 780

    user_window = ttk.Toplevel(parent, resizable=(False, False))
    
    style = ttk.Style()
    style.theme_use("solar")
    user_window.title("User Window")
    user_window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

    screen_width = user_window.winfo_screenwidth()
    screen_height = user_window.winfo_screenheight()

    x = (screen_width - SCREEN_WIDTH) // 2
    y = (screen_height - SCREEN_HEIGHT) // 2

    user_window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+{x}+{y}")
    name = ttk.StringVar()
    surname = ttk.StringVar()
    email_var = ttk.StringVar()
    gender = ttk.StringVar()
    birthday = ttk.StringVar()
    birthmonth = ttk.StringVar()
    birthyear = ttk.StringVar()
    data = {
        "execution": 2,
        "log": email,
        "password": password
    }
    send(data)
    response = client.recv(1024).decode(FORMAT)
    if response == "User exists":
        def update_info():
            global response_dict, user_data, sender_ids, sender_full_names, my_friends
            data = {
                "execution": 3,
                "email": email
            }
            send(data)
            response = client.recv(10000).decode(FORMAT)
            
            response_dict = json.loads(response)
            user_window.after(500, update_info)
            user_data = response_dict.get('user_data', [])[0]

            sender_ids = [sender.get('sender_id', None) for sender in response_dict.get('sender_id', []) if sender.get('sender_id') is not None]
            
            sender_full_names = [name.get('full_name', '') for name in response_dict.get('sender_full_name', [])]

            my_friends = response_dict.get('my_friends', [])
         
        update_info()
        name.set(user_data.get("first_name", ""))
        surname.set(user_data.get("last_name", "")) 
        gender.set(user_data.get("gender", ""))
        email_var.set(user_data.get("email", ""))
        birthmonth.set(user_data.get("birthmonth", ""))
        birthday.set(user_data.get("birthday", ""))
        birthyear.set(user_data.get("birthyear", ""))

        user_id = user_data.get("id")

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Comic Sans MS", 18, "bold"))

        tab = ttk.Notebook(user_window)
        tab1 = ttk.Frame(tab)
        tab2 = ttk.Frame(tab)
        tab.add(tab1, text="Tab 1")
        tab.add(tab2, text="Tab 2")
        tab.pack(fill="both", expand=True)
        window.iconify()
        
        
        profil_frame = ttk.Frame(tab1, width=1000, height=780)
        profil_frame.place(x=10, y=10)
        
        foreign_people = ttk.Frame(tab1, width=150, height=50)
        foreign_people.place(x=900, y=0)
        
        
        
        title_label = ttk.Label(profil_frame, text="User Profil", font=("Comic Sans MS", 40, "bold"))
        title_label.grid(row=0, column=0, pady=20, columnspan=2)
        
        profil_frame.configure(borderwidth=3, relief="groove")
        
        
        first_name_label = ttk.Label(profil_frame, text="First Name:", font=("Comic Sans MS", 20, "bold"))
        first_name_label.grid(row=1, column=0, padx=20, pady=14, sticky="w")

        last_name_label = ttk.Label(profil_frame, text="Last Name:", font=("Comic Sans MS", 20, "bold"))
        last_name_label.grid(row=2, column=0, padx=20, pady=14, sticky="w")

        gender_label = ttk.Label(profil_frame, text="Gender:", font=("Comic Sans MS", 20, "bold"))
        gender_label.grid(row=3, column=0, padx=20, pady=14, sticky="w")

        birthmonth_label = ttk.Label(profil_frame, text="Birthmonth:", font=("Comic Sans MS", 20, "bold"))
        birthmonth_label.grid(row=4, column=0, padx=20, pady=14, sticky="w")

        birthday_label = ttk.Label(profil_frame, text="birthday:", font=("Comic Sans MS", 20, "bold"))
        birthday_label.grid(row=5, column=0, padx=20, pady=14, sticky="w")

        birthyear_label = ttk.Label(profil_frame, text="birthyear:", font=("Comic Sans MS", 20, "bold"))
        birthyear_label.grid(row=6, column=0, padx=20, pady=14, sticky="w")

        Email_label = ttk.Label(profil_frame, text="Email:", font=("Comic Sans MS", 20, "bold"))
        Email_label.grid(row=7, column=0, padx=20, pady=14, sticky="w")

        user_name = ttk.Label(profil_frame, textvariable=name, font=("Comic Sans MS", 20, "bold"))
        user_name.grid(row=1, column=1, padx=20, pady=14, sticky="w")

        user_surname = ttk.Label(profil_frame, textvariable=surname, font=("Comic Sans MS", 20, "bold"))
        user_surname.grid(row=2, column=1, padx=20, pady=14, sticky="w")

        user_gender = ttk.Label(profil_frame, textvariable=gender, font=("Comic Sans MS", 20, "bold"))
        user_gender.grid(row=3, column=1, padx=20, pady=14, sticky="w")

        user_birthmonth = ttk.Label(profil_frame, textvariable=birthmonth, font=("Comic Sans MS", 20, "bold"))
        user_birthmonth.grid(row=4, column=1, padx=20, pady=14, sticky="w")

        user_birthday = ttk.Label(profil_frame, textvariable=birthday, font=("Comic Sans MS", 20, "bold"))
        user_birthday.grid(row=5, column=1, padx=20, pady=14, sticky="w")

        user_birthyear = ttk.Label(profil_frame, textvariable=birthyear, font=("Comic Sans MS", 20, "bold"))
        user_birthyear.grid(row=6, column=1, padx=20, pady=14, sticky="w")

        user_email = ttk.Label(profil_frame, textvariable=email_var, font=("Comic Sans MS", 20, "bold"))
        user_email.grid(row=7, column=1, padx=20, pady=14, sticky="w")
        
        search_entry_2 = tk.Entry(foreign_people, width=26, background='#586e75', foreground='white', font=("Comic Sans MS", 14, "bold"))
        search_entry_2.grid(row=0, column=0, padx=10, pady=14, sticky='w')

        search_button_2 = tk.Button(foreign_people, text="Search", background='#586e75', foreground='white', font=('Comic Sans MS', 12), command = lambda: search_people(search_entry_2.get()))
        search_button_2.grid(row=0, column=1, padx=5, pady=14, sticky='w')
        
        search_label_2 = ttk.Label(tab1, text= "Searched Friends", font=('Comic Sans MS', 16), width=380)
        search_label_2.place(x=950, y=60)
        search_box_frame_2 = ScrolledFrame(tab1, width=430, height=280)
        search_box_frame_2.place(x=950, y=100)
        search_box_frame_2.configure(borderwidth=1, relief="groove")
        req_label = ttk.Label(tab1, text= "Requests", font=('Comic Sans MS', 16), width=380)
        req_label.place(x=1000, y=380)
        search_box_frame_3 = ScrolledFrame(tab1,width=430, height=250)
        search_box_frame_3.place(x=950, y=450)
        search_box_frame_3.configure(borderwidth=1, relief="groove")
        def update_confirm():
            for widget in search_box_frame_3.winfo_children():
                widget.destroy()
            for index, data_1 in enumerate(sender_full_names):
                sender_id = sender_ids[index] 

                full_name = data_1
                label_1 = ttk.Label(search_box_frame_3, text=full_name, font=("Arial", 15), anchor="w", justify="center")
                label_1.grid(row=index, column=0, padx=5, pady=5)

                button_1 = ttk.Button(search_box_frame_3, text="Confirm", command=lambda k=user_id, sender_id=sender_id: confirm(k, sender_id))
                button_1.grid(row=index, column=1, padx=5, pady=5)
            user_window.after(1000, update_confirm)   
        update_confirm()    
#========================================================================================================================   
        style.configure('TFrame', background='#002b36')
        style.configure('TButton', background='#586e75', foreground='white')
        style.configure('TLabel', background='#002b36', foreground='white')

        text_box_frame = ScrolledFrame(tab2, width=990, height=640, autohide=True)
        text_box_frame.place(x=400, y=5)
       
        text_box_frame.configure(borderwidth=1, relief="groove")
        text_box_frame.propagate(False)
                

        send_frame = ttk.Frame(tab2)
        send_frame.place(x=400, y=653)
        
        send_entry = tk.Entry(send_frame, width=48, font=("Arial", 20))
        send_entry.grid(row=1, column=1, padx=10, pady=10)

        other_chats_frame = tk.Frame(tab2, width=400,height=30, bg='#073642')
        other_chats_frame.place(x=0, y=0)


        
        search_box_frame = tk.LabelFrame(tab2, text="Friends", width=380, height=330, font=('Comic Sans MS', 16))
        search_box_frame.place(x=5, y=2)

        
        search_box_frame.propagate(False)
        
        choosen = tk.LabelFrame(tab2, text="Choosen", width=380, height=80, font=('Comic Sans MS', 16))
        choosen.place(x=10, y=630)
        
        send_button = tk.Button(send_frame, text="Send", width=5, height=1, font=("Arial", 17), command = lambda : direct_send(sender_id_1, receiver_id_1, send_entry.get()))
        send_button.grid(row=1, column=2, padx=10, pady=10)
        
        all_messages = response_dict.get("all_messages_i_am_mentioned")
        
                
        def configure(r, sender_id, receiver_id):
           
            if configure.after_id:
                user_window.after_cancel(configure.after_id)

            
            for widget in choosen.winfo_children():
                widget.destroy()
            for widget in text_box_frame.winfo_children():
                widget.destroy()

            global sender_id_1, receiver_id_1, all_messages

            sender_id_1 = sender_id
            receiver_id_1 = receiver_id
            all_messages = response_dict.get("all_messages_i_am_mentioned")

            # Create the choosen label
            choosen_label = ttk.Label(choosen, text=r, font=("Arial", 15))
            choosen_label.pack()

            sent_messages = all_messages.get("sent_messages", [])
            received_messages = all_messages.get("received_messages", [])

            sent_from_me = [msg for msg in sent_messages if msg['sender'] == sender_id_1 and msg['receiver'] == receiver_id_1]
            received_from_sb = [msg for msg in received_messages if msg['receiver'] == sender_id_1 and msg['sender'] == receiver_id_1]

            messages_to_display = sent_from_me + received_from_sb
            messages_to_display.sort(key=lambda x: x['message_date'], reverse=True)
            existing_labels = text_box_frame.winfo_children()

            for i, msg in enumerate(messages_to_display):
                if msg['sender'] == sender_id_1:
                    text = f"{msg['message']}<:You"
                else:
                    text = f"Friend:>{msg['message']}"

                if i < len(existing_labels):
                    existing_labels[i].config(text=text)
                else:
                    label = tk.Label(text_box_frame, text=text, font=('Comic Sans MS', 16),
                                    anchor="e" if msg['sender'] == sender_id_1 else "w",
                                    wraplength=300, width=28 if msg['sender'] == sender_id_1 else 30)
                    label.grid(row=i * 2 if msg['sender'] == sender_id_1 else i * 2 + 1,
                            column=1 if msg['sender'] == sender_id_1 else 0, padx=10, pady=5,
                            sticky="e" if msg['sender'] == sender_id_1 else "w")
            for label in existing_labels[len(messages_to_display):]:
                label.destroy()
            configure.after_id = user_window.after(500, configure, r, sender_id, receiver_id)
        configure.after_id = user_window.after(0, lambda: None)


        def update_friends():
            for widget in search_box_frame.winfo_children():
                widget.destroy()
            for index, friend in enumerate(my_friends):
                full_name_3 = friend.get('full_name', "")
                label_1 = ttk.Label(search_box_frame, text=full_name_3, font=("Arial", 15), anchor="w", justify="left")
                label_1.grid(row=index, column=0, padx=5, pady=5)

                user_id = user_data.get('id', "")
                receiver_id = friend.get("id", "")

                button_3 = ttk.Button(search_box_frame, text="Text", command=lambda r=full_name_3, l=user_id, m=receiver_id: configure(r, l, m))
                button_3.grid(row=index, column=1, padx=5, pady=5)
            user_window.after(1000, update_friends)
        update_friends()
        user_window.mainloop()
    else:
        messagebox.showwarning("Warning", "This account does nor exists")
        

    
login_entry = ttk.Entry(login_frame, font=("Arial", 30), width=30, foreground="gray")
login_entry.insert(0, "Email or Phone")
login_entry.pack(pady=35)
login_entry.pack(side="top", pady=10)

login_entry.bind("<FocusIn>", on_entry_focus_in)
login_entry.bind("<FocusOut>", on_entry_focus_out)

password_entry = ttk.Entry(login_frame, show="", font=("Arial", 30), width=30, foreground="gray")
password_entry.insert(0, "Password")
password_entry.pack(pady=35)
password_entry.pack(side="top", pady=10)

password_entry.bind("<FocusIn>", on_password_focus_in)
password_entry.bind("<FocusOut>", on_password_focus_out)

#==================================================================================


window.style.configure("TButton.TButton", font=("Arial", 24))

login_button = ttk.Button(login_frame, text="Log In", style="TButton.TButton", command=lambda: login(window, login_entry.get(), password_entry.get()))

login_button.pack(pady=15)

create_new_button = tk.Button(login_frame, text="Create New Account", font=("Arial", 24), command=lambda: registration(window))
create_new_button.pack(side="top", pady=20)

window.mainloop()





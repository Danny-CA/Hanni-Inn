import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import re
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
import bcrypt
from datetime import datetime

class Hanni:
    def __init__(self):
        self.root = tk.Tk()
        self.root.state('normal') # Abre en pantalla completa
        self.root.title("sistema de gestión Hanni-Inn")
        self.root.configure(bg="#F0F0FF")
        
        self.create_main_window()
        self.root.mainloop()
        
    # Crear la ventana principal
    def create_main_window(self):
        self.frame = Frame(self.root, width=600, height=500)
        self.frame.pack()
        self.frame.place(anchor='center', relx=0.5, rely=0.5)
        self.img = ImageTk.PhotoImage(Image.open("IMG/patzcuaro.jpg"))
        self.label = Label(self.frame, image=self.img)
        self.label.pack()
        
        i1 = Label(self.root, text="Hanni-Inn", bg="#83838B", fg="white", font=('Dotum', 25))
        i2 = Label(self.root, text="Hanni-Inn", fg="white", bg="#83838B", font=('Dotum', 12))
        i1.pack(fill="x")
        i2.pack(fill="x")
        
        self.frame = Frame(self.root)
        self.frame.pack(side="right", anchor="ne")
        bf = Frame(self.root)
        bf2 = Frame(self.root)
        bf2.pack(side="bottom", anchor="sw")
        bf3 = Frame(self.root)
        bf3.pack(side="bottom", anchor="sw")
        bf.pack(side="bottom")
        bf1 = Frame(self.root)
        bf1.pack(side="bottom", anchor="sw")
        bottomframe = Frame(self.root)
        bottomframe.pack(side="bottom", anchor="se")
        
        i5 = Label(bf, text="2024", bg="white")
        i5.pack(side="left")
        i6 = Button(bottomframe, text="Aviso de privacidad", bg="white")
        i6.pack(side=RIGHT)
        i8 = Button(bottomframe, text="Términos y condiciones", bg="white")
        i8.pack(side=RIGHT)
        i3 = Button(self.frame, text="Registrarse", bg="white", command=self.sign_up)
        i3.pack(side=RIGHT)

        i4 = Button(self.frame, text="Iniciar sesión", bg="white", command=self.login)
        i4.pack(side=RIGHT)
        
    # Crear la página de registro
    def sign_up(self):
        c = Toplevel()
        c.geometry("550x550")
        c.title("Registrarse")
        c.configure(bg="#F0F0FF")

        i45 = Label(c, text="Hanni-Inn", bg="#83838B", fg="white", font=('Dotum', 25))
        i46 = Label(c, text="Hoteles-Resorts-Spas", fg="white", bg="#83838B", font=('Dotum', 12))
        i45.pack(fill="x")
        i46.pack(fill="x")

        # Declaración de valores de entrada
        Firstname = StringVar()
        LastName = StringVar()
        UserId = StringVar()
        phoneNumber = StringVar()
        Email = StringVar()
        createpassword = StringVar()
        confirmpassword = StringVar()

        def validate_name(name):
            return len(name) >= 2

        def check_user_id_exists(user_id):
            conn = sqlite3.connect('Hanni.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Hanni WHERE user_id=?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result is not None

        def validate_email(email):
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            return re.match(pattern, email)

        def validate_phone(phone):
            pattern = r"^\d{10}$"
            return re.match(pattern, phone)

        def validate_password(password):
            pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$"
            return re.match(pattern, password)

        def database():
            Fname = Firstname.get()
            Lname = LastName.get()
            user_id = UserId.get()
            number = phoneNumber.get()
            email = Email.get()
            createpass = createpassword.get()
            confirmpass = confirmpassword.get()

            if not user_id or not email or not createpass or not confirmpass:
                messagebox.showerror('Error', 'Todos los campos son requeridos')
                c.lift()
                return
            if Fname and not validate_name(Fname):
                messagebox.showerror('Error', 'El nombre debe tener al menos 2 caracteres.')
                c.lift()
                return
            if Lname and not validate_name(Lname):
                messagebox.showerror('Error', 'El apellido debe tener al menos 2 caracteres.')
                c.lift()
                return
            if check_user_id_exists(user_id):
                messagebox.showerror('Error', 'El usuario ya existe, por favor elige uno diferente.')
                c.lift()
                return
            if not validate_email(email):
                messagebox.showerror('Error', 'Formato de correo inválido.')
                c.lift()
                return
            if number and not validate_phone(number):
                messagebox.showerror('Error', 'El número de teléfono debe tener 10 dígitos.')
                c.lift()
                return
            if not validate_password(createpass):
                messagebox.showerror('Error', 'La contraseña debe tener entre 8 y 15 caracteres e incluir al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.')
                c.lift()
                return
            if createpass != confirmpass:
                messagebox.showerror('Error', 'Las contraseñas no coinciden.')
                c.lift()
                return
            
            hashed_password = bcrypt.hashpw(createpass.encode('utf-8'), bcrypt.gensalt())

            conn = sqlite3.connect('Hanni.db')
            with conn:
                cursor = conn.cursor()
                # Crear la tabla si no existe
                cursor.execute('''CREATE TABLE IF NOT EXISTS Hanni (
                                    user_id TEXT PRIMARY KEY, 
                                    Firstname TEXT, 
                                    LastName TEXT, 
                                    phoneNumber TEXT, 
                                    Email TEXT, 
                                    createpassword TEXT
                                )''')
                cursor.execute('INSERT INTO Hanni(user_id, Firstname, LastName, phoneNumber, Email, createpassword) values (?, ?, ?, ?, ?, ?)', 
                               (user_id, Fname, Lname, number, email, hashed_password))
            conn.commit()
            messagebox.showinfo('Information', 'Sign-up successfully')
            c.destroy()  # Cierra la ventana de registro solo después de un registro exitoso

        Label(c, text="Nombre(s)").place(x=120, y=100)
        Label(c, text="Apellido(s)").place(x=120, y=150)
        Label(c, text="Usuario*").place(x=120, y=200)
        Label(c, text="Número telefónico").place(x=120, y=250)
        Label(c, text="Correo*").place(x=120, y=300)
        Label(c, text="Contraseña*").place(x=120, y=350)
        Label(c, text="Confirma contraseña*").place(x=120, y=400)

        Entry(c, textvariable=Firstname).place(x=260, y=100)
        Entry(c, textvariable=LastName).place(x=260, y=150)
        Entry(c, textvariable=UserId).place(x=260, y=200)
        Entry(c, textvariable=phoneNumber).place(x=260, y=250)
        Entry(c, textvariable=Email).place(x=260, y=300)
        Entry(c, textvariable=createpassword, show='*').place(x=260, y=350)
        Entry(c, textvariable=confirmpassword, show='*').place(x=260, y=400)
        # Botón de enviar registro
        Button(c, text="Guardar", command=database, font=('Dotum', 10)).place(x=280, y=450)

    # Crear la página de inicio de sesión
    def login(self):
        b = Toplevel()
        b.geometry("330x355")
        b.title("Registrarse")
        b.configure(bg="#F0F0FF")

        i47 = Label(b, text="Hanni-Inn", bg="#83838B", fg="white", font=('Dotum', 25))
        i48 = Label(b, text="Hoteles-Resorts-Spas", fg="white", bg="#83838B", font=('Dotum', 12))
        i47.pack(fill="x")
        i48.pack(fill="x")

        user_id = StringVar()
        password = StringVar()

        L1 = Label(b, text="Usuario").place(x=50, y=80)
        L2 = Label(b, text="Contraseña").place(x=50, y=140)
        e1 = Entry(b, bd=3, textvariable=user_id)
        e1.place(x=120, y=80)
        e2 = Entry(b, bd=3, textvariable=password, show='*')
        e2.place(x=120, y=140)

        def LOGin():
            user = user_id.get()
            passwd = password.get()
            if user == "" or passwd == "":
                messagebox.showinfo('message', "Fill the form")
            else:
                conn = sqlite3.connect('Hanni.db')
                cursor = conn.cursor()
                cursor.execute("SELECT createpassword FROM Hanni WHERE user_id=?", (user,))
                row = cursor.fetchone()
                conn.close()
                if row and bcrypt.checkpw(passwd.encode('utf-8'), row[0]):
                    self.hotel_log(user_id=user)  # Pasar el user_id a la función hotel_log
                    b.destroy()  # Cerrar la ventana de login solo si las credenciales son correctas
                else:
                    messagebox.showerror('error', "Usuario o contraseña no son válidos")

        ce20 = Button(b, text="Entrar", command=LOGin)  # Botón de enviar info para iniciar sesión
        ce20.place(x=150, y=200)

    def hotel_log(self, user_id, previous_window=None):
        if previous_window is not None:
            previous_window.destroy()

        d = Toplevel()
        d.state('normal')
        d.title("Hanni reservations")
        d.configure(bg="#F0F0FF")

        b = Label(d, bg="#F0F0FF", bd=2, relief=RIDGE)
        b.place(relx=0.032, rely=0.1, relheight=0.85, relwidth=0.45)

        a = Label(d, bg="#F0F0FF", bd=2, relief=RIDGE)
        a.place(relx=0.52, rely=0.1, relheight=0.85, relwidth=0.45)
# first room
        i10 = Label(d, text="Michoacán", bg="#83838B", fg="white", font=('Dotum', 25))
        i11 = Label(d, text="Patzcuaro y Zamora", fg="white", bg="#83838B", font=('Dotum', 12))
        i12 = Label(d, text=f"Usuario: {user_id}", bg="#83838B", fg="white", font=('Dotum', 12))
        i10.pack(fill="x")
        i11.pack(fill="x")
        i12.pack(fill="x")

        i30 = Label(d, text="Departamento Patzcuaro", font=('Dotum', 22, 'bold'))
        i30.place(x=380, y=120)

        image = Image.open("IMG/apartamento.jpg")
        test = ImageTk.PhotoImage(image)
        labell = Label(d, image=test)
        labell.image = test
        labell.place(x=70, y=120)

        i31 = Label(d, text="*Apartamento acogedor", font=('Dotum', 10, 'bold'), bg="#F0F0FF")
        i31.place(x=430, y=170)

        i32 = Label(d, text="*Ubicado cerca del centro de la ciudad.", font=('Dotum', 10, 'bold'), bg="#F0F0FF")
        i32.place(x=430, y=210)

        i33 = Label(d, text="*Muy limpio", font=('Dotum', 10, 'bold'), bg="#F0F0FF")
        i33.place(x=430, y=250)

        i34 = Label(d, text="*Gran vista", font=('Dotum', 10, 'bold'), bg="#F0F0FF")
        i34.place(x=430, y=290)

        i35 = Label(d, text="- Wi-Fi", font=('Dotum', 10), bg="#F0F0FF")
        i35.place(x=70, y=380)

        i36 = Label(d, text="- Si necesitas comprar algo, hay tiendas cercanas.", font=('Dotum', 10), bg="#F0F0FF")
        i36.place(x=70, y=410)

        i37 = Label(d, text="- Zona muy tranquila", font=('Dotum', 10), bg="#F0F0FF")
        i37.place(x=70, y=440)

        i38 = Label(d, text="- Atracciones turísticas", font=('Dotum', 10), bg="#F0F0FF")
        i38.place(x=70, y=470)


        image = Image.open("IMG/patz.jpg")
        test = ImageTk.PhotoImage(image)
        labell = Label(d, image=test)
        labell.image = test
        labell.place(x=450, y=380)

# Labelling and packing "Room 2"

        i30=Label(d,text="Departamento ZAMORA",font=('Dotum',22,'bold'))
        i30.place(x=1150,y=120)
    
        image = Image.open("IMG/zamora.jpg")
        test=ImageTk.PhotoImage(image)
        labell=Label(d,image=test)
        labell.image=test
        labell.place(x=820,y=120)

        i31=Label(d,text="*Gran lugar",font=('Dotum',10,'bold'),bg="#F0F0FF")
        i31.place(x=1180,y=170)

        i32=Label(d,text="*Cocina incluida",font=('Dotum',10, 'bold'),bg="#F0F0FF")
        i32.place(x=1180,y=210)

        i33=Label(d,text="*Refrigerador incluido",font=('Dotum',10,'bold'),bg="#F0F0FF")
        i33.place(x=1180,y=250)

        i34=Label(d,text="*Zona tranquila",font=('Dotum', 10, 'bold'),bg="#F0F0FF")
        i34.place(x=1180,y=290)

        i35=Label(d,text="- WIFI",font=('Dotum',10),bg="#F0F0FF")
        i35.place(x=820,y=380)

        i36=Label(d,text="- Gran espacio",font=('Dotum',10),bg="#F0F0FF")
        i36.place(x=820,y=410)

        i37=Label(d,text="- genial para descansar",font=('Dotum',10),bg="#F0F0FF")
        i37.place(x=820,y=440)

        i38=Label(d,text="- Ubicado en un gran lugar",font=('Dotum',10),bg="#F0F0FF")
        i38.place(x=820,y=470)       

        image = Image.open("IMG/zamo.jpg")
        test=ImageTk.PhotoImage(image)
        labell=Label(d,image=test)
        labell.image=test
        labell.place(x=1100,y=380)


        def hotel_log_A():
            f = Toplevel()
            f.state('normal')
            f.title("Hanni Reservations")
            f.configure(bg="#F0F0FF")
# Label Widget
            b = Label(f, bg="#F0F0FF", bd=2, relief=RIDGE)
            b.place(relx=0.032, rely=0.1, relheight=0.85, relwidth=0.45)
# Label Widget
            a = Label(f, bg="#F0F0FF", bd=2, relief=RIDGE)
            a.place(relx=0.52, rely=0.1, relheight=0.85, relwidth=0.45)
# Labelling and packing Room 1
            i101 = Label(f, text="Guerrero", bg="#83838B", fg="white", font=('Dotum', 25))
            i111 = Label(f, text="Playas", fg="white", bg="#83838B", font=('Dotum', 12))
            i101.pack(fill="x")
            i111.pack(fill="x")

            i301 = Label(f, text="Departamento Ixtapa", font=('Dotum', 22, 'bold'))
            i301.place(x=430, y=120)

            image = Image.open("IMG/ixtapa.jpg")
            test = ImageTk.PhotoImage(image)
            labell1 = Label(f, image=test)
            labell1.image = test
            labell1.place(x=70, y=120)

            i311 = Label(f, text="*lugar fresco", font=('Dotum', 10, 'bold'), bg="#F0F0FF")
            i311.place(x=430, y=170)

            i321=Label(f,text="*Cerca de la playa",font=('Dotum', 10, 'bold'),bg="#F0F0FF")
            i321.place(x=430,y=210)

            i331=Label(f,text="*Ventilator inside",font=('Dotum', 10,'bold'),bg="#F0F0FF")
            i331.place(x=430,y=250)

            i341=Label(f,text="*Lugar seguro",font=('Dotum', 10, 'bold'),bg="#F0F0FF")
            i341.place(x=430,y=290)

            i351=Label(f,text="- FREE WIFI",font=('Dotum',10),bg="#F0F0FF")
            i351.place(x=70,y=380)

            i361=Label(f,text="- Ideal para tus vacaciones",font=('Dotum',10),bg="#F0F0FF")
            i361.place(x=70,y=410)

            i371=Label(f,text="- Espacioso",font=('Dotum',10),bg="#F0F0FF")
            i371.place(x=70,y=440)

            i381 = Label(f, text="- Pruebalo!", font=('Dotum', 10), bg="#F0F0FF")
            i381.place(x=70, y=470)

            image = Image.open("IMG/ixta.jpg")
            test = ImageTk.PhotoImage(image)
            labell1 = Label(f, image=test)
            labell1.image = test
            labell1.place(x=450, y=380)

# Labelling and packing "Room 2"

            i301=Label(f,text="Departamento Acapulco",font=('Dotum',22,'bold'))
            i301.place(x=1150,y=120)
    
            image = Image.open("IMG/acapulco.jpg")
            test=ImageTk.PhotoImage(image)
            labell1=Label(f,image=test)
            labell1.image=test
            labell1.place(x=820,y=120)

            i311=Label(f,text="*Gran lugar",font=('Dotum',10,'bold'),bg="#F0F0FF")
            i311.place(x=1180,y=170)

            i321=Label(f,text="*Cocina y refrigerador incluidos",font=('Dotum', 10, 'bold'),bg="#F0F0FF")
            i321.place(x=1180,y=210)

            i331=Label(f,text="*Aire acondicionado incluido",font=('Dotum',10,'bold'),bg="#F0F0FF")
            i331.place(x=1180,y=250)
    
            i341=Label(f,text="*Zona turística",font=('Dotum', 10, 'bold'),bg="#F0F0FF")
            i341.place(x=1180,y=290)

            i351=Label(f,text="- WIFI",font=('Dotum',10),bg="#F0F0FF")
            i351.place(x=820,y=450)

            i361=Label(f,text="- Pedimos gente responsable",font=('Dotum',10),bg="#F0F0FF")
            i361.place(x=820,y=490)

            i371=Label(f,text="- No hay música alta a altas horas de la noche.",font=('Dotum',10),bg="#F0F0FF")
            i371.place(x=820,y=530)

            image = Image.open("IMG/aca.jpg")
            test=ImageTk.PhotoImage(image)
            label1l=Label(f,image=test)
            label1l.image=test
            label1l.place(x=1180,y=380)

            ce30 = Button(f, text="Reserva ya!", command=book, font=('Dotum', 14, 'bold'))
            ce30.place(x=520, y=670)

# Reserva ya button for Room 2
            ce30 = Button(f, text="Reserva ya!", command=book, font=('Dotum', 14, 'bold'))
            ce30.place(x=1280, y=700)

            ce600 = Button(f, text="<<", command=lambda: self.hotel_log(f), font=('Dotum', 10))
            ce600.pack(side="left")

        def book():
            e = Toplevel()
            e.state('normal')
            e.title("Reservas")
            e.configure(bg="#F0F0FF")
            
            # Labelling and packing
            i51 = Label(e, text="Hanni", bg="#83838B", fg="white", font=('Dotum', 25))
            i52 = Label(e, text="Reservas", fg="white", bg="#83838B", font=('Dotum', 12))
            i51.pack(fill="x")
            i52.pack(fill="x")

            i39 = Label(e, text="Detalles", font=('Dotum', 22))
            i39.place(x=650, y=120)

            ADULTS = StringVar()
            ROOMS = StringVar()
            CHECK_IN = StringVar()
            CHECK_OUT = StringVar()

            #def database(nights, adults, rooms, check_in_date, check_out_date):
                #if not (nights and adults and rooms and check_in_date and check_out_date):
                    #messagebox.showerror('Error', 'Todos los campos son requeridos')
                    #return
                #try:
                    #conn = sqlite3.connect("SELF.db")
                    #with conn:
                        #cursor = conn.cursor()
                        #cursor.execute('''CREATE TABLE IF NOT EXISTS company (
                            #NIGHTS INTEGER,
                            #ADULTS TEXT,
                            #ROOMS TEXT,
                            #CHECK_IN TEXT,
                            #CHECK_OUT TEXT)''')
                        #cursor.execute('''INSERT INTO company (NIGHTS, ADULTS, ROOMS, CHECK_IN, CHECK_OUT)
                            #VALUES (?, ?, ?, ?, ?)''', (nights, adults, rooms, check_in_date, check_out_date))
                    #conn.commit()
                    #messagebox.showinfo('Information', 'BOOKED SUCCESSFULLY')
                #except sqlite3.Error as error:
                    #messagebox.showerror('Database Error', f"An error occurred: {error}")
                #finally:
                    #if conn:
                        #conn.close()

            def database(nights, adults, rooms, check_in_date, check_out_date):
                if not (nights and adults and rooms and check_in_date and check_out_date):
                    messagebox.showerror('Error', 'Todos los campos son requeridos')
                    return

                try:
                    conn = sqlite3.connect("SELF.db")
                    with conn:
                        cursor = conn.cursor()
                        # Verificar si hay traslapes con reservas existentes en la misma habitación
                        cursor.execute('''SELECT * FROM company WHERE 
                                        ((CHECK_IN BETWEEN ? AND ?) OR 
                                        (CHECK_OUT BETWEEN ? AND ?)) AND 
                                        ROOMS = ?''', (check_in_date, check_out_date, check_in_date, check_out_date, rooms))
                        overlapping_reservations = cursor.fetchall()
                        if overlapping_reservations:
                            messagebox.showerror('Error', 'Las fechas seleccionadas se superponen con reservas existentes en la misma habitación.')
                            return

                        # Insertar la reserva en la base de datos si no hay traslapes
                        cursor.execute('''CREATE TABLE IF NOT EXISTS company (
                            NIGHTS INTEGER,
                            ADULTS TEXT,
                            ROOMS TEXT,
                            CHECK_IN TEXT,
                            CHECK_OUT TEXT)''')
                        cursor.execute('''INSERT INTO company (NIGHTS, ADULTS, ROOMS, CHECK_IN, CHECK_OUT)
                            VALUES (?, ?, ?, ?, ?)''', (nights, adults, rooms, check_in_date, check_out_date))
                    conn.commit()
                    messagebox.showinfo('Información','Reservación guardada con éxito')
                except sqlite3.Error as error:
                    messagebox.showerror('Database Error', f"Ocurrió un error: {error}")
                finally:
                    if conn:
                        conn.close()

            L51 = Label(e, text="Noches").place(x=620, y=200)
            L52 = Label(e, text="Guespedes").place(x=620, y=250)
            guest_options = ["1", "2", "3", "4"]
            Label(e, text="Departamento").place(x=620, y=300)
            room_options = ["Pátzcuaro", "Zamora", "Ixtapa", "Acapulco"]

            nights_var = StringVar()
            e51 = Entry(e, bd=3, textvariable=nights_var, state='readonly')
            e51.place(x=720, y=200)

            e52 = OptionMenu(e, ADULTS, *guest_options)
            e52.place(x=720, y=250)

            e53 = OptionMenu(e, ROOMS, *room_options)
            e53.place(x=720, y=300)

            def get_selected_date():
                selected_date = cal.get_date()
                date_var.set(selected_date)

            # Calendar Widget
            cal = Calendar(e, selectmode="day", year=2024, month=5, day=3)
            cal.place(x=300, y=200)

            select_date_button = Button(e, text="Selecciona fecha", command=get_selected_date)
            select_date_button.place(x=390, y=450)

            date_var = StringVar()
            selected_date_label = Label(e, textvariable=date_var)
            selected_date_label.place(x=410, y=400)

            def update_checkin_date():
                checkin_entry.delete(0, tk.END)
                checkin_entry.insert(0, date_var.get())
                CHECK_IN.set(date_var.get())
                calculate_nights()

            def update_checkout_date():
                checkout_entry.delete(0, tk.END)
                checkout_entry.insert(0, date_var.get())
                CHECK_OUT.set(date_var.get())
                calculate_nights()

            def calculate_nights():
                check_in_date = CHECK_IN.get()
                check_out_date = CHECK_OUT.get()
                if check_in_date and check_out_date:
                    try:
                        check_in_dt = datetime.strptime(check_in_date, "%d/%m/%y")
                        check_out_dt = datetime.strptime(check_out_date, "%d/%m/%y")
                        nights = (check_out_dt - check_in_dt).days
                        if nights > 0:
                            nights_var.set(nights)
                        else:
                            nights_var.set('')
                            messagebox.showerror('Error', 'La fecha de salida debe ser posterior a la fecha de entrada.')
                    except ValueError:
                        messagebox.showerror('Error', 'Formato de fecha no válido.')

            # Check-In Date
            Label(e, text="Llegada:").place(x=620, y=350)
            checkin_entry = Entry(e)
            checkin_entry.place(x=720, y=350)
            Button(e, text="Confirmar fecha de llegada", command=update_checkin_date).place(x=720, y=390)

            # Check-Out Date
            Label(e, text="Salida:").place(x=620, y=440)
            checkout_entry = Entry(e)
            checkout_entry.place(x=720, y=440)
            Button(e, text="Confirmar fecha de salida", command=update_checkout_date).place(x=720, y=480)

            # Confirm Booking Button
            def confirm_booking():
                try:
                    nights = int(nights_var.get())
                except ValueError:
                    messagebox.showerror('Error', 'Seleccione fechas válidas de entrada y salida.')
                    return
                database(nights, ADULTS.get(), ROOMS.get(), CHECK_IN.get(), CHECK_OUT.get())

               # Confirm Booking Button
            
            insert_button = Button(e, text="CONFIRMAR", command=lambda: database(int(nights_var.get()), ADULTS.get(), ROOMS.get(), CHECK_IN.get(), CHECK_OUT.get()), font=('Dotum', 14, 'bold'))
            insert_button.place(x=700, y=600)

        ce30 = Button(d, text="Reserva ya!", command=book, font=('Dotum', 14, 'bold'))
        ce30.place(x=500, y=610)

# Reserva ya button for Room 2
        ce30 = Button(d, text="Reserva ya!", command=book, font=('Dotum', 14, 'bold'))
        ce30.place(x=1180, y=650)

        ce60 = Button(d, text=">>",command=hotel_log_A,font=('Dotum', 10))
        ce60.pack(side="right")

if __name__ == "__main__":
    app = Hanni()

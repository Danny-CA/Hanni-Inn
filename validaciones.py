def sign_up(self):
        c = Toplevel()
        c.geometry("550x550")
        c.title("SIGN UP")
        c.configure(bg="#F0F0FF")
        
        i45 = Label(c, text="Hanni-Inn", bg="#83838B", fg="white", font=('Dotum', 25))
        i46 = Label(c, text="Hotels-Resorts-Spas", fg="white", bg="#83838B", font=('Dotum', 12))
        i45.pack(fill="x")
        i46.pack(fill="x")

        # Declaration of input values
        Firstname = StringVar()
        LastName = StringVar()
        phoneNumber = StringVar()
        Email = StringVar()
        createpassword = StringVar()
        confirmpassword = StringVar()

        def validate_name(name):
            return len(name) >= 2

        def validate_email(email):
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            return re.match(pattern, email)

        def validate_phone(phone):
            pattern = r"^\d{10}$"
            return re.match(pattern, phone)
        
        def validate_password(password):
            pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$"
            return re.match(pattern, password)
        
            # Minimo 8 caracteres
            # Maximo 15
            # Al menos una letra mayúscula
            # Al menos una letra minucula
            # Al menos un dígito
            # No espacios en blanco
            # Al menos 1 caracter especial

        def database():
            Fname = Firstname.get()
            Lname = LastName.get()
            number = phoneNumber.get()
            email = Email.get()
            createpass = createpassword.get()
            confirmpass = confirmpassword.get()
            
            if not Fname or not Lname or not number or not email or not createpass or not confirmpass:
                messagebox.showerror('Error', 'All fields are required.')
                c.lift()
                return
            if not validate_name(Fname):
                messagebox.showerror('Error', 'First name must be at least 2 characters long.')
                return
            if not validate_name(Lname):
                messagebox.showerror('Error', 'Last name must be at least 2 characters long.')
                return
            if not validate_email(email):
                messagebox.showerror('Error', 'Invalid email format.')
                c.lift()
                return
            if not validate_phone(number):
                messagebox.showerror('Error', 'Phone number must be 10 digits.')
                c.lift()
                return
            if not validate_password(createpass):
                messagebox.showerror('Error', 'Password must be 8-15 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character.')
                c.lift()
                return
            if createpass != confirmpass:
                messagebox.showerror('Error', 'Passwords do not match.')
                c.lift()
                return

            conn = sqlite3.connect('Hanni.db')
            with conn:
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS SIGNUP(Firstname text, LastName text, phoneNumber text, Email text, createpassword text, confirmpassword text)")
                cursor.execute('INSERT INTO SIGNUP(Firstname, LastName, phoneNumber, Email, createpassword, confirmpassword) values (?, ?, ?, ?, ?, ?)', (Fname, Lname, number, email, createpass, confirmpass))
            conn.commit()
            messagebox.showinfo('Information', 'Sign-up successfully')
            c.destroy()  # Close the signup window only after successful signup

        c1 = Label(c, text="First Name*").place(x=120, y=100)
        c2 = Label(c, text="Last Name*").place(x=120, y=150)
        c3 = Label(c, text="Phone Number*").place(x=120, y=200)
        c4 = Label(c, text="Email*").place(x=120, y=250)
        c5 = Label(c, text="Password*").place(x=120, y=300)
        c6 = Label(c, text="Confirm Password*").place(x=120, y=350)
        
        ce1 = Entry(c, textvar=Firstname, bd=3)
        ce1.place(x=260, y=100)
        ce2 = Entry(c, textvar=LastName, bd=3)
        ce2.place(x=260, y=150)
        ce3 = Entry(c, textvar=phoneNumber, bd=3)
        ce3.place(x=260, y=200)
        ce4 = Entry(c, textvar=Email, bd=3)
        ce4.place(x=260, y=250)
        ce5 = Entry(c, textvar=createpassword, bd=3, show='*')
        ce5.place(x=260, y=300)
        ce6 = Entry(c, textvar=confirmpassword, bd=3, show='*')
        ce6.place(x=260, y=350)

        # SignUp Submit Button
        submit_button = Button(c, text="SUBMIT/Enviar", command=database, font=('Dotum', 10))
        submit_button.place(x=280, y=400)
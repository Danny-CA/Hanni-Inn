import tkinter as tk
from tkinter import messagebox
import subprocess

def execute_hotel_booking():
    try:
        subprocess.run(['python', 'scripts/español.py'])
        root.destroy()  # Cierra la ventana principal
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def execute_prueba():
    try:
        subprocess.run(['python', 'scripts/english.py'])
        root.destroy()  # Cierra la ventana principal
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}") 

def main():
    global root
    root = tk.Tk()
    root.title("Selecciona una opción")
    root.geometry("400x200")
    root.configure(bg="#F0F0FF")

    label = tk.Label(root, text="Elige una opción", font=('Dotum', 18), bg="#F0F0FF")
    label.pack(pady=20)

    button1 = tk.Button(root, text="Español", command=execute_hotel_booking, font=('Dotum', 14), bg="#83838B", fg="white", width=25)
    button1.pack(pady=10)

    button2 = tk.Button(root, text="English", command=execute_prueba, font=('Dotum', 14), bg="#83838B", fg="white", width=25)
    button2.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

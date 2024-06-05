import tkinter as tk
from tkinter import messagebox
import subprocess

#Parte actualizada añadida por ángel:
#
#Actualización de los paquetes necesarios para la ejecución y transformación
import sys
import os

def install_or_update(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

def check_tkinter():
    try:
        import tkinter
    except ImportError:
        print("tkinter no está instalado. Por favor, instálalo manualmente.")
        sys.exit(1)

def check_dos2unix():
    if os.name == 'nt':
        # No hacer nada en Windows
        return
    try:
        result = subprocess.run(["dos2unix", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode().strip())
    except FileNotFoundError:
        print("dos2unix no está instalado. Por favor, instálalo manualmente.")
        sys.exit(1)



def main():
    with open('requirements.txt', 'r') as file:
        packages = file.readlines()

    for package in packages:
        package = package.strip()
        if package:
            install_or_update(package)

    check_tkinter()
    check_dos2unix()


def execute_hotel_booking():
    try:
        subprocess.run(['python3', 'scripts/español.py'])
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

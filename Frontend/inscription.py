import tkinter as tk

def on_register():
    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()
    print(f"tentative d'inscription avec : {username} / {email} / {password}")

root = tk.Tk()
root.title("inscription")

label_username = tk.Label(root, text="nom d'utilisateur :")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_email = tk.Label(root, text="email :")
label_email.pack()
entry_email = tk.Entry(root)
entry_email.pack()

label_password = tk.Label(root, text="mot de passe :")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

button_register = tk.Button(root, text="s'inscrire", command=on_register)
button_register.pack()

root.mainloop()
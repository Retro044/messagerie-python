import tkinter as tk

def on_login():
    username = entry_username.get()
    password = entry_password.get()
    print(f"tentative de connexion avec : {username} / {password}")

root = tk.Tk()
root.title("connexion")

label_username = tk.Label(root, text="nom d'utilisateur :")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="mot de passe :")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

button_login = tk.Button(root, text="se connecter", command=on_login)
button_login.pack()

root.mainloop()
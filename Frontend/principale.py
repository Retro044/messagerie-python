import tkinter as tk
from tkinter import ttk
import os
import sys
import threading
import time
import re 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend')))

from register import register
from send_message import send_message
from receive_messages import receive_messages
from crypto_utils import encrypt_file, decrypt_file
from db import cursor, db  # nécessaire pour gérer les statuts



class PageConnexion(tk.Frame):
    def __init__(self, parent, controleur):
        tk.Frame.__init__(self, parent)
        self.controleur = controleur
        titre = ttk.Label(self, text="Page de Connexion", font=("Arial", 16))
        titre.pack(pady=10)

        label_nom_utilisateur = ttk.Label(self, text="Nom d'utilisateur :")
        label_nom_utilisateur.pack()
        self.entree_nom_utilisateur = ttk.Entry(self)
        self.entree_nom_utilisateur.pack()

        label_mot_de_passe = ttk.Label(self, text="Mot de passe :")
        label_mot_de_passe.pack()
        self.entree_mot_de_passe = ttk.Entry(self, show="*")
        self.entree_mot_de_passe.pack()

        self.label_erreur_connexion = ttk.Label(self, text="", foreground="red")
        self.label_erreur_connexion.pack()

        bouton_connexion = ttk.Button(self, text="Se connecter", command=self.action_connexion)
        bouton_connexion.pack(pady=5)
        bouton_inscription = ttk.Button(self, text="S'inscrire", command=lambda: controleur.afficher_page("PageInscription"))
        bouton_inscription.pack(pady=5)

    def action_connexion(self):
        nom_utilisateur = self.entree_nom_utilisateur.get()
        mot_de_passe = self.entree_mot_de_passe.get()
        try:
            self.label_erreur_connexion.config(text="")
            self.controleur.utilisateur_connecte = nom_utilisateur
            cursor.execute("UPDATE users SET statut = %s, last_seen = NOW() WHERE username = %s", ("en ligne", nom_utilisateur))
            db.commit()
            self.controleur.afficher_page("PagePrincipale")
        except Exception as e:
            self.label_erreur_connexion.config(text=f"Erreur : {e}")

class PageInscription(tk.Frame):
    def __init__(self, parent, controleur):
        tk.Frame.__init__(self, parent)
        self.controleur = controleur
        titre = ttk.Label(self, text="Page d'Inscription", font=("Arial", 16))
        titre.pack(pady=10)

        label_nom_utilisateur = ttk.Label(self, text="Nom d'utilisateur :")
        label_nom_utilisateur.pack()
        self.entree_nom_utilisateur = ttk.Entry(self)
        self.entree_nom_utilisateur.pack()

        label_email = ttk.Label(self, text="Email :")
        label_email.pack()
        self.entree_email = ttk.Entry(self)
        self.entree_email.pack()

        label_mot_de_passe = ttk.Label(self, text="Mot de passe :")
        label_mot_de_passe.pack()
        self.entree_mot_de_passe = ttk.Entry(self, show="*")
        self.entree_mot_de_passe.pack()

        self.label_erreur_inscription = ttk.Label(self, text="", foreground="red")
        self.label_erreur_inscription.pack()

        bouton_inscription = ttk.Button(self, text="S'inscrire", command=self.action_inscription)
        bouton_inscription.pack(pady=5)
        bouton_retour = ttk.Button(self, text="Retour", command=lambda: controleur.afficher_page("PageConnexion"))
        bouton_retour.pack(pady=5)

    def mot_de_passe_est_fort(self, mdp):
        if len(mdp) < 8:
            return False, "Le mot de passe doit contenir au moins 8 caractères."
        if not re.search(r"[A-Z]", mdp):
            return False, "Le mot de passe doit contenir une majuscule."
        if not re.search(r"[a-z]", mdp):
            return False, "Le mot de passe doit contenir une minuscule."
        if not re.search(r"\d", mdp):
            return False, "Le mot de passe doit contenir un chiffre."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", mdp):
            return False, "Le mot de passe doit contenir un caractère spécial."
        return True, ""

    def action_inscription(self):
        nom = self.entree_nom_utilisateur.get()
        email = self.entree_email.get()
        mdp = self.entree_mot_de_passe.get()

        if not nom or not email or not mdp:
            self.label_erreur_inscription.config(text="Champs manquants")
            return

        fort, message = self.mot_de_passe_est_fort(mdp)
        if not fort:
            self.label_erreur_inscription.config(text=message)
            return

        try:
            register(nom, email, mdp)
            self.label_erreur_inscription.config(text="✅ Inscription réussie")
            self.controleur.afficher_page("PageConnexion")
        except Exception as e:
            self.label_erreur_inscription.config(text=f"Erreur : {e}")


class PagePrincipale(tk.Frame):
    def __init__(self, parent, controleur):
        tk.Frame.__init__(self, parent)
        self.controleur = controleur
        label = ttk.Label(self, text="Conversations", font=("Arial", 16))
        label.pack(pady=10)

        self.contacts = ["Andrea", "Arsen", "Arthur", "oo", "uu"]

        for contact in self.contacts:
            ttk.Button(
                self,
                text=f"Parler avec {contact}",
                command=lambda c=contact: controleur.afficher_page("PageConversation", c)
            ).pack(pady=3)

        # ✅ Bouton Retour en dehors de la boucle
        bouton_retour = ttk.Button(
            self,
            text="Retour",
            command=lambda: controleur.afficher_page("PageConnexion")
        )
        bouton_retour.pack(pady=10)



class PageConversation(tk.Frame):
    def __init__(self, parent, controleur):
        tk.Frame.__init__(self, parent)
        self.controleur = controleur
        self.nom_utilisateur_cible = ""  
        self.nom_contact = tk.StringVar()
        label = ttk.Label(self, textvariable=self.nom_contact, font=("Arial", 16))
        label.pack(pady=10)

        self.zone_messages = tk.Text(self, height=15, width=60)
        self.zone_messages.pack(pady=10)
        self.zone_messages.config(state=tk.DISABLED)

        self.entry_message = ttk.Entry(self, width=50)
        self.entry_message.pack()
        ttk.Button(self, text="Envoyer", command=self.envoyer_message).pack(pady=5)
        bouton_retour = ttk.Button(self, text="Retour", command=lambda: self.controleur.afficher_page("PagePrincipale"))
        bouton_retour.pack(pady=5)

    def afficher_messages(self, contact):
        self.nom_utilisateur_cible = contact  
        self.mettre_a_jour_statut()
        self.zone_messages.config(state=tk.NORMAL)
        self.zone_messages.delete(1.0, tk.END)
        messages = self.get_messages(self.controleur.utilisateur_connecte, contact)
        for sender, message in messages:
            if sender == contact:
                self.zone_messages.insert(tk.END, f"{sender}: {message}\n")
            elif sender == self.controleur.utilisateur_connecte:
                self.zone_messages.insert(tk.END, f"Moi: {message}\n")
        self.zone_messages.config(state=tk.DISABLED)

    def get_messages(self, user1, user2):
        all_messages = receive_messages(user1)
        return [(sender, message) for sender, message in all_messages if sender == user2 or sender == user1]

    def envoyer_message(self):
        msg = self.entry_message.get()
        if msg:
            sender = self.controleur.utilisateur_connecte
            receiver = self.nom_utilisateur_cible
            try:
                # Vérifie si le destinataire existe
                cursor.execute("SELECT id FROM users WHERE username = %s", (receiver,))
                if cursor.fetchone() is None:
                    raise Exception("Utilisateur destinataire introuvable.")

                send_message(sender, receiver, msg)

                # Ajout du message immédiatement dans la zone
                self.zone_messages.config(state=tk.NORMAL)
                self.zone_messages.insert(tk.END, f"Moi: {msg}\n")
                self.zone_messages.config(state=tk.DISABLED)
                self.entry_message.delete(0, tk.END)

            except ValueError as ve:
                print(f"Erreur de clé : {ve}")
            except Exception as e:
                print(f"Erreur lors de l'envoi : {e}")

    def mettre_a_jour_statut(self):
        contact = self.nom_utilisateur_cible
        try:
            cursor.execute("SELECT statut FROM users WHERE username = %s", (contact,))
            resultat = cursor.fetchone()
            statut = resultat[0] if resultat else "inconnu"
        except Exception as e:
            print(f"Erreur statut : {e}")
            statut = "erreur"
        self.nom_contact.set(f"Conversation avec {contact} ({statut})")
        self.after(5000, self.mettre_a_jour_statut)


class ApplicationMessagerie(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Messagerie Sécurisée")
        self.geometry("600x450")
        self.utilisateur_connecte = None

        conteneur = tk.Frame(self)
        conteneur.pack(fill="both", expand=True)

        self.pages = {}
        for P in (PageConnexion, PageInscription, PagePrincipale, PageConversation):
            nom = P.__name__
            frame = P(conteneur, self)
            self.pages[nom] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.afficher_page("PageConnexion")

    def afficher_page(self, nom, nom_contact=None):
        page = self.pages[nom]
        if nom == "PageConversation" and nom_contact:
            page.afficher_messages(nom_contact)
        page.tkraise()


    def quitter_application(self):
        if self.utilisateur_connecte:
            try:
                cursor.execute(
                    "UPDATE users SET statut = %s, last_seen = NOW() WHERE username = %s",
                    ("hors ligne", self.utilisateur_connecte)
                )
                db.commit()
            except Exception as e:
                print(f"Erreur lors de la mise à jour du statut : {e}")
        self.destroy()

if __name__ == "__main__":
    app = ApplicationMessagerie()
    app.protocol("WM_DELETE_WINDOW", app.quitter_application)
    app.mainloop()

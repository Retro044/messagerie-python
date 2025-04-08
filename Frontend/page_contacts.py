import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class ApplicationContacts:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Gestionnaire de Contacts")
        self.racine.geometry("700x500")
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6)
        
        # Configuration initiale
        self.contacts_db = {}
        self.fichier_db = "contacts_db.json"
        self.charger_donnees()
        
        # Interface principale
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface utilisateur principale"""
        # Frame principal
        main_frame = ttk.Frame(self.racine)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Barre de recherche
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        self.search_var = tk.StringVar()
        ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            search_frame,
            text="Rechercher",
            command=self.filtrer_contacts
        ).pack(side="left", padx=5)
        
        # Liste des contacts avec scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(
            list_frame,
            columns=("Nom", "Email", "Téléphone"),
            show="headings",
            selectmode="browse"
        )
        
        # Configuration des colonnes
        self.tree.heading("Nom", text="Nom", anchor="w")
        self.tree.heading("Email", text="Email", anchor="w")
        self.tree.heading("Téléphone", text="Téléphone", anchor="w")
        
        self.tree.column("Nom", width=200)
        self.tree.column("Email", width=200)
        self.tree.column("Téléphone", width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Boutons d'action
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(
            btn_frame,
            text="Ajouter",
            command=self.ouvrir_ajout_contact,
            style="Accent.TButton"
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Modifier",
            command=self.modifier_contact,
            state="disabled"
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Supprimer",
            command=self.supprimer_contact,
            style="Danger.TButton"
        ).pack(side="right", padx=5)
        
        # Styles personnalisés
        self.style.configure("Accent.TButton", foreground="white", background="#4CAF50")
        self.style.configure("Danger.TButton", foreground="white", background="#f44336")
        
        # Événements
        self.search_var.trace_add("write", lambda *args: self.filtrer_contacts())
        self.tree.bind("<Double-1>", lambda e: self.modifier_contact())
        
        # Chargement initial
        self.actualiser_liste()
    
    def charger_donnees(self):
        """Charge les contacts depuis le fichier JSON"""
        if os.path.exists(self.fichier_db):
            try:
                with open(self.fichier_db, "r") as f:
                    self.contacts_db = json.load(f)
            except:
                self.contacts_db = {}
        else:
            # Données exemple
            self.contacts_db = {
                "Alice Dupont": {
                    "email": "alice@example.com",
                    "telephone": "0123456789"
                },
                "Bob Martin": {
                    "email": "bob@example.com",
                    "telephone": "0987654321"
                }
            }
            self.sauvegarder_donnees()
    
    def sauvegarder_donnees(self):
        """Sauvegarde les contacts dans le fichier JSON"""
        with open(self.fichier_db, "w") as f:
            json.dump(self.contacts_db, f, indent=4)
    
    def actualiser_liste(self):
        """Met à jour l'affichage de la liste"""
        self.tree.delete(*self.tree.get_children())
        for nom, infos in self.contacts_db.items():
            self.tree.insert("", "end", values=(
                nom,
                infos.get("email", ""),
                infos.get("telephone", "")
            ))
    
    def filtrer_contacts(self):
        """Filtre les contacts selon la recherche"""
        recherche = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        
        for nom, infos in self.contacts_db.items():
            if (recherche in nom.lower() or 
                recherche in infos.get("email", "").lower() or
                recherche in infos.get("telephone", "")):
                
                self.tree.insert("", "end", values=(
                    nom,
                    infos.get("email", ""),
                    infos.get("telephone", "")
                ))
    
    def ouvrir_ajout_contact(self):
        """Ouvre la fenêtre d'ajout de contact"""
        fenetre = tk.Toplevel(self.racine)
        fenetre.title("Nouveau Contact")
        fenetre.transient(self.racine)
        fenetre.grab_set()
        
        # Variables TKinter
        self.var_nom = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telephone = tk.StringVar()
        
        # Configuration de la fenêtre
        form_frame = ttk.Frame(fenetre)
        form_frame.pack(padx=20, pady=20)
        
        # Champs du formulaire
        ttk.Label(form_frame, text="Nom complet:").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_nom, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_email, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="Téléphone:").grid(row=2, column=0, sticky="e", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_telephone, width=30).grid(row=2, column=1, pady=5)
        
        # Boutons
        btn_frame = ttk.Frame(fenetre)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="Annuler",
            command=fenetre.destroy
        ).pack(side="left", padx=10)
        
        ttk.Button(
            btn_frame,
            text="Valider",
            command=lambda: self.valider_contact(fenetre),
            style="Accent.TButton"
        ).pack(side="right", padx=10)
        
        # Raccourci clavier
        fenetre.bind("<Return>", lambda e: self.valider_contact(fenetre))
    
    def valider_contact(self, fenetre):
        """Valide l'ajout ou la modification d'un contact"""
        nom = self.var_nom.get().strip()
        email = self.var_email.get().strip()
        telephone = self.var_telephone.get().strip()
        
        # Validation
        if not nom:
            messagebox.showwarning("Erreur", "Le nom est obligatoire")
            return
        
        # Vérification format email
        if email and "@" not in email:
            messagebox.showwarning("Erreur", "Format d'email invalide")
            return
        
        # Ajout/modification
        self.contacts_db[nom] = {
            "email": email,
            "telephone": telephone
        }
        
        self.sauvegarder_donnees()
        self.actualiser_liste()
        fenetre.destroy()
        messagebox.showinfo("Succès", "Contact enregistré")
    
    def modifier_contact(self):
        """Ouvre la fenêtre de modification pour le contact sélectionné"""
        selection = self.tree.selection()
        if not selection:
            return
            
        nom = self.tree.item(selection[0])["values"][0]
        
        # Pré-remplissage des champs
        self.var_nom = tk.StringVar(value=nom)
        self.var_email = tk.StringVar(value=self.contacts_db[nom].get("email", ""))
        self.var_telephone = tk.StringVar(value=self.contacts_db[nom].get("telephone", ""))
        
        # Fenêtre de modification (réutilise ouvrir_ajout_contact)
        self.ouvrir_ajout_contact()
    
    def supprimer_contact(self):
        """Supprime le contact sélectionné"""
        selection = self.tree.selection()
        if not selection:
            return
            
        nom = self.tree.item(selection[0])["values"][0]
        
        if messagebox.askyesno("Confirmation", f"Supprimer {nom} ?"):
            del self.contacts_db[nom]
            self.sauvegarder_donnees()
            self.actualiser_liste()
            messagebox.showinfo("Succès", "Contact supprimé")

if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationContacts(root)
    root.mainloop()
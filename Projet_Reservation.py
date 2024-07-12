import re
import pickle
from datetime import datetime, timedelta
from tabulate import tabulate  # Importer la bibliothèque tabulate
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar

class Reservation:
    def __init__(self, nom, prenom, heure_debut):
        self.nom = nom
        self.prenom = prenom
        self.heure_debut = heure_debut
        self.heure_fin = heure_debut + timedelta(minutes=20)

    def __str__(self):
        return f"Nom: {self.nom}, Prénom: {self.prenom}, Date: {self.heure_debut.strftime('%Y-%m-%d')}, Début: {self.heure_debut.strftime('%H:%M')}, Fin: {self.heure_fin.strftime('%H:%M')}"

    def __repr__(self):
        return f"Réservé de {self.heure_debut.strftime('%H:%M')} à {self.heure_fin.strftime('%H:%M')}"

class SystemeReservation:
    def __init__(self, root):
        self.reservations = []
        self.code_affichage = "1234"
        self.load_reservations()
        self.root = root
        self.setup_gui()

    def ajouter_reservation(self, nom, prenom, heure_debut):
        reservation = Reservation(nom, prenom, heure_debut)
        self.reservations.append(reservation)
        messagebox.showinfo("Succès", "Créneau réservé avec succès.")
        self.save_reservations()
        self.refresh_creneaux_disponibles()

    def afficher_reservations(self):
        if self.reservations:
            details = "\n".join([str(r) for r in self.reservations])
            messagebox.showinfo("Réservations", details)
        else:
            messagebox.showinfo("Réservations", "Aucune réservation n'a été effectuée.")

    def afficher_creneaux_disponibles(self):
        creneaux_disponibles = []
        selected_date = self.calendar.selection_get()
        heure = datetime.combine(selected_date, datetime.min.time()).replace(hour=8)
        
        while heure.hour < 17:
            if self.heure_valide(heure):
                creneaux_disponibles.append(heure)
            heure += timedelta(minutes=20)
        
        return creneaux_disponibles

    def heure_valide(self, heure_debut):
        for reservation in self.reservations:
            if heure_debut.date() == reservation.heure_debut.date() and \
               heure_debut >= reservation.heure_debut and heure_debut < reservation.heure_fin:
                return False
        return True

    def convertir_heure(self, heure_str):
        pattern = r'^\d{2}:\d{2}$'
        if not re.match(pattern, heure_str):
            return None

        try:
            heure = datetime.strptime(heure_str, '%H:%M')
            if heure.minute % 20 != 0:
                messagebox.showerror("Erreur", "L'heure doit être un multiple de 20 minutes.")
                return None
            return heure
        except ValueError:
            return None

    def setup_gui(self):
        self.root.title("Système de Réservation")
        
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.calendar = Calendar(frame, selectmode='day', date_pattern='y-mm-dd')
        self.calendar.grid(row=0, column=0, columnspan=2)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_select)

        self.tree = ttk.Treeview(frame, columns=("heure"), show='headings', selectmode="browse")
        self.tree.heading("heure", text="Heure")
        self.tree.grid(row=1, column=0, columnspan=2)

        ttk.Button(frame, text="Afficher créneaux", command=self.refresh_creneaux_disponibles).grid(row=2, column=0, columnspan=2)

        ttk.Label(frame, text="Nom:").grid(row=3, column=0, sticky=tk.E)
        self.nom_entry = ttk.Entry(frame)
        self.nom_entry.grid(row=3, column=1)

        ttk.Label(frame, text="Prénom:").grid(row=4, column=0, sticky=tk.E)
        self.prenom_entry = ttk.Entry(frame)
        self.prenom_entry.grid(row=4, column=1)

        ttk.Button(frame, text="Réserver", command=self.handle_reservation).grid(row=5, column=0, columnspan=2)
        ttk.Button(frame, text="Afficher les réservations", command=self.show_reservations).grid(row=6, column=0, columnspan=2)

    def refresh_creneaux_disponibles(self):
        creneaux_disponibles = self.afficher_creneaux_disponibles()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i, creneau in enumerate(creneaux_disponibles):
            self.tree.insert("", "end", iid=i, values=(creneau.strftime('%H:%M'),))

    def on_date_select(self, event):
        self.refresh_creneaux_disponibles()

    def handle_reservation(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un créneau.")
            return

        heure_str = self.tree.item(selected_item[0], 'values')[0]
        selected_date = self.calendar.selection_get()
        heure_debut = datetime.combine(selected_date, self.convertir_heure(heure_str).time())
        if not heure_debut:
            messagebox.showerror("Erreur", "Créneau invalide.")
            return

        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        if not nom or not prenom:
            messagebox.showerror("Erreur", "Veuillez entrer le nom et le prénom.")
            return

        self.ajouter_reservation(nom, prenom, heure_debut)
        self.refresh_creneaux_disponibles()

    def show_reservations(self):
        reservations = self.afficher_reservations_gui()
        if reservations:
            top = tk.Toplevel(self.root)
            top.title("Réservations")
            text = tk.Text(top, wrap='word')
            text.pack(expand=1, fill='both')
            text.insert('1.0', reservations)

    def afficher_reservations_gui(self):
        if self.reservations:
            details = "\n".join([str(r) for r in self.reservations])
            return details
        else:
            return "Aucune réservation n'a été effectuée."

    def save_reservations(self):
        with open('reservations.pkl', 'wb') as f:
            pickle.dump(self.reservations, f)

    def load_reservations(self):
        try:
            with open('reservations.pkl', 'rb') as f:
                self.reservations = pickle.load(f)
        except FileNotFoundError:
            self.reservations = []

# Programme principal
root = tk.Tk()
systeme = SystemeReservation(root)
root.mainloop()

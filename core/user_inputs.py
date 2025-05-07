# Copyright © 2025 Maxence Cailleteau - HEIG-VD - GRIPIT
# SPDX‑License‑Identifier: GPL‑3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License 
# and any later version.
#______________________________________________________________________


import os
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

# Créer la fenêtre principale
root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale

def demander_valeur(message):
    try:
        # Ouvrir une fenêtre de dialogue pour saisir une valeur
        valeur = simpledialog.askfloat("Entrée", message)
        if valeur is not None:
            # Afficher la valeur dans une boîte de dialogue
            #messagebox.showinfo("Valeur entrée", f"Vous avez entré : {valeur}")
            return valeur
        else:
            messagebox.showinfo("Annulé", "Vous n'avez rien entré.")
    except ValueError:
        # Gérer les erreurs si la conversion échoue
        messagebox.showerror("Erreur", "Valeur invalide. Veuillez entrer un nombre décimal.")


def demander_texte():
    # Ouvrir une boîte de dialogue pour saisir un texte
    texte = simpledialog.askstring("Entrée", "Veuillez entrer un texte :")
    if texte:  # Si l'utilisateur entre un texte
        #messagebox.showinfo("Texte saisi", f"Vous avez entré : {texte}")
        return texte
    else:
        messagebox.showinfo("Annulé", "Vous n'avez rien entré.")


def demander_confirmation(message)->bool:
    # Ouvre une boîte de dialogue Oui/Non
    return messagebox.askyesno("Confirmation", message)


def select_and_verify_csv_file(message):
    # Open a file dialog for the user to select a file
    #root = tk.Tk()
    #root.withdraw()  # Hide the root window
    root.attributes('-topmost', True)  # Bring the dialog to the front
    messagebox.showinfo("File Selection", message)
    # Open a file dialog for the user to select a file
    file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    # Check if a file was selected
    if not file_path:
        print("No file selected.")
        return None
    # Verify the file extension
    if not file_path.lower().endswith('.csv'):
        print(f"Invalid file format: {file_path}. Please select a .csv file.")
        return None
    print(f"File selected: {file_path}")
    return file_path



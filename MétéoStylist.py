from experta import *
import tkinter as tk
from tkinter import messagebox

class Meteo(Fact):
    """Information sur la météo"""
    pass

class ConseillerVestimentaire(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.conseils = []
    
    @Rule(Meteo(temp=P(lambda temp: temp <= 5)),
          Meteo(humidite=P(lambda humidite: humidite >= 60)),
          Meteo(pluie=True))
    def condition_tres_froide_humide_pluvieuse(self):
        self.conseils.append("- Très froid, humide et pluvieux. Portez un manteau imperméable, des bottes et un bonnet.")

    @Rule(Meteo(temp=P(lambda temp: 6 <= temp <= 15)),
          Meteo(vent=P(lambda vent: vent >= 20)),
          Meteo(soleil=False))
    def condition_fraiche_ventee_nuageuse(self):
        self.conseils.append("- Temps frais, venteux et nuageux. Optez pour une veste coupe-vent et un pull.")

    @Rule(Meteo(temp=P(lambda temp: 16 <= temp <= 22)),
          Meteo(uv=P(lambda uv: uv <= 3)),
          Meteo(soleil=True))
    def condition_moderement_chaude_faible_uv_ensoleillee(self):
        self.conseils.append("- Température modérée avec faible UV et ensoleillé. Portez des vêtements légers et une casquette.")

    @Rule(Meteo(temp=P(lambda temp: 23 <= temp <= 30)),
          Meteo(humidite=P(lambda humidite: humidite < 40)),
          Meteo(soleil=True))
    def condition_chaude_seche_ensoleillee(self):
        self.conseils.append("- Temps chaud, sec et ensoleillé. Privilégiez les vêtements aérés et protégez-vous du soleil.")

    @Rule(Meteo(temp=P(lambda temp: temp > 30)),
          Meteo(uv=P(lambda uv: uv > 5)),
          Meteo(vent=P(lambda vent: vent < 10)))
    def condition_tres_chaude_uv_eleve_peu_de_vent(self):
        self.conseils.append("- Très chaud avec un indice UV élevé et peu de vent. Utilisez de la crème solaire et portez un chapeau.")

    @Rule(Meteo(humidite=P(lambda humidite: humidite >= 60)),
          Meteo(pluie=True),
          Meteo(vent=P(lambda vent: vent > 15)))
    def condition_humide_pluvieuse_ventee(self):
        self.conseils.append("- Temps humide, pluvieux et venteux. Optez pour un imperméable robuste et un parapluie résistant au vent.")

    @Rule(Meteo(temp=P(lambda temp: temp < 0)),
          Meteo(neige=True),
          Meteo(vent=P(lambda vent: vent < 5)))
    def condition_gel_neigeux_calme(self):
        self.conseils.append("- Conditions de gel avec neige et peu de vent. Habillez-vous très chaudement, portez des boots de neige et des gants.")

    @Rule(Meteo(temp=P(lambda temp: 0 <= temp <= 10)),
          Meteo(humidite=P(lambda humidite: humidite < 50)),
          Meteo(soleil=True))
    def condition_froide_seche_ensoleillee(self):
        self.conseils.append("- Temps froid, sec et ensoleillé. Portez des couches de vêtements et une paire de lunettes de soleil.")

    @Rule(Meteo(temp=P(lambda temp: 10 < temp <= 20)),
          Meteo(vent=P(lambda vent: vent >= 10)),
          Meteo(uv=P(lambda uv: uv > 3)),
          Meteo(pluie=False))
    def condition_temperee_ventee_uv_moderes(self):
        self.conseils.append("- Température tempérée, ventée avec un indice UV modéré. Portez un coupe-vent léger et appliquez de la crème solaire.")


    def afficher_conseil(self):
        conseil_final = "\n".join(self.conseils)
        messagebox.showinfo("Conseil Vestimentaire", conseil_final)
    

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Conseiller Vestimentaire")

# Définir la taille de la fenêtre
width = 400
height = 500
root.geometry(f"{width}x{height}")

# Obtenir les dimensions de l'écran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculer la position x et y pour centrer la fenêtre
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

# Positionner la fenêtre au centre de l'écran
root.geometry(f'+{x}+{y}')

# Variables pour les boutons radio
temp_var = tk.IntVar()
humidite_var = tk.IntVar()
uv_var = tk.IntVar()
vent_var = tk.IntVar()
soleil_var = tk.BooleanVar()
pluie_var = tk.BooleanVar()
neige_var = tk.BooleanVar()
nuage_var = tk.BooleanVar()

# Fonction appelée lorsque l'utilisateur soumet ses choix
def submit_choices():
    temp = temp_var.get()
    humidite = humidite_var.get()
    uv = uv_var.get()
    vent = vent_var.get()
    soleil = soleil_var.get()
    pluie = pluie_var.get()
    neige = neige_var.get()
    nuage=nuage_var.get()
    # Afficher les choix de l'utilisateur
    messagebox.showinfo("Choix", f"Température: {temp}\nHumidité: {humidite}\nUV: {uv}\nVent: {vent}\nSoleil: {soleil}\nPluie: {pluie}\nNeige: {neige}")

    # Exécution moteur
    conseiller = ConseillerVestimentaire()
    conseiller.reset()

    conseiller.declare(Meteo(temp=temp,humidite=humidite,uv=uv,vent=vent,soleil=soleil,pluie=pluie,neige=neige))
    conseiller.run()
    conseiller.afficher_conseil()

# Widgets pour la température
tk.Label(root, text="Température:").pack()
tk.Radiobutton(root, text="0-15", variable=temp_var, value=0).pack()
tk.Radiobutton(root, text="16-25", variable=temp_var, value=16).pack()
tk.Radiobutton(root, text="26-35", variable=temp_var, value=26).pack()

# Widgets pour l'humidité
tk.Label(root, text="Humidité:").pack()
tk.Radiobutton(root, text="0-30", variable=humidite_var, value=30).pack()
tk.Radiobutton(root, text="31-60", variable=humidite_var, value=60).pack()

# Widgets pour l'indice UV
tk.Label(root, text="Indice UV:").pack()
tk.Radiobutton(root, text="Faible", variable=uv_var, value=1).pack()
tk.Radiobutton(root, text="Moyen", variable=uv_var, value=5).pack()

# Widgets pour le vent
tk.Label(root, text="Vent:").pack()
tk.Radiobutton(root, text="Calme", variable=vent_var, value=0).pack()
tk.Radiobutton(root, text="Modéré", variable=vent_var, value=10).pack()
tk.Radiobutton(root, text="Extreme", variable=vent_var, value=20).pack()

# Widgets pour soleil et nuage
tk.Label(root, text="Conditions:").pack()
tk.Checkbutton(root, text="Ensoleillé", variable=soleil_var).pack()
tk.Checkbutton(root, text="Nuageux", variable=nuage_var).pack()

# Widgets pour précipitations
tk.Label(root, text="Précipitations:").pack()
tk.Checkbutton(root, text="Pluie", variable=pluie_var).pack()
tk.Checkbutton(root, text="Neige", variable=neige_var).pack()

submit_button = tk.Button(root, text="Soumettre", command=submit_choices)
submit_button.pack()

# Lancer l'application Tkinter
root.mainloop()



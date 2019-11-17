from elopy import *
from tkinter import * 
from tkinter import simpledialog
from tkinter import messagebox


def verifier_joueurs():

    

    ok = True
    suffisant = (players[0].get() != '' or players[1].get() != '') and (players[2].get() != '' or players[3].get() != '') 

    for player in players:

        name = player.get()

        if elo.isPlayer(name) or (name == '' and suffisant):
            color = 'lightgreen'
        else:
            color = 'tomato'
            ok = False

        player.config(bg = color)

  
    if ok:
        verifier.config(stat=DISABLED)
        victoireA_bouton.config(stat=NORMAL)
        victoireB_bouton.config(stat=NORMAL)
        
        for player in players : player.config(stat=DISABLED, bg=color)


def ajouter_joueur():
    ok = False
    while not ok:
        name = simpledialog.askstring("Nouveau joueur", "Nom du joueur : ", parent=fenetre)
        if not elo.isPlayer(name):
            ok = True
        else:
            messagebox.showwarning("Nouveau joueur", 'Le nom "{}" existe déjà, choisissez en un autre...'.format(name))
        
    elo.addPlayer(name)

    messagebox.showinfo("Nouveau joueur", "Le joueur {} a bien été ajouté !".format(name))


def victoireA():
    victoire(0)

def victoireB():
    victoire(1)

def victoire(team):

    scores = {}
    
    
    names1 = []
    if players[0].get() != '':
        names1.append(players[0].get())
    if players[1].get() != '':
        names1.append(players[1].get())
    
    names2 = []
    if players[2].get() != '':
        names2.append(players[2].get())
    if players[3].get() != '':
        names2.append(players[3].get())

    for name in names1 + names2:
        rating =elo.getPlayerRating(name)
        scores[name] = '{} : #{}({}) -> '.format(name, rating[1], rating[0])
    
    elo.recordXvXMatch(names1, names2, team)

    message = ''
    for name in names1 + names2:
        rating = elo.getPlayerRating(name)
        scores[name] = scores[name] + '#{}({})'.format(rating[1], rating[0])
        message += scores[name] + '\n'

    
    
    messagebox.showinfo("Résultats", message)

    for player in players:
        player.config(stat=NORMAL, bg='white')

    victoireA_bouton.config(stat=DISABLED)
    victoireB_bouton.config(stat=DISABLED)
    verifier.config(stat=NORMAL)

def score_joueur():
    ok = False
    while not ok:
        name = simpledialog.askstring("Score joueur", "Nom du joueur : ", parent=fenetre)
        if elo.isPlayer(name):
            ok = True
        else:
            messagebox.showwarning("Score joueur", 'Le nom "{}" n\'existe pas dans la base de donnée...'.format(name))
    rating = elo.getPlayerRating(name)
    messagebox.showinfo("Score joueur", "#{} {} : {}".format(rating[1], name, rating[0]))

def classement():
    clas = elo.getRatingList()
    liste = ''
    i = 1
    for player in clas:
        liste += '#{} {} : {}\n'.format(i, player[0], int(player[1]))
        i += 1

    messagebox.showinfo("Classement", liste)

    

elo = Elo()

fenetre = Tk()
fenetre.title("EloBP")


messagebox.showinfo("Credits", "EloBP®\nIdée originale : Raùl\nCode : Colin\nPassez une bonne soirée avec notre bénédiction <3")



label = Label(fenetre, text="vs.")

resultats = LabelFrame(fenetre, text = "Résultats")

teams = [LabelFrame(fenetre, text = "Equipe 1"), LabelFrame(fenetre, text = "Equipe 2")]

players = []
for i in range(2):
    for j in range(2):
        players.append(Entry(teams[i], width=20))
        players[-1].pack()

victoireA_bouton = Button(resultats, text="Victoire A", command=victoireA, stat=DISABLED)
victoireB_bouton = Button(resultats, text="Victoire B", command=victoireB, stat=DISABLED)

victoireA_bouton.grid(row=0, column=0)
victoireB_bouton.grid(row=0, column=2)


verifier = Button(resultats, text="Lancer la partie", command=verifier_joueurs)
verifier.grid(row=0, column=1)

label.grid(row=0, column=1)

teams[0].grid(row=0, column=0)
teams[1].grid(row=0, column=2)

resultats.grid(row=1, columnspan=3)




# menu
menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Ajouter", command=ajouter_joueur)
menu1.add_command(label="Supprimer")
menubar.add_cascade(label="Joueurs", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Classement", command=classement)
menu2.add_command(label="Score individuel", command=score_joueur)
menubar.add_cascade(label="Scores", menu=menu2)


fenetre.config(menu=menubar)

fenetre.mainloop()
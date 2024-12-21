from tkinter import *
from tkinter import ttk
from random import *
from tkinter import messagebox

global prima
global bombe,vittory
vittory=False
finestra = Tk()
finestra.title("CAMPO MINATO")
finestra.resizable(False, False)

sconfitta=False
def aggiorna(t,timer):
        global sconfitta,vittory
        if sconfitta!=True and vittory!=True:
            try:
                timer.config(text="⏱️"+str(t))
                finestra.after(1000,lambda: aggiorna(t+1,timer))
            except:
                pass
        else:
            pass

def crea_bottone(riga, colonna, gioco, bombe, lista_griglia):
    global mine
    global prima
    larghezza = 4
    altezza = 2
    
    if riga % 2 == 0:
        if colonna % 2 == 0:
            bottone = Button(gioco, bg="#aad751", width=larghezza, height=altezza, border=0)
        else:
            bottone = Button(gioco, bg="#a2d149", width=larghezza, height=altezza, border=0)
    else:
        if colonna % 2 != 0:
            bottone = Button(gioco, bg="#aad751", width=larghezza, height=altezza, border=0)
        else:
            bottone = Button(gioco, bg="#a2d149", width=larghezza, height=altezza, border=0)
    
    bottone.grid(row=riga, column=colonna)
    lista_griglia.append([[riga], [colonna]])
    
    bottone.bind("<Button-1>", lambda event, b=bottone: bottone_cliccato(b, "sinistro", bombe, lista_griglia, riga, colonna))
    bottone.bind("<Button-3>", lambda event, b=bottone: bottone_cliccato(b, "destro", bombe, lista_griglia, riga, colonna))
def scopribombe(gioco):
    global lista_mine,t,timer,sconfitta
    sconfitta=True
    colori=["red","purple","yellow","cyan","green","blue","orange"]
    for i in lista_mine:
        gioco.grid_slaves(row=i[0],column=i[1])[0].config(text="💣",bg=colori[randint(0,6)])
        gioco.after(100)
        gioco.grid_slaves(row=i[0],column=i[1])[0].update()
    messagebox.showerror("SCONFITTA", "Hai perso😢")
    return aggiorna(t,timer)
    
        
def bottone_cliccato(bottone, tasto, bombe, lista_griglia, riga, colonna):
    

    global mine, prima, lista_mine,barra,t,timer

    
        
    

    if tasto == "destro":
        if bottone.cget("text") == "🚩":
            bottone.config(text="")
            mine += 1
            bombe.config(text="🚩" + str(mine))
        else:
            if mine - 1 >= 0:
                if bottone.cget("bg") == "#aad751" or bottone.cget("bg") == "#a2d149":
                    bottone.config(text="🚩")
                    mine -= 1
                    bombe.config(text="🚩" + str(mine))

    if tasto == "sinistro":
        if bottone.cget("bg") == "#aad751" or bottone.cget("bg") == "#a2d149":
            if bottone.cget("text") != "🚩":
                if prima:
                    aggiorna(t,timer)
                    genera_mine(lista_griglia, lista_mine, riga, colonna)
                    prima = False

                if [[riga], [colonna]] in lista_mine:
                    return scopribombe(gioco)
                    
                else:
                    libera_bottone(bottone, riga, colonna, lista_griglia)
def libera_bottone(bottone, riga, colonna, lista_griglia):
    global lista_mine,vittory
    vittory=False
    if riga % 2 == 0:
        if colonna % 2 == 0:
            bottone.config(bg="#e5c29f")
        else:
            bottone.config(bg="#d7b899")
    else:
        if colonna % 2 != 0:
            bottone.config(bg="#e5c29f")
        else:
            bottone.config(bg="#d7b899")
    
    numero_mine_vicine = contavicini(riga, colonna, lista_mine)
    vittoria=True
    for a in lista_griglia:
        if gioco.grid_slaves(row=a[0],column=a[1])[0].cget("bg") == "#aad751" or gioco.grid_slaves(row=a[0],column=a[1])[0].cget("bg") == "#a2d149":
            vittoria=False
    if vittoria==True:
        vittory=True
        messagebox.showinfo("VITTORIA", "Hai vinto!")
        return creagriglia("")
        
    if numero_mine_vicine > 0:
        bottone.config(text=str(numero_mine_vicine))
    else:
        return sblocca_adiacenti(riga, colonna, lista_griglia)

def contavicini(riga, colonna, lista_mine):
    adiacenti = [
        [riga + 1, colonna], [riga - 1, colonna], [riga, colonna + 1], [riga, colonna - 1],
        [riga - 1, colonna - 1], [riga - 1, colonna + 1], [riga + 1, colonna + 1], [riga + 1, colonna - 1]
    ]
    mine = 0
    for adj in adiacenti:
        if [[adj[0]], [adj[1]]] in lista_mine:
            mine += 1
    return mine

def sblocca_adiacenti(riga, colonna, lista_griglia):
    adiacenti = [
        [riga + 1, colonna], [riga - 1, colonna], [riga, colonna + 1], [riga, colonna - 1],
        [riga - 1, colonna - 1], [riga - 1, colonna + 1], [riga + 1, colonna + 1], [riga + 1, colonna - 1]
    ]

    for adj in adiacenti:
        try:
            bottone_adj = gioco.grid_slaves(row=adj[0], column=adj[1])[0]
            if bottone_adj.cget("bg") in ("#aad751", "#a2d149"):  
                libera_bottone(bottone_adj, adj[0], adj[1], lista_griglia)
        except:
            pass

def genera_mine(lista_griglia, lista_mine, riga_iniziale, colonna_iniziale):
    global mine
    adiacenti_iniziali = [
        [riga_iniziale, colonna_iniziale], [riga_iniziale + 1, colonna_iniziale], [riga_iniziale - 1, colonna_iniziale],
        [riga_iniziale, colonna_iniziale + 1], [riga_iniziale, colonna_iniziale - 1], [riga_iniziale + 1, colonna_iniziale + 1],
        [riga_iniziale + 1, colonna_iniziale - 1], [riga_iniziale - 1, colonna_iniziale + 1], [riga_iniziale - 1, colonna_iniziale - 1]
    ]
    
    for adj in adiacenti_iniziali:
        if [[adj[0]], [adj[1]]] in lista_griglia:
            lista_griglia.remove([[adj[0]], [adj[1]]])

    while len(lista_mine) < mine:
        pos = randint(0, len(lista_griglia) - 1)
        lista_mine.append(lista_griglia[pos])
        lista_griglia.pop(pos)

def creagriglia(difficulty):
    global prima, lista_mine,barra,t,timer,sconfitta
    sconfitta=False
    lista_mine = []
    prima = True
    lista_griglia = []
    global mine
    if difficulty=="":
        difficulty="medio"
    for widget in finestra.winfo_children():
        widget.destroy()
    
    def compila2(event=None):
        creagriglia(difficolta.get())

    barra = Frame(finestra)
    barra.pack(fill="x")
    global gioco
    gioco = Frame(finestra)
    gioco.pack()

    difficolta = ttk.Combobox(barra, width=18, state="readonly", textvariable="aa")
    difficolta['values'] = ["facile", "medio", "difficile"]
    difficolta.grid(row=0, column=0, sticky=W)
    difficolta.bind("<<ComboboxSelected>>", compila2)

    if difficulty == "facile":
        mine = 10
    elif difficulty == "medio":
        mine = 40
    elif difficulty == "difficile":
        mine = 100

    bombe = Label(barra, text="🚩" + str(mine),font=30)
    bombe.grid(row=0, column=1)
    t=0
    timer =Label(barra,text="⏱️"+str(t),font=30)
    timer.grid(column=2,row=0,columnspan=3)
    
    t=0
    timer =Label(barra,text="⏱️"+str(t),font=30)
    timer.grid(column=2,row=0)
    
    if difficulty == "facile":
        for i in range(1, 9):
            for j in range(10):
                crea_bottone(i, j, gioco, bombe, lista_griglia)
    elif difficulty == "medio":
        for i in range(1, 15):
            for j in range(18):
                crea_bottone(i, j, gioco, bombe, lista_griglia)
    elif difficulty == "difficile":
        for i in range(1, 21):
            for j in range(24):
                crea_bottone(i, j, gioco, bombe, lista_griglia)


creagriglia("")


finestra.mainloop()

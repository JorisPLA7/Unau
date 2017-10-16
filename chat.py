from tkinter import*


fenetre3 = Tk()
fenetre3.wm_title("test chat")
contact = Frame(fenetre3)
contact.pack(side=LEFT)
chat = Frame(fenetre3)
chat.pack(side=BOTTOM)


##conversation
def sel():
    global A,B,C
    test=2
    A="Nickname"
    B=cont2.curselection()
    C=cont[B[0]]
    print(B)
    aa="COUCOU !!!!"
    bb="COUCOUx !!!!"

    if test==1:
        nuser1 = LabelFrame(fenetre3, text=A)
        nuser1.pack()
        tuser1 = Label(nuser1, text=aa)
        tuser1.pack()
    if test==2:
        nuser2 = LabelFrame(fenetre3, text=C)
        nuser2.pack()
        tuser2 = Label(nuser2, text=bb)
        tuser2.pack()


##CONTACT
scrollbar = Scrollbar(contact)
scrollbar.pack( side = RIGHT, fill=Y)
cont2 = Listbox(contact, yscrollcommand = scrollbar.set, height=30, width=30)
cont=['Arthur','Samuel','Joris','a','z','e','r','t','y','u','i','o']

for i in range(len(cont)):
    cont2.insert(END, cont[i])

cont2.pack(side=TOP, fill=Y)
scrollbar.config( command = cont2.yview)

bsel = Button(contact, text ="sélectionner", command = sel, anchor=CENTER, pady=4, height=1, width=16)
bsel.pack(side = BOTTOM, fill=X)

##chat

def envoie():
    global zchat
    aa=zchat.get()
    nuser1 = LabelFrame(fenetre3, text=A)
    nuser1.pack()
    tuser1 = Label(nuser1, text=aa)
    tuser1.pack()
    zchat.destroy()
    zchat = Entry(chat)
    zchat.pack(side=LEFT)


zchat = Entry(chat)
zchat.pack(side=LEFT)

benvoie = Button(chat, text ="Envoyer", command=envoie, anchor=CENTER, pady=4, height=1, width=7)
benvoie.pack(side = RIGHT)



fenetre3.mainloop()
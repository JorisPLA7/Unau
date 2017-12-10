from random import *


class Jeu:
    # ----------------------------------------------Classmethods----------------------------------------------------------

    

    def gameInit(self, nombreJoueurs, nombreCartes):
        """ Fonction qui initialise tout le jeu, le programme peut tourner sans mais il faut alors créer les instances à la main et certaines méthodes ne sont pas disponibles"""

        self.active = 0  # Id du joueur actif
        self.nextPlayer = 1
        self.bin = []  # défausse
        self.deck = Deck  # le deck est un objet aussi
        self.deck.__init__(self.deck)  # pas nécessaire mais il y avait des bugs (je retirerai quand tout sera bien fini)
        self.table = self.pioche()  # carte retournée
        self.nb_joueurs = nombreJoueurs
        self.sens = 1
        self.modificateurs_de_jeu = []
        self.extensions = {}
        while type(self.table) != Carte:  # on retourne des cartes jusqu'à obtenir une carte "normale"
            self.pose(self.pioche())

        self.player = []  # liste des joueurs
        for i in range(nombreJoueurs):
            self.player.append(Joueur(i))
            paquet = self.player[i].main_depart(self)
            self.unpack(paquet)
            
        
    

    def pioche(self):
        carte, status = self.deck.pioche(self.deck, self.bin) #status : nb de carte restantes dans le deck
        if status == 0 :
            self.bin=[]
        return carte

    

    def setNextPlayer(self, nb=1):
        '''nexp = 0 le joueur rejoue
        =1 joueur suivant
        =-1 joueur précédent sans changement de sens

        NON TESTE
        '''
        next = (self.active + self.sens * nb) % self.nb_joueurs
        self.nextPlayer = next
        # print("le joueur suivant sera donc : {} {}".format(self.player[self.nextPlayer].nom,self.player[self.nextPlayer].num))
        return next

    

    def setActive(self):
        act = self.nextPlayer
        self.active = act
        return act

    

    def pose(self, carte):
        self.bin.append(self.table)
        self.table = carte

    def autorisation(self, carte):
        can_play = True
        for i in self.modificateurs_de_jeu:
            can_play = can_play and i[0](carte)
        return can_play

    def applyModifs(self):
        for i in self.modificateurs_de_jeu:
            i[1]()
        self.modificateurs_de_jeu = []

    def unpack(self, data):  # pour récupérer les données, écrire a.unpack(a)
        [self.deck,
         self.active,
         self.nextPlayer,
         self.bin,
         self.table,
         self.player,
         self.nb_joueurs,
         self.sens,
         self.modificateurs_de_jeu,
         self.autoAsk,
         self.extensions] = list(data)

    def getActive(self):  # fonction pas nécessaire mais utile au déboguage
        try:
            return self.active
        except:
            return -1

    

    # ----------------------------------------------Instance--------------------------------------------------------------
    
    def __init__(self, main=False, packet="False", nombreJoueurs=2, nombreCartes=7):

        self.autoAsk = False
        if main: self.gameInit(nombreJoueurs,nombreCartes)
        if packet != "False":
            self.unpack(packet)

    def enregistrer(self):

        data = [self.deck,
            self.active,
            self.nextPlayer,
            self.bin,
            self.table,
            self.player,
            self.nb_joueurs,
            self.sens,
            self.modificateurs_de_jeu,
            self.autoAsk,
            self.extensions
        ]
        return data

    def pack(self):
        self.data = list(self.enregistrer())

        return self.data

    def describe(self):  # si tu es perdu Joris
        dico = self.caracteristics()

        print(self.caracteristics())
        return dico

    def launch(self):
        self.autoAsk = True
        self.routine()

    def routine(self):
        while self.autoAsk == True:

            request = input("Appuyez sur Entrée ou entrez une commande :")
            if request == "stop":
                self.autoAsk = False
            elif len(request) != 0:
                try:
                    exec(request)
                except:
                    print("Erreur.")
            else:
                if self.player[self.active].nom == 'en attente de ' :
                    self.player[self.active].nom = input("Entrez ici votre nom : ")
                self.ask()

    def ask(self):

        self.setNextPlayer(1)
        
        paquet=self.player[self.active].answer(self)
        
        self.unpack(paquet)
        
        self.setActive()
        
        #print("finAsk")
        #print("actif = ", self.active)
        #print("suivant (le meme) = ", self.nextPlayer)


class Deck(Jeu):
    def __init__(self):
        deckInit = [["Cataclysme", "Pouvoir"], ["Cataclysme", "Pouvoir"], ["Benediction", "Pouvoir"],
                    ["Benediction", "Pouvoir"], ["Benediction", "Pouvoir"], ["Benediction", "Pouvoir"],
                    ["Tempete", "Pouvoir"], ["Tempete", "Pouvoir"], ["Tempete", "Pouvoir"], ["Tempete", "Pouvoir"]]
        val = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Salamandre", 1, 2, 3, 4, 5, 6, 7, 8, 9, "Salamandre", "Dragon", "Dragon",
               "Esprit", "Esprit"]
        colors = ["Bambous", "Cascade", "Braises", "Lumière"]
        for i in range(len(val)):
            for j in range(len(colors)):
                deckInit.append([val[i], colors[j]])

        self.deckActive = []
        
        for i in deckInit:
            self.deckActive.append(self.createCard(i))

        shuffle(self.deckActive)

    def createCard(liste):

        if type(liste[0]) == int:
            return Carte(liste)

        if liste[0] == "Salamandre":
            return Salamandre(liste)

        if liste[0] == "Dragon":
            return Dragon(liste)

        if liste[0] == "Esprit":
            return Esprit(liste)

        if liste[0] == "Cataclysme":
            return Cataclysme(liste)

        if liste[0] == "Benediction":
            return Benediction(liste)

        if liste[0] == "Tempete":
            return Tempete(liste)

        

    def reset(self, bin):
        cartes = bin
        
        for i in range(len(cartes)) :
            cartes[i]=createCard(cartes[i].id) # on régénère un deck neuf, sans modification
        shuffle(cartes)
        self.deckActive = cartes

    def pioche(self, bin):
        
        carte = self.deckActive.pop()
        status = len(self.deckActive)
        if status == 0:
            self.reset(bin)
            
        return carte, status

    def caracteristics(self):
        dico = {"nombre de cartes" : len(self.deckActive), "cartes" : self.deckActive}
        return dico


class Carte(Jeu):
    def __init__(self, liste):

        self.id = liste # pour la régénération du deck
        self.val = liste[0]
        self.typ = liste[1]
        self.owner = None # pour des effets spéciaux

    def pose(self, jeu, joueur):
        #modifie le jeu
        #mofifie le joueur
        jeu.pose(self)
        self.setOwner(joueur.num)
        paquet=joueur.pack()
        return jeu, paquet

    def setOwner(self, parent):
        self.owner = parent


    def coveredEffect(self):
        def noEffect(joueur, jeu):
            return joueur.pack(), jeu

        return noEffect

    def compatibTest(self, carte):
        return (self.val == carte.val or self.typ == carte.typ)
        
    def caracteristics(self):
        dico = {"carte": self.id, "owner": self.owner}
        return dico


class Joueur(Jeu):
    hand = []

    def __init__(self, playNumb, Username='en attente de '):
        self.num = playNumb
        self.nom = Username
        

        self.StartMethodList = []
        
        self.restrictions = []
        
    def main_depart(self, jeu):
        self.hand = [jeu.pioche() for i in range(7)]
        return jeu.pack()
        
    def answer(self, jeu):
        input("C'est à {} {} de jouer !".format(self.nom, self.num))

        for i in self.StartMethodList:  # effets de début de tour
                paquet, jeu = i(self, jeu)

        print("La carte posée est | ~ {} de {} ~ |".format(jeu.table.val, jeu.table.typ))
        print("Voici vos cartes : ")
        for i in range(len(self.hand)):
            print("| {} : ~ {} de {} ~ |".format(i, self.hand[i].val, self.hand[i].typ))
        print()
        if not self.peutJouer(jeu):
            jeu = self.pioche(jeu)
            print("Vous piochez : | {} : ~ {} de {} ~ |".format(len(self.hand) - 1, self.hand[len(self.hand) - 1].val,
                                                                self.hand[len(self.hand) - 1].typ))

        if not self.peutJouer(jeu):
            print("Vous ne pouvez pas jouer.")
            
        else:
            indice = input("Quelle carte poser ? ")
            try:
                indice = int(indice)
            except:
                while type(indice) != int:
                    indice = input("Il faudrait songer à entrer le numéro correspondant : ")
                    try:
                        indice = int(indice)
                    except:
                        pass

            while self.playable(indice, jeu) == False:
                indice = input("Vous ne pouvez pas jouer ça. Essayez encore : ")
                try:
                    indice = int(indice)
                except:
                    while type(indice) != int:
                        indice = input("Il faudrait songer à entrer le numéro correspondant : ")
                        try:
                            indice = int(indice)
                        except:
                            pass
            jeu = self.pose(indice, jeu)
            
        paquet=self.endTurn(jeu)
        return paquet

    def endTurn(self, jeu):
        #modifie le jeu
        if len(self.hand) == 0:
            self.setVictory()
        if jeu.nextPlayer != self.num:
            print("C'est la fin de votre tour.")
        print()
        self.clearLists()
        paquet=jeu.pack()
        return paquet

    def setVictory(self):
        pass

    def pioche(self, jeu):
        #modifie le jeu
        self.hand.append(jeu.pioche())
        return jeu

    

    def clearLists(self):
        self.StartMethodList = []
        
        self.restrictions = []

    def peutJouer(self, jeu):  # renvoie vraie si la main du joueur contient au moins une carte jouable
        Canplay = False
        for i in self.hand:
            Canplay = (Canplay or self.verify(i, jeu))
        return Canplay

    def verify(self, carte, jeu):  # détermine si une carte est jouable en prenant en compte les restricions imposées par...

        canPlay = True
        # canPlay=(canPlay and jeu.autorisation(carte) )#les modificateurs de jeu en cours
        canPlay = (canPlay and carte.compatibTest(jeu.table))  # la carte elle-même
        for i in self.restrictions:  # les diverses restrictions supplémentaires du joueur
            if i(self, carte, jeu) == "ByPass":  # "code spécial" pour éviter toutes les restricions
                canPlay = True
                return canPlay

            else:
                canPlay = canPlay and i(self, carte, jeu)

        return canPlay

    def playable(self, cardId, jeu):
        
        if cardId < 0:
            cardId = 0
        if cardId >= len(self.hand):
            cardId = len(self.hand) - 1
        return self.verify(self.hand[cardId], jeu)
        
    def enregistrer(self):

        data = [
            self.num, 
            self.nom, 
            self.hand,
            self.StartMethodList,
            
            self.restrictions
        ]
        return data
        
    def unpack(self, data):

        [self.num, 
        self.nom, 
        self.hand,
        self.StartMethodList,
        
        self.restrictions] = list(data)
    
    def pack(self) :
        self.data=self.enregistrer()
        return self.data
    
    def pose(self, cardId, jeu):
        #modifie le jeu
        carte = self.hand.pop(cardId)
        jeu, paquet = carte.pose(jeu, self)
        self.unpack(paquet)
        
        return jeu

    def caracteristics(self):
        dico = {"Joueur": [self.num, self.nom], "nombre de carte": len(self.hand)}
        return dico


class Special(Carte):
    '''carte de nous
    '''

    def __init__(self, liste):
        Carte.__init__(self, liste)

    def pose(self, jeu, joueur):
        self.typ = jeu.table.typ
        #modifie le jeu
        #mofifie le joueur
        jeu.pose(self)
        self.setOwner(joueur.num)
        paquet=joueur.pack()
        return jeu, paquet

class Salamandre(Carte):
    ''' equivalent carte +2
    '''

    def __init__(self, liste):
        Carte.__init__(self, liste)
        
    def pose(self, jeu, joueur):
        #modifie le jeu
        #mofifie le joueur
        jeu.pose(self)
        self.setOwner(joueur.num)
        
        paquet, jeu = self.poseEffect(jeu)
        
        return jeu, paquet
        
    def poseEffect(self, jeu):

    
        #print("Y'a comme un Lézard...")  # déboguage... ça marche !!!!!!!!!!!
        nextPlayer = (jeu.active + jeu.sens) % jeu.nb_joueurs

        
        if "counter" in jeu.extensions :
            jeu.extensions["counter"] += 2
            #print("Lézard + 2 !!")
        else :
            #print("Traitement du Lézard")
            jeu.extensions["counter"] = 2

        can_play = False
        for i in jeu.player[nextPlayer].hand:
            can_play = (can_play or i.val == "Salamandre")

        if not can_play:
            print("C'est parti pour piocher !")
            for i in range(jeu.extensions["counter"]):
                jeu = jeu.player[nextPlayer].pioche(jeu)
                print(
                    "{} {} pioche !".format(jeu.player[nextPlayer].nom,jeu.player[nextPlayer].num))  # les prints c'est pour pouvoir suivre
            jeu.extensions["counter"] = 0
            jeu.setNextPlayer(2)

        else:
            print("il parait que tu peux jouer dis donc !")
            def restriction(joueur, carte, jeu):
                return jeu.table.val == carte.val
            jeu.player[nextPlayer].restrictions.append(restriction)
            
        return joueur.pack(), jeu

        


class Dragon(Carte):
    ''' equivalent carte 'No'
    '''

    def __init__(self, liste):
        Carte.__init__(self, liste)

    def poseEffect(self, jeu):

        jeu.setNextPlayer(2)
        return joueur.pack(), jeu

    def pose(self, jeu, joueur):
        #modifie le jeu
        #mofifie le joueur
        jeu.pose(self)
        self.setOwner(joueur.num)
        
        paquet, jeu = self.poseEffect(jeu)
        
        return jeu, paquet

class Esprit(Carte):
    ''' equivalent changement de sens 'sens'
    '''

    def __init__(self, liste):
        Carte.__init__(self, liste)

    def poseEffect(self):
        
        jeu.sens = jeu.sens * (-1)
        jeu.setNextPlayer(1)
        return joueur.pack(), jeu

    def pose(self, jeu, joueur):
        #modifie le jeu
        #mofifie le joueur
        jeu.pose(self)
        self.setOwner(joueur.num)
        
        paquet, jeu = self.poseEffect()
        
        return jeu, paquet


class Cataclysme(Special):
    def __init__(self, liste):
        Carte.__init__(self, liste)

    def compatibTest(self, carte):
        if type(carte.val) == str and str(carte.val) != "Dragon":
            return False
        elif type(carte.val) == str and str(carte.val) == "Dragon":
            return True
        elif carte.val == 0:
            return True
        return False


class Tempete(Special):
    def __init__(self, liste):
        liste[0] = "Tempête"
        Carte.__init__(self, liste)

    def compatibTest(self, carte):
        if type(carte.val) == str and str(carte.val) != "Esprit":
            return False
        elif type(carte.val) == str and str(carte.val) == "Esprit":
            return True
        elif carte.val < 5:
            return True
        return False


class Benediction(Special):
    def __init__(self, liste):
        liste[0] = "Bénédiction"
        Carte.__init__(self, liste)

    def compatibTest(self, carte):
        if type(carte.val) == str:
            return False
        elif carte.val > 7:
            return True
        return False


def login():
    '''Fct de démonstration et de test.
    Par Joris Placette
    '''
    host = "127.0.0.1"
    port = 8082
    print("Saisir 'q' pour obtenir un terminal de commande")
    nickname = str(input("saisir un pseudo (inferieur à 10 caractères):  "))
    password = "lol ;')"
    global MyNet
    MyNet = Net(host, port, nickname, password)

    MyNet.Identify()  # séquence d'identification
    if MyNet.Connected == True:
        print("Vous êtes connecté en tant que {}".format(MyNet.WhoAmI()))
        print("Pour envoyer les données taper 'network.Transmit(données)' ")
    else:
        print("Vous n'êtes pas connecté")


if __name__ == '__main__':
    global a
    a = Jeu(True)
    # login()

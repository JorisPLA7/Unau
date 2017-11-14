from random import *
import sys


class Jeu :




    #----------------------------------------------Classmethods----------------------------------------------------------

    def getUsernames(cls): #voir avec le serveur
        pass


    def classInit (cls, nombreJoueurs):
        """ Fonction qui initialise tout le jeu, le programme peut tourner sans
        mais il faut alors créer les instances à la main et certaines méthodes
        ne sont pas disponibles"""

        cls.active=0 # Id du joueur actif
        cls.nextPlayer=1
        cls.bin=[] #défausse
        cls.deck=Deck # le deck est un objet aussi
        cls.deck.__init__(cls.deck) # pas nécessaire mais il y avait des bugs (je retirerai quand tout sera bien fini)
        cls.table=cls.pioche() #carte retournée
        while type(cls.table)!=Carte : # on retourne des cartes jusqu'à obtenir une carte "normale"
            cls.pose(cls.pioche())

        cls.player=[Joueur(i) for i in range(nombreJoueurs)] #liste des joueurs
        cls.nb_joueurs=nombreJoueurs
        cls.sens=1
        cls.modificateurs_de_jeu=[]
        cls.toggleNext=False #si le joueur suivant a déja été determiné , alors toogleNext = True et la fct setNextPlayer n'est pas appelée de nouveau
        # on le RAZ à chaque nv joueur
    classInit=classmethod(classInit) #diffuse cette méthode sur l'ensemble des objets de cette classe ainsi que les sous-classes (n'importe quelle instance (même une carte) peut donc modifier les propriétés du Jeu)

    def pioche(cls):
        return cls.deck.pioche(cls.deck)

    pioche=classmethod(pioche)

    def setNextPlayer(cls,nb=1):
        '''nexp = 0 le joueur rejoue
        =1 joueur suivant
        =-1 joueur précédent sans changement de sens

        NON TESTE
        '''
        cls.nextPlayer=(cls.active+cls.sens*nb)%cls.nb_joueurs
        print("le joueur suivant sera donc : {} {}".format(cls.player[cls.nextPlayer].nom,cls.player[cls.nextPlayer].num))
        cls.toggleNext=True

    setNextPlayer=classmethod(setNextPlayer)

    def pose(cls,carte):
        cls.bin.append(cls.table)
        cls.table=carte

    pose=classmethod(pose)

    def autorisation(cls, carte):
        can_play=True
        for i in cls.modificateurs_de_jeu :
            can_play= can_play and i[0]()
        return can_play


    def applyModifs(cls):
        for i in modificateurs_de_jeu :
            i[1]()
        cls.modificateurs_de_jeu=[]

    autorisation=classmethod(autorisation)





    def getActive(cls): #fonction pas nécessaire mais utile au déboguage
        try :
            return cls.active
        except :
            return -1
    getActive=classmethod(getActive)

    #----------------------------------------------Instance--------------------------------------------------------------
    def __init__(self, main=False, nbPl =4 ):

        self.autoAsk=False
        if main : Jeu.classInit(nbPl)

    def caracteristics(self) :
        dico={}
        return dico

    def describe(self): # si tu es perdu Joris
        dico=self.caracteristics()

        print(self.caracteristics())

    def launch(self):
        self.autoAsk=True
        self.routine()

    def routine(self):
        while self.autoAsk == True :

            request=input("Appuyez sur Entrée ou entrez une commande :")
            if len(request)!=0 :
                try :
                    exec(request)
                except :
                    print("Erreur.")
            else :
                self.ask()


    def ask(self):
        self.setNextPlayer()
        self.player[self.active].answer()
        self.toggleNext=False
        self.active=self.nextPlayer



class Deck(Jeu):
    def __init__(self):
        deckInit=[["sp",0] , ["sp",0]  , ["sp",0]  , ["sp",0]  , ["sp+",0] , ["sp+",0] , ["sp+",0] , ["sp+",0], ["sp++",0] , ["sp+",0] , ["sp++",0] , ["sp++",0] ]
        val=[0,1,2,3,4,5,6,7,8,9,"Salamandre",1,2,3,4,5,6,7,8,9,"Salamandre","Dragon","Dragon","Esprit","Esprit"]
        colors=["Bambous","Cascade","Braises","Lumière"]
        for i in range(len(val)):
            for j in range(len(colors)):
                deckInit.append([val[i],colors[j]])

        self.deckActive=[]
        for i in deckInit :
            self.deckActive.append(self.createCard(i))

        shuffle(self.deckActive)

    def createCard(liste):
        if liste[1] == 0 :
            return Special(liste)

        if type(liste[0]) == int :
            return Carte(liste)

        if liste[0] == "Salamandre" :
            return Salamandre(liste)

        if liste[0] == "Dragon" :
            return Dragon(liste)

        if liste[0] == "Esprit" :
            return Esprit(liste)

        else :
            return exec("{}(liste)".format(liste[0])) # dans le cas d'un apport extérieur d'une nouvelle classe


    def reset(self):
        cartes=Jeu.bin
        Jeu.bin=[]
        shuffle(cartes)
        self.deckActive=cartes

    def pioche(self):

        carte = self.deckActive.pop()
        if len(self.deckActive)==0:
            self.reset()
        return carte

    def caracteristics(self) :
        dico={}
        return dico

class Carte(Jeu):
    def __init__(self,liste):

        self.id=liste
        self.val=liste[0]
        self.typ=liste[1]
        self.owner= None



    def pose(self, parent=Jeu.getActive()):
        Jeu.pose(self)
        Jeu.player[parent].EndMethodList.append(self.poseEffect())
        self.setOwner(parent)



    def setOwner(self,parent) :
        self.owner=parent

    def poseEffect(self):
        def noEffect(cls) :
            pass

        return noEffect

    def coveredEffect(self):
        def noEffect(cls) :
            pass

        return noEffect

    def compatibTest(self, carte):
        if not (self.val ==carte.val or self.typ==carte.typ) :
            return False
        return True

    def caracteristics(self) :
        dico={"carte":self.id, "owner":self.owner}
        return dico

class Joueur(Jeu):
    hand=[]
    def __init__(self,playNumb,Username='Joueur'):
        self.num=playNumb
        self.nom=Username
        self.hand=[Jeu.pioche() for i in range(7)]

        self.StartMethodList=[]
        self.EndMethodList=[]
        self.restrictions=[]


    def answer(self):
        input("C'est à {} {} de jouer !".format(self.nom,self.num))
        print("La carte posée est | ~ {} de {} ~ |".format(Jeu.table.val,Jeu.table.typ))
        print("Voici vos cartes : ")
        for i in range(len(self.hand)) :
            print("| {} : ~ {} de {} ~ |".format(i,self.hand[i].val,self.hand[i].typ))
        print()
        if not self.peutJouer() :

            self.pioche()
            print ("Vous piochez : | {} : ~ {} de {} ~ |".format(len(hand)-1,self.hand[len(hand)-1].val,self.hand[len(hand)-1].typ))

        if not self.peutJouer() :
            self.endTurn()
        else :
            indice=input("Quelle carte poser ? ")
            try :
                indice=int(indice)
            except :
                while type(indice)!=int :
                    indice=input("Il faudrait songer à entrer le numéro correspondant : ")
                    try :
                        indice=int(indice)
                    except :
                        pass

            while(indice<0 or indice>=len(self.hand)) or self.play(indice)==False :
                indice=input("Vous ne pouvez pas jouer ça. Essayez encore : ")
                try :
                    indice=int(indice)
                except :
                    while type(indice)!=int :
                        indice=input("Il faudrait songer à entrer le numéro correspondant : ")
                        try :
                            indice=int(indice)
                        except :
                            pass
        self.endTurn()

    def endTurn(self):
        if Jeu.nextPlayer != self.num :
            print("C'est la fin de votre tour.")
        print()
        self.clearLists()



    def pioche(self) :
        self.hand.append(Jeu.pioche())

    def turnEffects(fonction):
        def effectuer_actions(self, arg2):
            for i in self.StartMethodList :
                if type(i) == classmethod :
                    i(self)
                else :
                    i(self)
            fonction(self, arg2)
            for i in self.EndMethodList :
                if type(i) == classmethod :
                    Jeu.i()
                else :
                    i(self)

        return effectuer_actions

    def clearLists(self):
        self.StartMethodList=[]
        self.EndMethodList=[]
        self.restrictions=[]

    def peutJouer(self): #renvoie vraie si la main du joueur contient au moins une carte jouable
        Canplay=False
        for i in self.hand:
            Canplay = (Canplay or self.verify(i))
        return Canplay

    def verify(self, carte): #détermine si une carte est jouable en prenant en compte les restricions imposées par...

        canPlay=True
        canPlay=(canPlay and Jeu.autorisation(carte) )#les modificateurs de jeu en cours
        canPlay=(canPlay and carte.compatibTest(Jeu.table) )#la carte elle-même
        for i in self.restrictions : #les diverses restrictions supplémentaires du joueur
            canPlay=canPlay and i(carte)
        return canPlay


    def play(self, cardId):
        if cardId<0 :
            cardId=0
        if cardId>=len(self.hand) :
            cardId=len(self.hand)-1
        if self.verify(self.hand[cardId]) :
            self.pose(cardId)
            return True
        else :
            return False

    @turnEffects
    def pose(self, cardId):
        carte = self.hand.pop(cardId)
        carte.pose(self.num)

    def caracteristics(self) :
        dico={"Joueur":[self.num,self.nom], "nombre de carte":len(self.hand)}
        return dico



class Special(Carte):
    '''carte de nous
    '''
    def __init__(self, liste):
        liste[1]="SpecialPower"
        Carte.__init__(self,liste)

    def compatibTest(self, carte):
        return True

class Salamandre(Carte):
    ''' equivalent carte +2
    '''

    def __init__(self, liste):
        Carte.__init__(self,liste)

    def poseEffect(self):

        def piocheur(cls):
            print("Y'a comme un Lézard...")  # déboguage... ça marche !!!!!!!!!!!
            nextPlayer=(Jeu.nextPlayer + Jeu.sens)%cls.nb_joueurs

            try :

                Jeu.counter +=2
                print("Lézard + 2 !!")
            except :
                print("Traitement du Lézard")
                Jeu.counter = 2

            can_play=False
            for i in Jeu.player[nextPlayer].hand :
                can_play=(can_play or i.typ == "Salamandre")

            if not can_play :
                print("C'est parti pour piocher !")
                for i in range(Jeu.counter):
                    Jeu.player[nextPlayer].pioche()
                    print("Joueur {} pioche !".format(Jeu.player[nextPlayer].num)) #les prints c'est pour pouvoir suivre
                Jeu.counter = 0
                Jeu.setNextPlayer(2)

            else :
                print("il parait que tu peux jouer dis donc !")
                def restriction(self, carte):
                    if Jeu.table.val!=carte.val :
                        return False
                Jeu.player[nextPlayer].restrictions.append(restriction)





        return piocheur



class Dragon(Carte):
    ''' equivalent carte 'No'
    '''
    def __init__(self, liste):
        Carte.__init__(self,liste)

    def poseEffect(self):
        def saut(cls):
            Jeu.setNextPlayer(2)

        return saut


class Esprit(Carte):
    ''' equivalent changement de sens 'sens'
    '''
    def __init__(self, liste):
        Carte.__init__(self,liste)

    def poseEffect(self):
        def changementSens(cls):
            Jeu.sens = Jeu.sens*(-1)

        return changementSens

if __name__ == '__main__':
    monjeu  = Jeu(True)
    monjeu.launch()

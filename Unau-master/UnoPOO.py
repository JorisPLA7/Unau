from random import *
import sys


class Jeu :


    #----------------------------------------------Classmethods----------------------------------------------------------

    def getUsernames(cls): #voir avec le serveur
        pass


    def classInit (cls, nombreJoueurs):
        """ Fonction qui initialise tout le jeu, le programme peut tourner sans mais il faut alors créer les instances à la main et certaines méthodes ne sont pas disponibles"""

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
        
    classInit=classmethod(classInit) #diffuse cette méthode sur l'ensemble des objets de cette classe ainsi que les sous-classes (n'importe quelle instance (même une carte) peut donc modifier les propriétés du Jeu)

    def pioche(cls):
        return cls.deck.pioche(cls.deck)

    pioche=classmethod(pioche)

    def setNext(self,nb=1):
        '''nexp = 0 le joueur rejoue
        =1 joueur suivant
        =-1 joueur précédent sans changement de sens

        NON TESTE
        '''
        next=(self.active+self.sens*nb)%self.nb_joueurs
        self.nextPlayer=next
        #print("le joueur suivant sera donc : {} {}".format(cls.player[cls.nextPlayer].nom,cls.player[cls.nextPlayer].num))
        return next


    def setNextPlayer(self, nb=1):
        self.nextPlayer=self.setNext(nb)


    def setAct(self):
        act=self.nextPlayer
        self.active=act
        return act
    

    def setActive(self):
        self.active=self.setAct()

      
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
        for i in cls.modificateurs_de_jeu :
            i[1]()
        cls.modificateurs_de_jeu=[]

    autorisation=classmethod(autorisation)


    def unpack(cls, data): #pour récupérer les données, écrire a.unpack(a)
      [cls.active,
          cls.nextPlayer,
          cls.bin,
          cls.table,
          cls.player,
          cls.nb_joueurs,
          cls.sens,
          cls.modificateurs_de_jeu,
          cls.autoAsk] = list(data)
      
        
    

    def getActive(cls): #fonction pas nécessaire mais utile au déboguage
        try :
            return cls.active
        except :
            return -1
    getActive=classmethod(getActive)

    #----------------------------------------------Instance--------------------------------------------------------------
    def __init__(self, main=False, packet="False", nbPl =4):

        self.autoAsk=False
        if main : Jeu.classInit(nbPl)
        if packet!="False":
            self.unpack(packet)

        
    def enregistrer(self) : 
        
        data= [
          self.active,
          self.nextPlayer,
          self.bin,
          self.table,
          self.player,
          self.nb_joueurs,
          self.sens,
          self.modificateurs_de_jeu,
          self.autoAsk
                ]
        return data
        
    def pack(self):
      self.data=list(self.enregistrer())
      
      return self.data
      
    def describe(self): # si tu es perdu Joris
        dico=self.caracteristics()
        
        print(self.caracteristics())
        return dico
    
    def launch(self):
        self.autoAsk=True
        self.routine()
        
    def routine(self):
        while self.autoAsk == True :
            
            request=input("Appuyez sur Entrée ou entrez une commande :")
            if request=="stop":
              self.autoAsk = False
            elif len(request)!=0 :
                try :
                    exec(request)
                except :
                    print("Erreur.")
            else :
                self.ask()
                
    
    def ask(self):
        
        self.setNextPlayer(1)
        #self.nextPlayer = (self.active + self.sens * 1) % self.nb_joueurs
        self.player[self.active].answer()
        self.setActive()
        #self.active=self.nextPlayer
        print("finAsk")
        print("actif = ", self.active)
        print("suivant (le meme) = ", self.nextPlayer)






class Deck(Jeu):
    def __init__(self):
        deckInit=[["Cataclysme","Pouvoir"] , ["Cataclysme","Pouvoir"]  , ["Benediction","Pouvoir"] , ["Benediction","Pouvoir"] , ["Benediction","Pouvoir"] , ["Benediction","Pouvoir"], ["Tempete","Pouvoir"] , ["Tempete","Pouvoir"] , ["Tempete","Pouvoir"] , ["Tempete","Pouvoir"] ]
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
        
        if type(liste[0]) == int :
            return Carte(liste)

        if liste[0] == "Salamandre" :
            return Salamandre(liste)

        if liste[0] == "Dragon" :
            return Dragon(liste)

        if liste[0] == "Esprit" :
            return Esprit(liste)
            
        if liste[0] == "Cataclysme" :
            return Cataclysme(liste)
        
        if liste[0] == "Benediction" :
            return Benediction(liste)
            
        if liste[0] == "Tempete" :
            return Tempete(liste)
        
        """      
                else :
                    carte=None
                    exec("carte = {}([0,0])".format("Cataclysme") )# dans le cas d'un apport d'une nouvelle classe
                    print(carte)
                    return carte
        """     
        #NE FONCTIONNE QUE DANS LA SHELL

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
        for i in self.poseEffect():
            Jeu.player[parent].PoseMethodList.append(i)
        self.setOwner(parent)



    def setOwner(self,parent) :
        self.owner=parent

    def poseEffect(self):
        def noEffect(cls) :
            pass

        return [noEffect]

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
    def __init__(self,playNumb,Username='en attente de '):
        self.num=playNumb
        self.nom=Username
        self.hand=[Jeu.pioche() for i in range(7)]

        self.StartMethodList = []
        self.PoseMethodList=[]
        self.restrictions=[]
    
    
    def answer(self):
        input("C'est à {} {} de jouer !".format(self.nom,self.num))
        
        for i in self.StartMethodList : #effets de début de tour
            if type(i) == classmethod :
                self.i(self)
            else :
                i(self)
                
                
        print("La carte posée est | ~ {} de {} ~ |".format(Jeu.table.val,Jeu.table.typ))
        print("Voici vos cartes : ")
        for i in range(len(self.hand)) :
            print("| {} : ~ {} de {} ~ |".format(i,self.hand[i].val,self.hand[i].typ))
        print()
        if not self.peutJouer() :
            
            self.pioche()
            print ("Vous piochez : | {} : ~ {} de {} ~ |".format(len(self.hand)-1,self.hand[len(self.hand)-1].val,self.hand[len(self.hand)-1].typ))
            
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
        if len(self.hand)== 0 :
            self.setVictory()
        if Jeu.nextPlayer != self.num :
            print("C'est la fin de votre tour.")
        print()
        self.clearLists()
        
    def setVictory(self):
        pass
        
        
    def pioche(self) :
        self.hand.append(Jeu.pioche())

    def turnEffects(fonction):
        def effectuer_actions(self, arg2):
           
            fonction(self, arg2)
            for i in self.PoseMethodList :
                if type(i) == classmethod :
                    self.i(self)
                else :
                    i(self)
            
        return effectuer_actions

    def clearLists(self):
        self.StartMethodList=[]
        self.PoseMethodList=[]
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
            if i(carte)=="ByPass" : #"code spécial" pour éviter toutes les restricions
              canPlay=True
              return canPlay
            
            else :
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
        Carte.__init__(self,liste)
    
    def pose(self, parent=Jeu.getActive()):
        self.typ=Jeu.table.typ
        Jeu.pose(self)
        for i in self.poseEffect():
            Jeu.player[parent].PoseMethodList.append(i)
        self.setOwner(parent)
    

class Salamandre(Carte):
    ''' equivalent carte +2
    '''

    def __init__(self, liste):
        Carte.__init__(self,liste)

    def poseEffect(self):

        def piocheur(self):
            #print("Y'a comme un Lézard...")  # déboguage... ça marche !!!!!!!!!!!
            nextPlayer=(Jeu.active + Jeu.sens)%self.nb_joueurs

            try :

                Jeu.counter +=2
                #print("Lézard + 2 !!")
            except :
                #print("Traitement du Lézard")
                Jeu.counter = 2

            can_play=False
            for i in Jeu.player[nextPlayer].hand :
                can_play=(can_play or i.typ == "Salamandre")

            if not can_play :
                #print("C'est parti pour piocher !")
                for i in range(Jeu.counter):
                    Jeu.player[nextPlayer].pioche()
                    print("Joueur {} pioche !".format(Jeu.player[nextPlayer].num)) #les prints c'est pour pouvoir suivre
                Jeu.counter = 0
                Jeu.setNextPlayer(2)

            else :
                #print("il parait que tu peux jouer dis donc !")
                def restriction(self, carte):
                    if Jeu.table.val!=carte.val :
                        return False
                Jeu.player[nextPlayer].restrictions.append(restriction)





        return [piocheur]



class Dragon(Carte):
    ''' equivalent carte 'No'
    '''
    def __init__(self, liste):
        Carte.__init__(self,liste)

    def poseEffect(self):
        def saut(self):
            Jeu.setNextPlayer(2)

        return [saut]


class Esprit(Carte):
    ''' equivalent changement de sens 'sens'
    '''
    def __init__(self, liste):
        Carte.__init__(self,liste)

    def poseEffect(self):
        def changementSens(self):
            Jeu.sens = Jeu.sens*(-1)
            Jeu.setNextPlayer(1)

        return [changementSens]

class Cataclysme(Special):
    def __init__(self, liste):
        Carte.__init__(self,liste)
    
    def compatibTest(self, carte):
        if type(carte.val)==str and str(carte.val)!="Dragon":
            return False
        elif type(carte.val)==str and str(carte.val)=="Dragon":
            return True
        elif carte.val==0:
            return True
        return False
        

class Tempete (Special):
    def __init__(self, liste):
        liste[0]="Tempête"
        Carte.__init__(self,liste)
    
    def compatibTest(self, carte):
        if type(carte.val)==str and str(carte.val)!="Esprit":
            return False
        elif type(carte.val)==str and str(carte.val)=="Esprit":
            return True
        elif carte.val<5:
            return True
        return False
        
class Benediction (Special):
    def __init__(self, liste):
        liste[0]="Bénédiction"
        Carte.__init__(self,liste)
    
    def compatibTest(self, carte):
        if type(carte.val)==str:
            return False
        elif carte.val>7:
            return True
        return False




def login():
    '''Fct de démonstration et de test.
    Par Joris Placette
    '''
    host ="127.0.0.1"
    port = 8082
    print("Saisir 'q' pour obtenir un terminal de commande")
    nickname = str(input("saisir un pseudo (inferieur à 10 caractères):  "))
    password = "lol ;')"
    global MyNet
    MyNet = Net(host, port, nickname, password)

    MyNet.Identify() #séquence d'identification
    if MyNet.Connected == True :
        print("Vous êtes connecté en tant que {}".format(MyNet.WhoAmI()))
        print("Pour envoyer les données taper 'network.Transmit(données)' ")
    else:
        print("Vous n'êtes pas connecté")
if __name__=='__main__':
    global a
    a=Jeu(True)
    #login()
 

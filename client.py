# -∗- coding: utf-8 -∗-


try :
    import socket
    print("Bibliothèque socket importée avec succès !")
except:
    print("Impossible d'importer la bibliothèque socket !")
try :
    import threading
    print("Bibliothèque threading importée avec succès !")
except:
    print("Impossible d'importer la bibliothèque threading !")
try :
    import time
    print("Bibliothèque time importée avec succès !")
except:
    print("Impossible d'importer la bibliothèque time !")

class NetThread (threading.Thread) :
    '''Classe-Thread chargé de l'envoi & récéption de donnée via le socket une fois le client identifié.
    Elle s'occupe de la partie "veille" de la classe Net.

    N'est pas concue pour être manipulée par Mes camarades.

    Voir l' help(Net())

    Par Joris Placette
    '''
    def __init__(self):
        threading.Thread.__init__(self) #séquence init du thread
        self.Message = []
        self.thereIsSomeNewData = False # désolé pour la longueur du nom de cette variable je n'ai pas trouvé mieux
    def __RequestTreatment(self, Request):
        Flow(Request) #extraction des données pour qu'elles soient récupérées par Arthur

    def run(self):

        while 1:
            if len(self.Message) >= 1: #si un message a été ajouté depuis la dernière fois
                data = self.Message.pop()
                Sock.sendall(data.encode()) #envoi du message ss forme de bytecode


            try :
                data = Sock.recv(1024).decode() #attente d'une reponse pdt 2sec en cas de timeout retourne une erreur, d'ou le try & except
                self.thereIsSomeNewData = True
            except:
                pass #en cas de time-out on passe simplement à la suite
            if self.thereIsSomeNewData:
                self.__RequestTreatment(data)#J'ai sorti la fonction du try; pour rendre le débuggage possible
            self.thereIsSomeNewData = False

class Net ():
    '''Classe interactive (API) pour mes camarades, se charge de mettre en forme les interactions client-serveurr pour une utilisation simplifiée des fonctionnallités socket.

    Par Joris Placette
    '''
    def __init__(self,Host, Port, Nickname, Pass):

        global Sock #devra être accessible dans toutes les classes
        Sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # on cree notre socket
        Sock.settimeout(1.0) #timeout crucial pour que le serv abandonne l'écoute toute les 2 secondes pour transmettre le(s) message(s)

        self.Host = socket.gethostbyname(Host) #récupération de l'adresse auprès des DNS par défaut si nom de domaine fourni
        self.Port = Port
        self.Nickname = Nickname #La Gui indique Pseudo au lieu de Nickname, doit mesurer 10 charactères ou moins
        self.NickLen = str(len(self.Nickname))  #calcul de la longueur du Pseudonyme
        self.Pass = Pass #le pas ne sert pas durant la phase d'identification du client, j'ai cependant implanté cette variable si mes camarades en ont besoin
        self.Connected = False
        self.__NetThread = NetThread()
        self.__NetThread.start() #Démarrage du thread chargé d'éccouter et de shipper les messages

    def Identify(self):
        '''Envoie une requette d'identification.
        Necessaire coté serveur c'est la première chose à faire après avoir initialisé Net.

        Par Joris Placette
        '''
        data = bytes("IDTF" + self.NickLen + self.Nickname, 'utf8') #on crée la chaine d'info d'identification comme "IDTF7exemple"

        try:
            Sock.connect((self.Host,self.Port)) # on se connecte sur le serveur avec les informations données
            print("Connection avec le serveur...")
            Sock.sendall(data)
            print("Identification auprès du serveur...")
            time.sleep(1) #afin de donner le temps au serv d'être en écoute

            self.Connected = True #la connexion a été établie, MAJ du status

        except:
            print("Impossible de se connecter au serveur !")
            self.Connected = False

    def Connected(self):
        '''Affiche le statut du client vis à vis du serveur

        Par Joris Placette
        '''
        return self.Connected

    def Disconnect(self):
        '''Force la fermeture de la connexion, rends impossible l'entrée et la sortie de données.

        Par Joris Placette
        '''
        Sock.close() # rends impossible l'entrée et la sortie de données.
        print("Disconnected")

    def Transmit(self,typed):
        '''Permet de transmettre une chaine de caractères brute au serveur.

        /!\ : Pour le moment les messages sont transmis toute les 2sec et non empillés, donc en cas de spam des messages seront perdus :/

        /!\ : Version DEV :
            Svp pay attention :) !
            Si la Chaine est reconnue comme une ligne de code python alors elle est EXECUTEE.

        Par Joris Placette
        '''
        self.__NetThread.Message.append(typed) #transmett la chaine au thread, on n'execute pas de fonction sinon il faut attentdre la fin de celle-ci , on se contente donc de transmettre la donnée.

    def WhoAmI(self):
        '''Renvoie le Pseudonyme déclaré au serveur lors de l'__init__()

        Par Joris Placette
        '''
        return self.Nickname
global Flow
def Flow(Request):
    '''Cette fonction est appelée à chaque fois que des données sont recues.
    Le traitement de ces données est une simple démonstration.
    Cette fonction permettra à Arthur de recevoir et traiter les données émises par les clients.

    Par Joris Placette
    '''
    print(Request)

    # variableQuiVautCeQueSamuelAEnvoye = Request
    # tu peux convertir fastoche avec int(Request) ou tuple(Request) par exemple
def debug():
    '''Saisir du code en cours de route, ça peut toujours servir... :)

    Par Joris Placette
    '''
    print("Fonction de débuggage...")
    while 1 :

        try :
            exec(input(">>>")) #sorte d'invite de commande en cas de lancement interactif sur le serveur
        except:
            pass


def login():
    '''Fct de démonstration et de test.
    c'est un cadeau pour toi Arth <3 ^^

    Par Joris Placette
    '''
    Host = "0"
    if Host == "0":
            Host ="127.0.0.1"
    Port = 8082
    print("Saisir 'q' pour obtenir un terminal de commande")
    Nickname = str(input("saisir un pseudo (inferieur à 10 caractères):  "))
    if Nickname == 'q':
        debug()
    Pass = "lol ;')"

    global MyNet
    MyNet = Net(Host, Port , Nickname, Pass)

    MyNet.Identify() #séquence d'identification
    if MyNet.Connected == True :
        print("Vous êtes connecté en tant que {}".format(MyNet.WhoAmI()))
        while True:
            Typed = input(">")
            MyNet.Transmit(Typed)

if __name__ == '__main__':
    login() # ce fichier sera peut-être une librairie, il faut donc empêcher l'inclusion du login si appelée par un autre fichier.

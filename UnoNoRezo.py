# -∗- coding: utf-8 -∗-
import socket
import threading
import UnoPOO
import time
import pickle

#---------------------UNO Local---------------------------

def getNetworkInfos():
    '''Fct de démonstration et de test.
    Par Joris Placette
    '''
    host = "127.0.0.1"
    port = 8082
    print("Saisir 'q' pour obtenir un terminal de commande")
    nickname = str(input("saisir un pseudo (inferieur à 10 caractères):  "))

    password = "lol ;')"

    return (host, port, nickname, password)

def getLocalID():
    id = int(input('saisir id client local entre 0 et 1 :  '))
    return id



'''
    def run(self):

        while 1:
            if len(self.Message) >= 1: #si un message a été ajouté depuis la dernière fois
                data = self.Message.pop()
                dataP = pickle.dumps(data)
                print('pickled!')
                Sock.sendall(dataP) #envoi du message ss forme de bytecode
                print('data sent!')
                #conn, addr = s.accept()

            try :
                data = Sock.recv(9000)

                print('received!')
                dataP = pickle.loads(data)
                print('unpickled!')
                print(type(dataP))

                data = dataP #attente d'une reponse pdt 2sec en cas de timeout retourne une erreur, d'ou le try & except

                self.thereIsSomeNewData = True

            except:
                pass
                #print("y'a un pb bb") #en cas de time-out on passe simplement à la suite
            if self.thereIsSomeNewData:
                self.__RequestTreatment(data)#J'ai sorti la fonction du try; pour rendre le débuggage possible
            self.thereIsSomeNewData = False
'''
#------------------------client.py---------------------





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
        self.thereIsSomeNewData = False # désolé pour la longueur du nom de cette variable je nickname'ai pas trouvé mieux
    def __RequestTreatment(self, Request):

        receptionPaquet(Request)
        #flow(Request)
        # #extractiona =  des données pour qu'elles soient récupérées par Arthur

    def run(self):

        while 1:
            if len(self.Message) >= 1: #si un message a été ajouté depuis la dernière fois
                data = self.Message.pop()
                dataP = pickle.dumps(data)
                print('pickled!')
                Sock.sendall(dataP) #envoi du message ss forme de bytecode
                print('data sent!')
                #conn, addr = s.accept()

            try :
                data = Sock.recv(9000)

                print('received!')
                dataP = pickle.loads(data)
                print('unpickled!')
                print(type(dataP))

                data = dataP #attente d'une reponse pdt 2sec en cas de timeout retourne une erreur, d'ou le try & except

                self.thereIsSomeNewData = True

            except:
                pass
                #print("y'a un pb bb") #en cas de time-out on passe simplement à la suite
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

        self.host = socket.gethostbyname(Host) #récupération de l'adresse auprès des DNS par défaut si nom de domaine fourni
        self.port = Port
        self.nickname = Nickname #La Gui indique Pseudo au lieu de nickname, doit mesurer 10 charactères ou moins
        self.nickLen = str(len(self.nickname))  #calcul de la longueur du Pseudonyme
        self.password = Pass #le pas ne sert pas durant la phase d'identification du client, j'ai cependant implanté cette variable si mes camarades en ont besoin
        self.connected = False
        self.__NetThread = NetThread()
        self.__NetThread.start() #Démarrage du thread chargé d'éccouter et de shipper les messages

    def identify(self):
        '''Envoie une requette d'identification.
        Necessaire coté serveur c'est la première chose à faire après avoir initialisé Net.

        Par Joris Placette
        '''
        data = bytes("IDTF" + self.nickLen + self.nickname, 'utf8') #on crée la chaine d'info d'identification comme "IDTF7exemple"

        try:
            Sock.connect((self.host, self.port)) # on se connecte sur le serveur avec les informations données
            print("Connection avec le serveur...")
            Sock.sendall(data)
            print("Identification auprès du serveur...")
            time.sleep(1) #afin de donner le temps au serv d'être en écoute

            self.connected = True #la connexion a été établie, MAJ du status

        except:
            print("Impossible de se connecter au serveur !")
            self.connected = False

    def connected(self):
        '''Affiche le statut du client vis à vis du serveur

        Par Joris Placette
        '''
        return self.connected

    def disconnect(self):
        '''Force la fermeture de la connexion, rends impossible l'entrée et la sortie de données.

        Par Joris Placette
        '''
        Sock.close() # rends impossible l'entrée et la sortie de données.
        print("Disconnected")

    def share(self, typed):
        '''Permet de transmettre une chaine de caractères brute au serveur.

        /!\ : Pour le moment les messages sont transmis toute les 2sec et non empillés, donc en cas de spam des messages seront perdus :/

        /!\ : Version DEV :
            Svp pay attention :) !
            Si la Chaine est reconnue comme une ligne de code python alors elle est EXECUTEE.

        Par Joris Placette
        '''
        self.__NetThread.Message.append(typed) #transmett la chaine au thread, on nickname'execute pas de fonction sinon il faut attentdre la fin de celle-ci , on se contente donc de transmettre la donnée.

    def whoAmI(self):
        '''Renvoie le Pseudonyme déclaré au serveur lors de l'__init__()

        Par Joris Placette
        '''
        return self.nickname

global flow

def flow(request):
    '''Cette fonction est appelée à chaque fois que des données sont recues.
    Le traitement de ces données est une simple démonstration.
    Cette fonction permettra à Arthur de recevoir et traiter les données émises par les clients.

    Par Joris Placette
    '''




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

    MyNet.identify() #séquence d'identification
    if MyNet.connected == True :
        print("Vous êtes connecté en tant que {}".format(MyNet.whoAmI()))
        while True:
            Typed = input(">")
            MyNet.share({'test':45, 'text':Typed})


def receptionPaquet(paquetIn):
    global a
    del a
    a = UnoPOO.Jeu(False, paquetIn)
    a.player[localID].nom=localNickname

    if localID == a.active :
        print('''! ! !  A TOI DE JOUER ! ! !''')
        a.ask()
        paquetOut = a.pack()
        network.share(paquetOut)

    else:
        print('en attente de joueur {}:  {} '.format(a.player[a.active].num,a.player[a.active].nom ))

if __name__ == '__main__':
    #création de l'objet jeu
    global a
    a = UnoPOO.Jeu(True, 'False', 2)
    paquet = a.pack()

    global localID, localNickname
    localID = getLocalID()

    #obtension des infos de networking
    host, port, localNickname, password = getNetworkInfos()

    #création de l'objet de networking client
    network = Net(host, port, localNickname, password)
    #identification auprès du serveur
    network.identify()

    while True :
        try :
            exec(input(">>>"))
        except :
            print("error")
            

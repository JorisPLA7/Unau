from lib.client import *
import UnoPOO

def login():
    '''Fct de démonstration et de test.
    Par Joris Placette
    '''
    Host ="127.0.0.1"
    Port = 8082
    print("Saisir 'q' pour obtenir un terminal de commande")
    Nickname = str(input("saisir un pseudo (inferieur à 10 caractères):  "))
    if Nickname == 'q':
        debug()
    Pass = "lol ;')"
    global MyNet
    MyNet = Net(Host, Port , Nickname, Pass)

    monJeu = UnoPOO.Jeu(True)

    MyNet.Identify() #séquence d'identification
    if MyNet.Connected == True :
        print("Vous êtes connecté en tant que {}".format(MyNet.WhoAmI()))
        while True:
            Typed = input(">")
            try :
                exec(Typed) #sorte d'invite de commande en cas de lancement interactif sur le serveur
            except:
                MyNet.Transmit({'test': monJeu , 'text':Typed})

if __name__ == '__main__':
    login() # ce fichier sera peut-être une librairie, il faut donc empêcher l'inclusion du login si appelée par un autre fichier.

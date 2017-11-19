from lib.client import *
import UnoPOO

def login(a):
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


    MyNet.Identify() #séquence d'identification
    if MyNet.Connected == True :
    print("Vous êtes connecté en tant que {}".format(MyNet.WhoAmI()))
    MyNet.Transmit(a)

if __name__ == '__main__':

    monJeu = UnoPOO.Jeu(True)
    monJeu.pack()

    login(monJeu) # ce fichier sera peut-être une librairie, il faut donc empêcher l'inclusion du login si appelée par un autre fichier.

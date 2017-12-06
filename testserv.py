from lib.serveur import *
global broadcast
broadcast = True #ATTENTION DEF LE BROADCAST à VRAI OU FAUX EST INDISPENSABLE POUR LE MOMENT

def SimpleHost():
    '''Fct de démonstration et de test.
    c'est un cadeau pour toi Samuel <3 ^^

    Par Joris Placette
    '''
    MyServ = ServerNet()
    MyServ.Listen(True)
    print("En attente de clients...")

if __name__ == '__main__':
    SimpleHost() # ce fichier sera peut-être une librairie, il faut donc empêcher l'inclusion du login si appelée par un autre fichier.

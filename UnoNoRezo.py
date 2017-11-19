

from lib import client
import UnoPOO

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

if __name__ == '__main__':
    #création de l'objet jeu
    a = UnoPOO.Jeu(True)
    a.pack()



    #obtension des infos de networking
    global localNickname
    host, port, localNickname, password = getNetworkInfos()

    #création de l'objet de networking client
    network = client.Net(host, port, localNickname, password)
    #identification auprès du serveur
    network.Identify()

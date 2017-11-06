#compilation

def compilation():
    dictio={}
    dictio["deck"]= list(deck)
    dictio["carte"]=list(Sensei.table)
    dictio["bin"]=list(Sensei.bin)
    dictio["sens"]=Sensei.sens
    dictio["AlivePlayers"]=list(Sensei.alivePlayers)
    dictio["lastPlayer"]=Sensei.lastPlayer
    dictio["chainMemory"]=Sensei.chainMemory
    dictio["battle"]=Sensei.battle
    playersData=[]
    for i in range(len(Sensei.player)):
        dico={}
        playersData.append(dico)
        playersData[i]["id"]=Sensei.player[i].playerNumber
        playersData[i]["hand"]=list(Sensei.player[i].main)
        playersData[i]["status"]=Sensei.player[i].gagne
    dictio["playersData"]=list(playersData)



def decompilation(dictio):

    list(deck) = dictio["deck"]
    list(Sensei.table) = dictio["carte"]
    list(Sensei.bin) = dictio["bin"]
    Sensei.sens = dictio["sens"]
    list(Sensei.alivePlayers) = dictio["AlivePlayers"]
    Sensei.lastPlayer = dictio["lastPlayer"]
    Sensei.chainMemory = dictio["chainMemory"]
    Sensei.battle = dictio["battle"]
    playersData=[]
    Sensei.player=[0 for i in range(len(dictio["playersData"]))]

    for i in range(len(dictio["playersData"])):
        Sensei.player[i].playerNumber=playersData[i]["id"]
        list(Sensei.player[i].main)=playersData[i]["hand"]
        Sensei.player[i].gagne = playersData[i]["status"]
        
    list(playersData) = dictio["playersData"]

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
        playersData[i]["id"]=Sensei.player[i].player
        playersData[i]["hand"]=list(Sensei.player[i].main)
        playersData[i]["status"]=Sensei.player[i].gagne
    dictio["playersData"]=list(playersData)
    
    
    

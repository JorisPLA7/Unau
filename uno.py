from random import *

"""
ATTENTION Créer une fonction de recyclage des cartes
"""

    
        
class Mj():
  def __init__(self, nombreJoueurs=2, ):
    player = []
    self.alivePlayers= [i for i in range(nombreJoueurs)]
    self.sens = True
    self.lastPlayer = 0 #dernier joueur ayant joué
    
    self.chainMemory=0
    
    for i in range(nombreJoueurs):
      player.append(Player(i))
    
    
    self.deck=[["+4",0] , ["+4",0]  , ["+4",0]  , ["+4",0]  , ["change",0] , ["change",0] , ["change",0] , ["change",0] ]
    val=[0,1,2,3,4,5,6,7,8,9,"+2",1,2,3,4,5,6,7,8,9,"+2","sens","sens","no","no"]
    colors=["j","v","b","r"]
    for i in range(len(val)):
        for j in range(len(colors)):
            self.deck.append([val[i],color[j]])
    shuffle(self.deck)
    self.table=deck.pop(0)
    
    self.bin = []
    
    while type(table[0])!=type(1): #si la 1ere carte est "spéciale" 
      self.bin.append(self.table)  #on repioche jusqu'à l'obtention d'un nbr
      self.table=self.deck.pop(0)
      
  def whosNext(self):
   
    
    if self.table[0]!="no":
      if sens : return alivePlayer[(self.lastPlayer + 2*True)%(len(self.alivePlayers))]
      else : return self.alivePlayers[(self.lastPlayer - 2*True + len(self.alivePlayers))%(len(self.alivePlayers))]
    
    else :
      if sens : return (self.lastPlayer + True)%(len(self.alivePlayers))
      else : return (self.lastPlayer - True + len(self.alivePlayers))%(len(self.alivePlayers))
      
  
  def call(self):
    called=self.whosnext()
    action=Player[called].play()
    return called, action
  
  def validation(self, act):
    if table[0]!="+2" and table[0]!="+4" : #si on a pas de surenchère, 
      if act=="pioche": #le joueur peut effectuer un tour "normal" (jouer/piocher)
        return True
        
      elif self.table[0]==act[0] or self.table[1] == act[1] :
        return True
      
      elif act[1]==0:
        return True
        
      else :#carte interdite
        return False
    
    
    
    else : #+4 ou +2
      if act=="pioche" :
        return True
        
      elif act[0]==table[0]: #surenchère
        return True
      
      else : # mauvaise carte
        return False
        
      
  def ParentDeJeu(self):
    '''
    fct qui appelle jeu et le rapelle après ne pioche
    '''
    
    replay=False
    endTurn=self.jeu(replay)
    if endTurn==False :
      replay=True
      self.jeu(replay)
      
  
  def jeu(self, replay):
    called, action=self.call()
    test=self.validation(action)
    while test != True :
      print("Action Impossible")
      called, action=self.call()
      test=self.validation(action)
    
    
    endTurn = False
    
    if action == "pioche" and replay == False:
      if table[0]!="+2" and table[0]!="+4" : #si on a pas de surenchère
        Player[called].pioche()
        endTurn=False
      elif table[0]="+2" :
        self.chainMemory+=2
        endTurn=True
        for i in range(chainMemory) :
          Player[called].pioche()
        self.chainMemory=0
        
      elif table[0]="+4" :
        self.chainMemory+=4
        endTurn=True
        for i in range(chainMemory) :
          Player[called].pioche()
        self.chainMemory=0
        
        
    elif action == "pioche" and replay == True:
      endTurn = True
      
      
    else :
      self.bin.append(self.table)
      self.table=action
       
      if self.table[0]=="sens":
        self.sens = not(self.sens)
        endTurn = True
        
      if self.table[0]=="change":
        self.table[1]=Player(called).askColor()
        endTurn = True
        
      elif self.table[0]=="+2" :
        self.chainMemory+=2
        endTurn = True
        
      elif self.table[0]=="+4" :
        self.chainMemory+=4
        endTurn = True
        
    return endTurn
    
      
      
    

  
class Player():
    def __init__(self, number):
      self.player=number
      self.main= [deck.pop(0) for i in range(7)]
        
    def play(self):
      print(self.main)
      indice=int(input("indice de la carte à jouer :"))
      if indice<0:
        return "pioche"
      else :
        return self.main[indice]
      
    def pioche(self):
      self.main.append(deck.pop())
      
    def askColor(self):
      color = 'satan'
      colors =  ["v","b","j","r"]
      while colors.count(color) == 0:
        color = input("r/v/j/b")
      return color
      


def routine():
    print ""
 
if __name__ == '__main__':
    routine()



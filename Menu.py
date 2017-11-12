#interface
import cocos
import pyglet
from cocos.actions import *
from cocos.director import *

class Menu(cocos.layer.base_layers.Layer):
    def __init__(self):
        self.items=[]
        img=("Ressources\Sprites\Bambous.jpg")
        img2=("Ressources\Sprites\Bambou1.png")
        Bambous = pyglet.sprite.Sprite(img)
        HighLighted=pyglet.sprite.Sprite(img2)
        nouveau=MenuItem('Nouveau', self.newGame)
        nouveau.generateWidgets(30,30,Bambous,HighLighted)
        self.items.append(nouveau)
        self.items.add(self)
        
        self.create_menu(self.items, zoom_in(), zoom_out() )
        
    def newGame():
        print("ok")
        
hello=Menu
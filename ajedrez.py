# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 17:12:54 2020

@author: FranciscoJose
"""
B = "blancas" 
N = "negras" 
profundidad=2

import sys

def print3(*args, **kargs):
    sep = kargs.get('sep',' ')
    end = kargs.get('end','\n')
    file = kargs.get('file',sys.stdout)
    output=''
    first = True
    for arg in args:
        output +=('' if first else sep) + str(arg)
        first=False
        file.write(output+end)


class Game: 
    #ive decided since the number of Piezas is capped but the type of Piezas is not (Peon transformations), I've already coded much of the modularity to support just using a dictionary of Piezas 
    def __init__(self): 
        self.turno = B 
        self.message = "this is where prompts will go" 
        self.tableros = [profundidad,{}] 
        self.colocaPiezas() 
        print3("chess program. enter moves in algebraic notation separated by space") 
        self.main() 


         
    def colocaPiezas(self): 
       
        for i in range(0,8): 
                self.tableros[0,(i,1)] = Peon(B,uniDict[B][Peon],1) 
                self.tableros[0,(i,6)] = Peon(N,uniDict[N][Peon],-1) 
             
        localizadores = [Torre,Caballo,Alfil,Reina,Rey,Alfil,Caballo,Torre]
        for i in range(0,8): 
                self.tableros[0,(i,0)] = localizadores[i](B,uniDict[B][localizadores[i]])
       
        localizadores.reverse()        
        for i in range(0,8): 
                self.tableros[0,((7-i),7)] = localizadores[i](N,uniDict[N][localizadores[i]]) 
        


class Pieza: 
     
    def __init__(self,color,simbolo): 
        self.simbolo = simbolo 
        self.position = None 
        self.Color = color 
    def isValid(self,startpos,endpos,Color,tableros): 
        if endpos in self.availableMoves(startpos[0],startpos[1],tableros, Color = Color): 
            return True 
        return False 
    def __repr__(self): 
        return self.simbolo 
     
    def __str__(self): 
        return self.simbolo 
     
    def availableMoves(self,x,y,tableros): 
        print3("ERROR: no movement for base class") 
         
    def AdNauseum(self,x,y,tableros, Color, intervals): 
        """repeats the given interval until another Pieza is run into.  
        if that Pieza is not of the same color, that square is added and 
         then the list is returned""" 
        answers = [] 
        for xint,yint in intervals: 
            xtemp,ytemp = x+xint,y+yint 
            while self.isInBounds(xtemp,ytemp): 
                #print(str((xtemp,ytemp))+"is in bounds") 
                 
                target = tableros.get((xtemp,ytemp),None) 
                if target is None: answers.append((xtemp,ytemp)) 
                elif target.Color != Color:  
                    answers.append((xtemp,ytemp)) 
                    break 
                else: 
                    break 
                 
                xtemp,ytemp = xtemp + xint,ytemp + yint 
        return answers 
                 
    def isInBounds(self,x,y): 
        "checks if a position is on the board" 
        if x >= 0 and x < 8 and y >= 0 and y < 8: 
            return True 
        return False 
     
    def noConflict(self,tableros,initialColor,x,y): 
        "checks if a single position poses no conflict to the rules of chess" 
        if self.isInBounds(x,y) and (((x,y) not in tableros) or tableros[(x,y)].Color != initialColor) : return True 
        return False 
         
         
chessCardinals = [(1,0),(0,1),(-1,0),(0,-1)] 
chessDiagonals = [(1,1),(-1,1),(1,-1),(-1,-1)] 


def CaballoList(x,y,int1,int2): 
    """sepcifically for the Torre, permutes the values needed around a position for noConflict tests""" 
    return [(x+int1,y+int2),(x-int1,y+int2),(x+int1,y-int2),(x-int1,y-int2),(x+int2,y+int1),(x-int2,y+int1),(x+int2,y-int1),(x-int2,y-int1)] 
def ReyList(x,y): 
    return [(x+1,y),(x+1,y+1),(x+1,y-1),(x,y+1),(x,y-1),(x-1,y),(x-1,y+1),(x-1,y-1)] 






class Caballo(Pieza): 
    def availableMoves(self,x,y,tableros, Color = None): 
        if Color is None : Color = self.Color 
        return [(xx,yy) for xx,yy in CaballoList(x,y,2,1) if self.noConflict(tableros, Color, xx, yy)] 
         
class Torre(Pieza): 
    def availableMoves(self,x,y,tableros ,Color = None): 
        if Color is None : Color = self.Color 
        return self.AdNauseum(x, y, tableros, Color, chessCardinals) 
         
class Alfil(Pieza): 
    def availableMoves(self,x,y,tableros, Color = None): 
        if Color is None : Color = self.Color 
        return self.AdNauseum(x, y, tableros, Color, chessDiagonals) 
         
class Reina(Pieza): 
    def availableMoves(self,x,y,tableros, Color = None): 
        if Color is None : Color = self.Color 
        return self.AdNauseum(x, y, tableros, Color, chessCardinals+chessDiagonals) 
         
class Rey(Pieza): 
    def availableMoves(self,x,y,tableros, Color = None): 
        if Color is None : Color = self.Color 
        return [(xx,yy) for xx,yy in ReyList(x,y) if self.noConflict(tableros, Color, xx, yy)] 
         
class Peon(Pieza): 
    def __init__(self,color,simbolo,direction): 
        self.simbolo = simbolo 
        self.Color = color 
        #of course, the smallest Pieza is the hardest to code. direction should be either 1 or -1, should be -1 if the Peon is traveling "backwards" 
        self.direction = direction 
    def availableMoves(self,x,y,tableros, Color = None): 
        if Color is None : Color = self.Color 
        answers = [] 
        if (x+1,y+self.direction) in tableros and self.noConflict(tableros, Color, x+1, y+self.direction) : answers.append((x+1,y+self.direction)) 
        if (x-1,y+self.direction) in tableros and self.noConflict(tableros, Color, x-1, y+self.direction) : answers.append((x-1,y+self.direction)) 
        if (x,y+self.direction) not in tableros and Color == self.Color : answers.append((x,y+self.direction))# the condition after the and is to make sure the non-capturing movement (the only fucRey one in the game) is not used in the calculation of checkmate 
        return answers 


uniDict = {B : {Peon : "♙", Torre : "♖", Caballo : "♘", Alfil : "♗", Rey : "♔", Reina : "♕" }, N : {Peon : "♟", Torre : "♜", Caballo : "♞", Alfil : "♝", Rey : "♚", Reina : "♛" }} 
         


         
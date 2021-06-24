# -*- coding: utf-8 -*-
"""
Created on Sat Jun 03 22:14:21 2017

@author: Amab

Learn to code sans you f***
"""
from tkinter import *
import math
class GUI(Frame): #define the GUI class
    ##########################################################################
    #initialize class variables and other UI

    ##########################################################################
  
    def __init__(self, parent): #define the intial setup of the GUI
        self.parent = parent
        Frame.__init__(self,parent)
        self.GC_p = 27
        self.GBA_p = 7
        self.initUI()
    
    def initUI(self):
        self.parent.title("AGuAcaTE")
        self.pack(fill=BOTH, expand=True) 
        mainframe = Frame(self,relief=RAISED)
        mainframe.pack(fill=BOTH)
        
        self.PRNG_entry = Entry(mainframe,width=15)
        self.PRNG_entry.grid(column=1,row=1,padx=2,pady=2,sticky=W)
        PRNGlabel = Label(mainframe,text="Current PRNG:")
        PRNGlabel.grid(column=0,row=1,padx=2,pady=2)
        Run_button = Button(mainframe,text="Run",command=self.run)
        Run_button.grid(column=2,row=1,padx=2,pady=2,sticky=E)
        
        self.disp = Text(mainframe,width=60,height=4,font=("Helvetica", 10))
        self.disp.grid(column=0,row=0,padx=2,pady=2,columnspan = 3)
    
    def xdrng(self,seed,j):
        k = 0
        while (k <= j):
       # newseed = seed
       # seed = (0x000043FD*(seed&0xFFFF)+((0x00000003*(seed&0xFFFF)+0x000043FD*int(seed/0x10000))&0xFFFF)*0x10000+0x00269EC3)&(0xFFFFFFFF) #formula
            seed = (seed * 0x343FD + 0x269ec3) & 0xFFFFFFFF
            k += 1
        return seed
        
    def xdrngr(self,seed,j): 
      k = 0
      while (k <= j):
        seed = (seed * 0xB9B33155 + 0xA170F641) & 0xFFFFFFFF
    #    seedr = (0x00003155*(seed&0xFFFF)+((0x0000B9B3*(seed&0xFFFF)+0x00003155*int(seed/0x10000))&0xFFFF)*0x10000+0xA170F641)&(0xFFFFFFFF) #formula
    #    seed = seedr
        k += 1
      return seed

    def run(self):
        
        TARGET = 29279
        inputPRNG = int(self.PRNG_entry.get())
        currentPRNG = inputPRNG
        closestCycle = math.floor((currentPRNG-TARGET)/2792)
        difference = currentPRNG - (TARGET + closestCycle*2792)
        highestBound = 4*difference/27
        lowestBound = difference/7
        self.disp.delete(0.0,END)
        
        # cycles must be positive, there also has to be an integer between the two bounds
        if((math.floor(highestBound) >= lowestBound or difference == 0) and closestCycle >= 0):
            self.disp.insert(0.0,'Closest cycle is ')
            self.disp.insert(END,str(closestCycle))
            self.disp.insert(END,'\r\n')

            ldeSolution = math.floor(highestBound)
            gcRedeems = -1*difference + 7 * ldeSolution
            gbaRedeems = 4*difference - 27 * ldeSolution
          
            self.disp.insert(END,'Number of Pikachu/Celebi GC Redeems is ')  
            self.disp.insert(END,gcRedeems)
            self.disp.insert(END,'\r\n')

            self.disp.insert(END,'Number of Pikachu GBA Redeems is ')  
            self.disp.insert(END,gbaRedeems)        
            self.disp.insert(END,'\r\n')

            self.disp.insert(END,'Difference ')  
            self.disp.insert(END,str(difference)) 
        else:
            self.disp.insert(0.0,'Not Possible')        

def main():
    
    root = Tk() #create GUI app
   
    root.geometry("430x103+10+10") #define GUI shape
    #root.tk.call('tk','scaling',1.25)
    #root.resizable(width=False, height=False) #no resizing
    
    
    app = GUI(root)#def app
    
    root.mainloop()  #do the GUI stuff
    try:    
        root.destroy() #destroy the GUI if the user hits file exit
    except:
        pass # dont if they hit the x button because its already gone


if __name__ == '__main__': #do the main
    main()  
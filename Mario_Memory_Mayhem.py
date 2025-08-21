# Program Name: Mario Memory Mayhem
# Description: A mario themed memory matching game that provides an accessible
#              option for colorblind individuals

###############################################################################

#Importing all the necessary modules

import tkinter as tk
from PIL import Image, ImageTk
import random

###############################################################################

class Card(tk.Button):
    
    """ A custom class that represents each card in the game as a button.

        Attributes:
                   frame: the tkinter frame for the display
                   points: to keep track of the regular and special cards
                   name: keeps track of the name of image for display & matching
                   grey: determines whether it's normal or colorblind
    
        Returns:
                None """
    
    def __init__(self, frame, points, name, grey=False):
    
        super().__init__(frame)
        self.grey = grey #keeps track of whether colorblind or not
        self.frame = frame #keeps track of frame
        self.points = points #keeps track of points
        self.open = False #keeps track of whether open or not
        self.matched = False #keeps track of whether matched or not
        self.__name = name #keeps track of name and is weakly private 
        
    def face_down(self, i, rely): #gets the image from computer
        image = ImageTk.PhotoImage(Image.open("card.png").resize((124, 124)))
        if self.grey: #check for colorblind
            image = ImageTk.PhotoImage(Image.open("card.png").convert("L")
                                       .resize((124, 124))) #makes it greyscale
        self.configure(bg="white", image=image, command=self.face_up)
        self.image = image       #puts image on card button
        self.place(relx=(0.15 + (0.09) * i), rely=rely) #places card on screen
        self.set_open(False) #tells system that card is closed
        
    def re_face_down(self):
        self.set_open(False) #tells system that card is closed
        image = ImageTk.PhotoImage(Image.open("card.png").resize((124, 124)))
        if self.grey: #check for colorblind
            image = ImageTk.PhotoImage(Image.open("card.png").convert("L")
                                       .resize((124, 124)))
        self.configure(image=image) #puts image on card button
        self.image = image #stores it
        
    def face_up(self):
        self.set_open(True) #tells system that card is opened
        image = ImageTk.PhotoImage(Image.open(self.name).resize((124, 124)))
        if self.grey:
            image = ImageTk.PhotoImage(Image.open(self.name).convert("L")
                                       .resize((124, 124))) #greyscale
        self.configure(image=image) #sets character image
        self.image = image
        self.frame.after(300, self.frame.check) #sends to check function
    
    def disable(self):
        self.configure(state="disabled") #disables the card from further action
        
    @property
    def name(self):
        return self.__name #returns the name
   
    # Implementing getters
    def get_open(self):
        return self.open #returns open status

    def get_points(self):
        return self.points #returns points
    
    def get_matched(self):  
        return self.matched #returns matched
    
    # Implementing setters
    def set_open(self, val: bool):
        self.open = val #assigns open a value

    def set_points(self, val: int):
        self.points = val #assigns points a value
        
    def set_matched(self, val: int):
        self.matched = val #assigns matched a value
            
    def __eq__(self, other): # Comparison operator
        if type(other) == type(self): #checks if they are the same
            return self.name == other.name 
        else:
            raise NotImplementedError
        
    def __radd__(self, value): #common operator   
        if type(value) == int:
            return self.get_points() + value #adds the points
        else:
            raise NotImplementedError

###############################################################################

class Board(tk.Frame):
            
    """ A custom frame class that sets widgets for the board in the game.

    Attributes:
               All that can be inherited from tk.frame
             
    Returns:
            None"""
    
    frames = {}
    
    def __init__(self, window, bg, name):
        super().__init__(window) #initializing the window
        self.config(bg=bg) #setting the background
        Board.frames[name] = self #adding frames to board
    
    @classmethod
    def get_frame(cls, name):
        return cls.frames[name]
        
    #creates a label that can be modified to preference
    def add_label(self,text:str,relx:float,rely:float,anchor:str,title: bool):
        fts = 16
        if title:
            fts = 60
        label = tk.Label(self, text=text,font=("System",fts), fg="white",
                         bg="black")
        label.place(relx=relx, rely=rely, anchor=anchor)
        return label
    
    #creates a button that can be modified to preference
    def add_button(self,text:str,command,relx:float,rely:float,anchor: str):
        btn = tk.Button(self, text=text,font=("System", 14), height=1,
                        width=10, command=command)
        btn.place(relx=relx, rely=rely, anchor=anchor)
        return btn

###############################################################################
    
class Deck(Board):
               
    """ A custom class for the game display that inherits from board.

    Attributes:
               All that can be inherited from board
             
    Returns:
            None """
        
    def __init__(self, window, bg, name, grey=False):
        super().__init__(window, bg, name)
        self.__score = 0 # weakly private and sets score
        self.window = window #sets window
        self.lives = 8 #sets lives
        self.specials = [3,9,10,14] #sets the special card names
        self.grey = grey #sets colorblind
        self.score_label = self.add_label("Score : " + str(self.score),0.5,0.68,
                                          "center", True) #puts title
        self.quit_btn = self.add_button("Quit",self.window.destroy,0.5,0.82,
                                        "center") #puts button
        self.hearts = self.place_hearts() #shows the lives
        self.cards = self.set_cards() #shows the cards
        
    @staticmethod
    def deal_cards():
        characters = range(0, 16) # sets the range for the 16 characters
        choose = 8 #needs eight
        chosen = random.sample(characters, choose) #chooses any eight
        chosen.extend(chosen) #making duplicates of the chosen
        return chosen

    @property
    def score(self):
        return self.__score #gets score
        
    def set_score(self):
        matched = self.get_matched()
        score = 0
        for match in matched:
            score += match #adds the scores
        self.__score = score
    
    def get_matched(self):
        matched = []
        for card in self.cards:
            if card.get_matched():
                matched.append(card) #gets all the matched cards
        return matched     
    
    def get_not_matched(self):
        opened = []
        for card in self.cards:
            if card.get_open() and not card.get_matched():
                opened.append(card) #gets all the unmatched cards
        return opened    
    
    def set_cards(self):
        cards = []
        dealed = Deck.deal_cards()
        for j in [0.25, 0.45]: #sets up the 2 rows
            for i in range (8): # Sets the cards in each row 
                name = dealed.pop(random.randint(0,len(dealed)-1))
                point = 1 #assigns point
                if name in self.specials:
                    point = 2 #assigns point
                card = Card(self,point, str(name) + ".png",self.grey)
                card.face_down(i, j) #puts the card on screen
                cards.append(card) #adds to list for future use
        return cards
    
    def update_score(self):
        self.score_label.configure(text="Score : " + str(self.score))#new score 
    
    def place_hearts(self):
        hearts = []
        for i in range(self.lives): #gets the image for lives
            image = ImageTk.PhotoImage(Image.open("heart.png").resize((80, 80)))
            if self.grey: #checks for colorblind
                image = ImageTk.PhotoImage(Image.open("heartw.png").resize((80,
                                                                        80)))
            heart = tk.Label(self, image=image, bg="black") 
            heart.place(relx=(0.3 + (0.05) * i), rely=0.08) #puts in on screen
            heart.image = image
            hearts.append(heart) #adds to list for future use
        return hearts
    
    def remove_hearts(self):
        self.lives -= 1          #gets the image for used lives
        image = ImageTk.PhotoImage(Image.open("heartw.png").resize((80, 80)))
        if self.grey:
            image = ImageTk.PhotoImage(Image.open("heartg.png").resize((80,80)))
        self.hearts[self.lives].configure(image= image) #puts in on screen
        self.hearts[self.lives].image = image  #stores it       

    def add_hearts(self):    
        if self.lives < len(self.hearts) - 1:
            image = ImageTk.PhotoImage(Image.open("heart.png").resize((80, 80)))
            if self.grey:
                image = ImageTk.PhotoImage(Image.open("heartw.png").resize((80,
                                                                           80)))
            self.hearts[self.lives].configure(image=image) #turns used into new
            self.hearts[self.lives].image = image
            self.lives += 1 #also adding to number of lives
        
    def check(self):
        unmatched = self.get_not_matched() #getting the unmatched cards
        matched = self.get_matched() #getting the matched cards
        if len(unmatched) == 2: #checks if there are only 2 cards 
            if unmatched[0] == unmatched[1]: #checks to see if they match
                unmatched[0].set_matched(True)
                unmatched[1].set_matched(True)
                unmatched[0].disable() #disables them from further use
                unmatched[1].disable()
                # Update score
                self.set_score()
                self.update_score() #adds to score
                self.add_hearts() #and lives
                
            else: #doesn't match
                unmatched[0].re_face_down() #flips back
                unmatched[1].re_face_down()
                self.remove_hearts() #remove life
                
        matched = self.get_matched()   
        if self.lives == 0 or len(matched) == 16: #checks if game can end
            if self.grey:
                self.after(1, self.window.setup_score("Game2"))
            else:
                self.after(1, self.window.setup_score("Game1"))
            
###############################################################################
                
class MemoryGame(tk.Tk):
           
    """ A custom class that creates tk.window and holds other info about frames.

    Attributes:
               All that can be inherited from tk.Tk
            
    Returns:
            None """
        
    def __init__(self, title):
        super().__init__()
        self.geometry("{}x{}".format(self.winfo_screenwidth(), #sets the screen
                                     self.winfo_screenheight())) #size
        self.title(title) #gives screen name
        self.add_frames() #adds frames
        self.setup_home() #starts with the homepage
        
    def add_frames(self):
        Board(self,"black","Home") #homepage frame
        Board(self, "black","Rules") #instructions frame
        Board(self,"black","Mode") #gaming mode frame
        Deck(self,"black","Game1", False) #normal game
        Deck(self,"black","Game2",True) #colorblind game
        Board(self,"black","Score") #scoreboard frame
    
    def setup_home(self):
                
        lb1 = Board.get_frame("Home").add_label("Mario Memory Mayhem",0.5,0.4,
                                            "center",True) #game title
        btn1 = Board.get_frame("Home").add_button("Start",self.instructions,0.5,
                                              0.55,"center") #start  
        self.show_page("Home", "")
        
    def instructions(self): #dispalying the rules of the game
        lb1 = Board.get_frame("Rules").add_label("Instructions",0.5,0.2,"center"
                                                 ,  True)
        lb2 = Board.get_frame("Rules").add_label("In this game you will start "+
                                             "with 8 lives",0.5,0.35,"center",
                                             False)
        lb3 = Board.get_frame("Rules").add_label("You will have 16 cards to " +
                                             "match, so 8 pairs in total",0.5,
                                             0.4,"center", False)
        lb4 = Board.get_frame("Rules").add_label("Turn over any two cards",0.5,
                                             0.45,"center", False)
        lb5 = Board.get_frame("Rules").add_label("If the cards match you will "+
                                             "earn points and restore a life",
                                             0.5,0.5,"center", False)
        lb6 = Board.get_frame("Rules").add_label("Regular pairs will earn you "+
                                             "2 points but some special pairs "+
                                             "will earn you 4 points",0.5,0.55,
                                             "center", False)
        lb7 = Board.get_frame("Rules").add_label("If the cards don't match " +
                                             "they will flip back and you will"+
                                             " loose a life",0.5,0.6,"center",
                                             False)
        lb8 = Board.get_frame("Rules").add_label("The game will end when you " +
                                             "either run out of lives or match"+
                                             " all 16 cards",0.5,0.65,"center",
                                             False)
        btn1 = Board.get_frame("Rules").add_button("Next",self.setup_mode,0.5,
                                                   0.75, "center")
        self.show_page("Rules", "Home")
        
    def setup_mode(self):
        lb = Board.get_frame("Mode").add_label("Select Game Mode!",0.5,0.4,
                                               "center", True)
        btn1 = Board.get_frame("Mode").add_button("Normal",self.normal_game,0.45
                                                  ,0.5,"center")#sends to normal
        btn2 = Board.get_frame("Mode").add_button("Colorblind", #to colorblind
                                                  self.colorblind_game,0.55,0.5,
                                                  "center")
        self.show_page("Mode","Rules")
        
    def normal_game(self):      
        self.show_page("Game1","Mode") #the normal game
        
    def colorblind_game(self):
        self.show_page("Game2","Mode") #the colorblind game
    
    def setup_score(self, name: str):
        if Board.get_frame(name).lives == 0: #if  lost
            lb1 = Board.get_frame("Score").add_label("Better luck next time!",
                                                 0.5,0.4,"center",True)
        else: #if won
            lb1 = Board.get_frame("Score").add_label("Yay! You did it!",0.5,0.4,
                                                 "center",True)
        
        lb2 = Board.get_frame("Score").add_label("Your final score is " +
                                             str(Board.get_frame(name).score),
                                                 0.5, 0.6,"center",False)#score
        btn1 = Board.get_frame("Score").add_button("Exit",self.destroy,0.50,0.8,
                                               "center")
        self.show_page("Score",name)
        
    def show_page(self, key: str, erase: str):#making it easier to change frames
        if erase != "":
            Board.get_frame(erase).pack_forget() #removes current frame
        Board.get_frame(key).pack(fill=tk.BOTH, expand=True)
        Board.get_frame(key).tkraise() #shows new frame
        
###############################################################################
        
if __name__ == "__main__":   
    game = MemoryGame("Mario Memory Mayhem")
    game.mainloop() #starts the loop
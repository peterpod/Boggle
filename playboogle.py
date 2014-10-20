#Boogle!###%%%55555

from Tkinter import *
import random
import string
#import winsound

#####################################################
import sys

class BoggleSolver:
    
    def __init__(self, board):
        self.dictionary = Dictionary("words.txt")
        self.board = []
        for row in range(len(board)):
           column=[]
           for col in range(len(board[0])):
              column+=board[row][col].lower()
           self.board+=[column]
        #print self.board      
        #qprint self.board
        self.min_length = 4
        self.found_words = set()

        # Find all words starting from each coordinate position
        for row in xrange(4):
            for column in xrange(4):
                self._find_words(Word.new(row, column), row, column)

    def _find_words(self, word, row, column):
        #print "i am finding words"
        # print self.board
        word.add_letter(self.board[row][column], row, column)
        #print word

        if (self._can_add_word(word)):
            self.found_words.add(word.letter_sequence)

        for row, column in self._get_valid_coodinates_for_word(word, row, column):
            #print self.dictionary.contains_prefix(word.letter_sequence + self.board[row][column])
            if(self.dictionary.contains_prefix(word.letter_sequence + self.board[row][column])):
                self._find_words(Word.new_from_word(word), row, column)

    def _can_add_word(self, word):
        return len(word) >= self.min_length and self.dictionary.contains_word(word.letter_sequence)

    def _get_valid_coodinates_for_word(self, word, row, column):
        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):
                if r >= 0 and r < 4 and c >= 0 and c < 4:
                    if ((r, c) not in word.used_board_coordinates):
                        yield r, c

class Board:
    def __init__(self, letter_list):
        self.side_length = 4
        if (self.side_length != int(self.side_length)):
            raise Exception("Board must have equal sides! (4x4, 5x5...)")
        else:
            self.side_length = int(self.side_length)
        self.board= [["S", "E","R", "S"],
	   ["P", "A","T","G"],
           ["L", "I", "N", "E"],
           ["S", "E","R", "S"]]

    def __getitem__(self, row):
        return self.board[row]

class Word:
    #print "I am in word"
    def __init__(self):
        self.letter_sequence = ""
        self.used_board_coordinates = set()

    @classmethod
    def new(cls, row, column):
        word = cls()
        word.used_board_coordinates.add((row, column))
        return word

    @classmethod
    def new_from_word(cls, word):
        new_word = cls()
        new_word.letter_sequence += word.letter_sequence
        new_word.used_board_coordinates.update(word.used_board_coordinates)
        return new_word

    def add_letter(self, letter, row, column):
        self.letter_sequence += letter
        self.used_board_coordinates.add((row, column))

    def __str__(self):
        return self.letter_sequence

    def __len__(self):
        return len(self.letter_sequence)

class Dictionary:
    def __init__(self, dictionary_file):
        self.words = set()
        self.prefixes = set()
        word_file = open(dictionary_file, "r")

        for word in word_file.readlines():
            #print word.strip()
            self.words.add(word.strip())
            for index in xrange(len(word.strip()) + 1):
                #print self.prefixes
                self.prefixes.add(word[:index])

    def contains_word(self, word):
        return word in self.words

    def contains_prefix(self, prefix):
        #print prefix
        return prefix in self.prefixes

#print words

#######################################################
def playSound(canvas, synchronous,word):
    dictionary=canvas.data.dictionary
    if (synchronous):
        flags = winsound.SND_FILENAME
    else:
        # asynchronous
        flags = winsound.SND_FILENAME | winsound.SND_ASYNC
    #winsound.PlaySound("Deuces.mp3",flags)
    if(word in dictionary):
        winsound.PlaySound("correct.wav", flags)
    else:
        winsound.PlaySound("failbuzzer.wav", flags)

def startSoundLoop():
    flags = winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
    winsound.PlaySound("correct.wav", flags)

def stopSoundLoop():
    flags = winsound.SND_FILENAME
    winsound.PlaySound(None, flags)

def mousePressed(canvas,event):
    margin=canvas.data.margin
    cellSize=canvas.data.cellSize
    board=canvas.data.boogleBoard
    canvas.data.cordsAdded=0
    #while the game is going
    if(canvas.data.isPaused==False and canvas.data.play==True):
       cx=(event.x-margin-260)/cellSize
       cy=(event.y-2*margin)/cellSize
       newWallCenter = (cy,cx)
       #make sure you do not click off the board
       if(cx<0 or cx>3 or cy<0 or cy>3):
           pass
       else:
           if(newWallCenter in canvas.data.clickPiece):
               if(newWallCenter==canvas.data.clickPiece[len(canvas.data.clickPiece)-1]):
                   newWallCenter = (cy,cx)
                   canvas.data.clickPiece.remove(newWallCenter)
                   canvas.data.pressedLetters.remove(canvas.data.pressedLetters[len(canvas.data.pressedLetters)-1])
           else:
               if(len(canvas.data.clickPiece)==0):
                   #just add the location     
                   canvas.data.color="green"
                   #print cx,cy, event.x, event.y, event.x-margin+260,event.y-margin
                   newWallCenter = (cy,cx)
                   canvas.data.clickPiece.append(newWallCenter)
                   canvas.data.cordsAdded+=1
                   canvas.data.pressedLetters.append(board[cy][cx].lower())
               else:
                   #print canvas.data.clickPiece[0]
                   pass
                   #check to see if clicked location is adjacent!
                   #print abs(cy-canvas.data.clickPiece[canvas.data.cordsAdded-1][0]),abs(cx-canvas.data.clickPiece[canvas.data.cordsAdded-1][1])
                   if((abs(cy-canvas.data.clickPiece[canvas.data.cordsAdded-1][0])<=1) and
                      abs(cx-canvas.data.clickPiece[canvas.data.cordsAdded-1][1])<=1):
                       canvas.data.color="green"
                       #print cx,cy, event.x, event.y, event.x-margin+260,event.y-margin
                       newWallCenter = (cy,cx)
                       canvas.data.clickPiece.append(newWallCenter)
                       canvas.data.cordsAdded+=1
                       canvas.data.pressedLetters.append(board[cy][cx].lower())
                   else:
                       pass    
           #print canvas.data.pressedLetters
    redrawAll(canvas)

def ignoreKey(event):
    # Helper function to return the key from the given event
    ignoreSyms = [ "Shift_L", "Shift_R", "Control_L", "Control_R", "Caps_Lock" ]
    return (event.keysym in ignoreSyms)

def keyPressed(canvas,event):
    #keep track of keys pressed
    canvas = event.widget.canvas
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)
    if (ignoreKey(event) == False):
       print canvas.data.pressedLetters, event.keysym
       #key pressed is not an ignored key
       if(event.keysym=="BackSpace"):
          print "i am backspacing"
          canvas.data.pressedLetters.remove(canvas.data.pressedLetters[len(canvas.data.pressedLetters)-1])
       if(event.keysym=="Return"):
          canvas.data.color="orange"
          #return the word 
          score(canvas,canvas.data.pressedLetters)
          #RESET both pressed letters and the tiles
          #on board that were clicked
          canvas.data.pressedLetters=[]
          canvas.data.clickPiece=[]
          canvas.data.cordsAdded=0
       if ((len(event.keysym) == 1) and (event.keysym.isalpha())):
           # it's an alphabetic (A-Za-z)
           canvas.data.pressedLetters.append(event.keysym)
    redrawAll(canvas)
    
def button1Pressed(canvas):
    #PLAY BUTTON
    if(canvas.data.gameOver==True):
        #this function works as a play again function if you
        #want a new game!
        canvas.data.time=120
        canvas.data.gameOver=False
        canvas.play=True
        canvas.data.time=120
        canvas.data.score=0
    #canvas.data.time=120
    canvas.data.play=True
    canvas.data.isPaused=False
    redrawAll(canvas)

def button2Pressed(canvas):
    # Pause
    canvas.data.isPaused=True
    redrawAll(canvas)

def button3Pressed(canvas):
    # Shuffle
    highestScore=bestScore(canvas)
    canvas.data.bestScore=highestScore
    if(canvas.data.time==120):
        loadBoogleBoard(canvas)
    redrawAll(canvas)

def button4Pressed(canvas):
    # Rotate
    rotateBoard(canvas)
    redrawAll(canvas)

def button5Pressed(canvas):
    # Instructions
    canvas.data.mainMenu=False
    canvas.data.instructions=True
    canvas.data.highScores=False
    redrawAll(canvas)    

def button6Pressed(canvas):
    # switch from main menu to
    # play screen
    canvas.data.highScores=False
    canvas.data.mainMenu=False
    canvas.data.instructions=False
    #print "i am clicking play", canvas.data.mainMenu
    redrawAll(canvas)

def button7Pressed(canvas):
    # Speed Round
    canvas.data.speedRound=True
    canvas.data.mainMenu=False
    #print "i am clicking play", canvas.data.mainMenu
    redrawAll(canvas)

def button8Pressed(canvas):
    # Sound
    if(canvas.data.sound==True):canvas.data.sound=False
    else:
        canvas.data.sound=True
    redrawAll(canvas)

def button9Pressed(canvas):
    # High Scores
    canvas.data.highScores=True
    canvas.data.instruction=False
    canvas.data.mainMenu=False
    redrawAll(canvas)

def button10Pressed(canvas):
    # go back to main menu
    canvas.data.mainMenu=True
    canvas.data.instructions=False
    canvas.data.highScores=False
    canvas.data.time=120
    canvas.data.play=False
    redrawAll(canvas)


def timerFired(canvas):
    board=canvas.data.boogleBoard
    redrawAll(canvas)
    canvas.data.count+=1
    #print (canvas.data.play,canvas.data.isPaused,canvas.data.gameOver)
    if(canvas.data.count%4==0 and canvas.data.play==True
       and canvas.data.isPaused==False):
       #print "you are in replay"
       canvas.data.time-=1
    delay = 250 # milliseconds
    if(canvas.data.play==True):
        if(canvas.data.time>0):
            #print "time > 0"
            pass
            #getMove(canvas,board)
        else:
            #print "game is Over"
            if(inTopScores(canvas,canvas.data.score) and canvas.data.score>0):
                inFile=open("scores.txt",'a')
                inFile.write(str(canvas.data.score)+"\n")
                inFile.close()
                canvas.data.play=False
                #timer reached 0! Game is over
                canvas.data.gameOver=True
    def f():
       timerFired(canvas)
    canvas.after(delay, f)

def inTopScores(canvas,score):
    inFile=open("scores.txt",'r')
    scoresList=[]
    for line in inFile:
        scores=line.strip()
        scores=int(scores)
        scoresList.append(scores)
    scoresList.append(score)
    sortScoresList=sorted(scoresList)
    if(len(sortScoresList)>10):
        if(len(sortScoresList)-sortScoresList.index(score)>10):
            return False
        else:
            return True
    return True         


def redrawAll(canvas):
    canvas.delete(ALL)
    canvasWidth=canvas.data.width
    if(canvas.data.mainMenu==True):
        #print "load Main menu", canvas.data.mainMenu
        b6 = canvas.data.button6
        canvas.create_window(canvasWidth/2, 240, window=b6)
        b5=canvas.data.button5
        canvas.create_window(canvasWidth/2, 280, window=b5)
        b7 = canvas.data.button7
        canvas.create_window(canvasWidth/2, 320, window=b7)
        b8 = canvas.data.button8
        canvas.create_window(canvasWidth/2, 360, window=b8)
        b9 = canvas.data.button9
        canvas.create_window(canvasWidth/2, 400, window=b9)
        loadMainMenu(canvas)
    elif(canvas.data.instructions==True):
        b6 = canvas.data.button6
        canvas.create_window(canvasWidth/2, 640, window=b6)
        b10 = canvas.data.button10
        canvas.create_window(canvasWidth/2-80, 640, window=b10)
        loadInstructions(canvas)
    elif(canvas.data.highScores==True):
        b6 = canvas.data.button6
        canvas.create_window(canvasWidth/2, 640, window=b6)
        b10 = canvas.data.button10
        canvas.create_window(canvasWidth/2-80, 640, window=b10) 
        loadHighScores(canvas)
    else:
        #print "i am drawring buttons"
        if canvas.data.gameOver==True:
           canvas.data.play=False
           #game is over pause everything.
        canvasWidth=canvas.data.width
        canvasHeight=canvas.data.height
        canvas.delete(ALL)
        #score!
        canvas.create_text(100, 600, text="Score:",
                           font=("Helvetica", 18, "bold"), fill="white")
        #display timer
        canvas.create_text(600, 100, text="Time:",
                           font=("Helvetica", 18, "bold"), fill="white")
        canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="blue")
        b1 = canvas.data.button1
        canvas.create_window(300, 600, window=b1)
        b2 = canvas.data.button2
        canvas.create_window(302, 640, window=b2)
        b3 = canvas.data.button3
        canvas.create_window(680, 600, window=b3)
        b4 = canvas.data.button4
        canvas.create_window(680, 640, window=b4)
        b10 = canvas.data.button10
        canvas.create_window(760, 22, window=b10)
        
        #drawListBox(canvas)
        drawGuessedWords(canvas)
        drawBoogleBoard(canvas)

def loadHighScores(canvas):
    canvasWidth=canvas.data.width
    canvasHeight=canvas.data.height
    letterScores=canvas.data.letterScores
    margin = canvas.data.margin
    #make Background
    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="blue",width=0)
    canvas.create_text(canvasWidth/2, 140, text="High Scores",
                           font=("Helvetica", 46, "bold"), fill="green")
    inFile=open("scores.txt",'r')
    scoresList=[]
    for line in inFile:
        score=line.strip()
        score=int(score)
        scoresList.append(score)
    sortScoresList=sorted(scoresList)
    y=220
    for index in range(len(sortScoresList)):
        canvas.create_text(canvasWidth/2, y, text=str(sortScoresList[len(sortScoresList)-1-index]),
                           font=("Helvetica", 20, "bold"), fill="red")
        y+=26
    inFile.close()
    b6 = canvas.data.button6
    canvas.create_window(canvasWidth/2, 640, window=b6)


def drawGuessedWords(canvas):
    if(canvas.data.play==True):
        guessedWords=canvas.data.guessedWords
        dictionary=canvas.data.dictionary
        board=canvas.data.boogleBoard
        pressedLetters=canvas.data.pressedLetters
        y=60
        x=20
        font=18
        threshold=550
        color="red"
        if(len(guessedWords)>24):
            for word in guessedWords[len(guessedWords)-25:len(guessedWords)]:
                color="red"
                if(word in dictionary and onBoard(board,word.upper())):color="green" 
                canvas.create_text(100, y, text=word,
                               font=("Helvetica", font, "bold"), fill=color)
                y+=x
            cx=80
            for letter in pressedLetters:
                #draw Words
                canvas.create_text(cx, y, text=letter,
                               font=("Helvetica", font, "bold"), fill=color)
                cx+=12
        else:  
            for word in guessedWords:
                #draw Words
                if (y>threshold):
                    y=60
                    x-=4
                    font-=4
                color="red"
                if(word in dictionary and onBoard(board,word.upper())):color="green" 
                canvas.create_text(100, y, text=word,
                               font=("Helvetica", font, "bold"), fill=color)
                y+=x
            cx=80
            for letter in pressedLetters:
                #draw Words
                canvas.create_text(cx, y, text=letter,
                               font=("Helvetica", font, "bold"), fill=color)
                cx+=12
    
def rotateBoard(canvas):
    board=canvas.data.boogleBoard
    newPiece=[]
    for col in xrange(len(board[0])):
        column=[]
        for row in xrange(len(board)):
            column+=[board[row][col]]
        newPiece+=[column]
    newPiece.reverse()
    #print canvas.data.boogleBoard
    canvas.data.boogleBoard=newPiece
    #-print canvas.data.boogleBoard
#mainloop()

def loadMainMenu(canvas):
    canvasWidth=canvas.data.width
    canvasHeight=canvas.data.height
    letterScores=canvas.data.letterScores
    margin = canvas.data.margin
    #make Background
    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="blue",width=0)
    canvas.create_text(canvasWidth/2, 140, text="Boggle",
                           font=("Helvetica", 46, "bold"), fill="green")
    if(canvas.data.sound==True):sound="ON"
    else:
        sound="OFF"
    canvas.create_text(canvasWidth/2+60, 360, text=sound,
                           font=("Helvetica", 20, "bold"), fill="green")
    
def loadInstructions(canvas):
    canvasWidth=canvas.data.width
    canvasHeight=canvas.data.height
    letterScores=canvas.data.letterScores
    margin = canvas.data.margin
    #make Background
    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="blue",width=0)
    msg="Boggle is an interesting game where\nthe user is given a randomized 4x4 board and\ntheir goal is to find as many words as \npossible for the highest score. Click start\n to begin, and type or click on the screen\n to make words. Hit return to get a score"
    canvas.create_text(canvasWidth/2, 100, text="Instructions",
                           font=("Helvetica", 38, "bold"), fill="green")
    canvas.create_text(canvasWidth/2, 260, text=msg,
                           font=("Helvetica", 26, "bold"), fill="green")
    b6 = canvas.data.button6
    canvas.create_window(canvasWidth/2, 640, window=b6)
    

def loadBoogleBoard(canvas):
    #print "in load boogle Board"
    rows=canvas.data.rows
    cols=canvas.data.cols
    boogleBoard=[]
    #create 2d matrix
    for row in range(rows):boogleBoard+=[[0]*cols]
    #load random letters to the board
    possibleLetters=string.ascii_uppercase
    for row in range(rows):
       for col in range(cols):
          boogleBoard[row][col]=possibleLetters[random.randint
                                                (0,len(possibleLetters)-1)]
    canvas.data.boogleBoard=boogleBoard
    boggleSolver = BoggleSolver(canvas.data.boogleBoard)
    totalWords = boggleSolver.found_words
    canvas.data.totalWords=len(totalWords)
    highestScore=bestScore(canvas)
    canvas.data.bestScore=highestScore
    #print boogleBoard
    

def loadFixedBoggleBoard(canvas):
    board=[["S", "E","R", "S"],
	   ["P", "A","T","G"],
           ["L", "I", "N", "D"],
           ["S", "E","R", "S"]]
    canvas.data.boogleBoard=board

def drawBoogleBoard(canvas):
    #print "made it to draw Boogle Board"
    boogleBoard=canvas.data.boogleBoard
    rows=canvas.data.rows
    cols=canvas.data.cols
    for row in range(rows):
       for col in range(cols):
          drawBoogleCell(canvas,boogleBoard,row,col)

def drawBoogleCell(canvas,boogleBoard,row,col):
    canvasWidth=canvas.data.width
    canvasHeight=canvas.data.height
    letterScores=canvas.data.letterScores
    margin = canvas.data.margin
    TopMargin=margin*2
    cellSize = canvas.data.cellSize
    leftShift=260
    left = leftShift+margin + col * cellSize
    right = left + cellSize
    top = TopMargin + row * cellSize
    bottom = top + cellSize
    #print left,top,right,bottom
    if(canvas.data.isPaused==True):
        canvas.create_rectangle(left, top, right, bottom, fill="gray")
        canvas.create_text(500,300, text="PAUSE",
                       font=("Helvetica", 72, "bold"), fill="green")
    else:    
        canvas.create_rectangle(left, top, right, bottom, fill="orange",width=3)
        cx=(left+right)/2
        cy=(top+bottom)/2
        textX=cx-44
        textY=cy-44
        #print canvas.data.clickPiece
        clickedPiece=canvas.data.clickPiece
        #print clickedPiece
        for c in clickedPiece:
            if (c==(row,col)):
                canvas.create_rectangle(left, top, right, bottom, fill=canvas.data.color,width=3)
                canvas.create_text(cx, cy, text=boogleBoard[row][col] ,
                           font=("Helvetica", 32, "bold"), fill="blue")
                canvas.create_text(textX, textY, text=letterScores[ord(boogleBoard[row][col])-65],
                           font=("Helvetica", 18, "bold"), fill="white")
        #text in top left corner
        #print ord(boogleBoard[row][col])-65,boogleBoard[row][col]
        canvas.create_text(textX, textY, text=letterScores[ord(boogleBoard[row][col])-65],
                           font=("Helvetica", 18, "bold"), fill="white")    
        #draw letter
        canvas.create_text(cx, cy, text=boogleBoard[row][col] ,
                           font=("Helvetica", 32, "bold"), fill="white")
    canvas.data.scoreText="Score="+str(canvas.data.score)
    #score!
    canvas.create_text(100, 600, text=canvas.data.scoreText,
                       font=("Helvetica", 22, "bold"), fill="white")
    canvas.create_text(140, 640, text="Best Score:"+str(canvas.data.bestScore),
                       font=("Helvetica", 18, "bold"), fill="white")
    #displaytimer
    canvas.data.timerText="Time="+str(canvas.data.time)
           
    canvas.create_text(340, 26, text=canvas.data.timerText,
                       font=("Helvetica", 22, "bold"), fill="white")
    canvas.create_text(100, 24, text="Words:"+str(canvas.data.correctWords)+"/"+str(canvas.data.totalWords),
                       font=("Helvetica", 18, "bold"), fill="white")

def score(canvas,move):
    board=canvas.data.boogleBoard
    #make sure game is going
    if(canvas.data.play==False or canvas.data.isPaused==True):
        pass
    else:
        letterScore=canvas.data.letterScores
        score=0
        word=""
        dictionary=canvas.data.dictionary
        for index in range(len(move)):
            word+=move[index]
        #make sure word hasent already been guessed
        #print canvas.data.guessedWords
        if(canvas.data.sound==True):playSound(canvas,True,word)
        if(word in canvas.data.guessedWords):
            pass
        else:
            #print "i am in score"
            canvas.data.guessedWords+=[word]
            if(word in canvas.data.dictionary):
                if(len(word)<=2):
                    pass
                else:
                    #print onBoard(board,word)
                    if(onBoard(board,word.upper())==True):
                        if(canvas.data.speedRound==True):
                            canvas.data.correctWords+=1
                            canvas.data.score+=13
                        else:
                            #correct Guess word
                            canvas.data.correctWords+=1
                            for c in word:
                                position=ord(c)-97
                                #print position
                                value=letterScore[position]
                                score+=value
                            if(len(word)>5):
                                canvas.data.score+=score*2
                            else:
                                canvas.data.score+=score

def onBoard(board,word):
   repeatedChar=[]
   for row in range(len(board)):
      for col in range(len(board[0])):
         letter=word[0]
         if(board[row][col]==word[0]):
            #check all the letters that word start with
            if(searchWord(board,word,letter,row,col,repeatedChar)==True):
               return True
   return False

def letterOnBoard(board,letter):
   for row in range(len(board)):
      for col in range(len(board[0])):
         if(board[row][col]==letter):
            #check all the letters that word start with
            return True
   return False

def lettersAdjacent(board,letter,previous,startRow,startCol):
    rows=len(board)
    cols=len(board[0])
    for drow in xrange(-1,2):
         for dcol in xrange(-1, 2):
            boardRow = startRow+drow
            boardCol = startCol+dcol
            if ((boardRow < 0) or (boardRow >= rows) or
                (boardCol < 0) or (boardCol >= cols)):
               pass
            else:
               boardLetter=board[boardRow][boardCol]
               if(boardLetter==previous):return True
    return False

def findRowCol(board,letter):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if(board[row][col]==letter):
                return (row,col)

def searchWord(board,word, letter, startRow, startCol,repeatedChar):
   rows=len(board)
   cols=len(board[0])
   #if (word.find(letter) not in repeatedChar and noRepeats(word,letter)==False): 
    #   repeatedChar+=[word.find(letter)]
   #print letter, word[len(word)-1]
   #print (letter==word[len(word)-1]),letterOnBoard(board,letter),lettersAdjacent(board,letter,word[len(word)-2],startRow,startCol)
   if((letter==word[len(word)-1])and (letterOnBoard(board,letter))and
                                     lettersAdjacent(board,letter,word[len(word)-2],startRow,startCol)):
      return True
   if((letter==word[len(word)-1])):return False
   else:
      for drow in xrange(-1,2):
         for dcol in xrange(-1, 2):
            boardRow = startRow+drow
            boardCol = startCol+dcol
            if ((boardRow < 0) or (boardRow >= rows) or
                (boardCol < 0) or (boardCol >= cols)):
               pass
            else:
               boardLetter=board[boardRow][boardCol]
               if(boardLetter==letter):
                  if(noRepeats(word,letter)==True):
                     # print "no repeat"
                      nextletter=word[word.find(letter)+1]
                  else:
                      #print "there is a repeat" ,letter, noRepeats(word,letter)
                      if word.find(letter) not in repeatedChar:
                          repeatedChar+=[word.find(letter)]
                          nextletter=word[word.find(letter)+1]
                      else:
                          #print letter, "checking next Index", repeatedChar , findNextIndex(word,letter,repeatedChar)
                          nextletter=word[findNextIndex(word,letter,repeatedChar)+1]
                          repeatedChar+=[findNextIndex(word,letter,repeatedChar)]
                  #print letter,boardLetter,nextletter
                  solution=searchWord(board,word,nextletter,boardRow,boardCol,repeatedChar)
                  if(solution!=None):
                     return solution
                  #solution=searchWord(board,word,letter,startRow,startCol)                
      return None

def findNextIndex(word,letter,repeatedChar):
    for index in range(len(word)):
        if(letter==word[index]):
            if(index not in repeatedChar):return index
    

def noRepeats(word,letter):
    count=0
    for c in word:
        if(c==letter):
            count+=1
    if(count>1):return False
    return True

def getDictionary(canvas):
    board=canvas.data.boogleBoard
    d=dict()
    f=open("dictionary.txt")
    try:
       for line in f:
          word=line[0:line.find(" ")].lower()      
          #if(onBoard(board,word.upper())==True):canvas.data.totalWords+=1
          d[word]=word
    finally:
       f.close()
    return d

def isLegalMove(canvas,word):
    #checks if word is on the board
    board=canvas.data.boogleBoard
    dictionary=canvas.data.dictionary

def bestScore(canvas):
    board=canvas.data.boogleBoard
    #make sure game is going
    letterScore=canvas.data.letterScores
    totalScore=0
    dictionary=canvas.data.dictionary
    boggleSolver = BoggleSolver(canvas.data.boogleBoard)
    totalWords = boggleSolver.found_words
    print len(totalWords)
    for word in totalWords:
        individualScore=0
        for c in word:
            position=ord(c)-97
            #print position
            value=letterScore[position]
            individualScore+=value
        #print canvas.data.bestScore,score,word
        if(len(word)>5):
            totalScore+=individualScore*2
        else:
            totalScore+=individualScore
    return totalScore
    
   
def init(root,canvas):
    #note they should be capital
    letterScores = [
   #  a, b, c, d, e, f, g, h, i, j, k, l, m
    1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3,
   #  n, o, p, q, r, s, t, u, v, w, x, y, z
    1, 1, 3,10, 1, 1, 1, 1, 4, 4, 8, 4,10]
    loadFixedBoggleBoard(canvas)
    #loadBoogleBoard(canvas)
    dictionary=getDictionary(canvas)
    canvas.data.dictionary=dictionary
    canvas.data.letterScores=letterScores
    boggleSolver = BoggleSolver(canvas.data.boogleBoard)
    totalWords = boggleSolver.found_words
    #print totalWords
    canvas.data.score=0
    canvas.data.count=0
    canvas.data.time=120
    canvas.data.totalWords=len(totalWords)
    highestScore=bestScore(canvas)
    canvas.data.bestScore=highestScore
    #print dictionary
    canvas.data.correctGuesses=[]
    canvas.data.isPaused=False
    canvas.data.play=False
    canvas.data.speedRound=False
    canvas.data.gameOver=False
    canvas.data.pressedLetters=[]
    canvas.data.guessedWords=[]
    canvas.data.clickPiece=[]
    canvas.data.sound=False
    canvas.data.info = "Key Events Demo"
    canvas.data.mainMenu=True
    canvas.data.correctWords=0
    canvas.data.instructions=False
    canvas.data.highScores=False
    #########
    #BUTTONS!#
    ##########
    def b1Pressed(): button1Pressed(canvas)
    b1 = Button(root, text="Start", command=b1Pressed)
    canvas.data.button1=b1
    def b2Pressed(): button2Pressed(canvas)
    b2 = Button(root, text="Pause", command=b2Pressed)
    canvas.data.button2=b2
    def b3Pressed(): button3Pressed(canvas)
    b3 = Button(root, text="Shuffle", command=b3Pressed)
    canvas.data.button3=b3
    # Here is the local function and "canvas" is in the closure
    def b4Pressed(): button4Pressed(canvas)
    b4 = Button(root, text="Rotate", command=b4Pressed)
    canvas.data.button4=b4
    canvas.pack()
    def b6Pressed(): button6Pressed(canvas)
    b6 = Button(root, text="Play!", command=b6Pressed)
    canvas.data.button6=b6
    canvas.pack()
    def b5Pressed(): button5Pressed(canvas)
    b5 = Button(root, text="Instructions", command=b5Pressed)
    canvas.data.button5=b5
    canvas.pack()
    def b7Pressed(): button7Pressed(canvas)
    b7 = Button(root, text="SpeedRound", command=b7Pressed)
    canvas.data.button7=b7
    canvas.pack()
    def b8Pressed(): button8Pressed(canvas)
    b8 = Button(root, text="Sound", command=b8Pressed)
    canvas.data.button8=b8
    canvas.pack()
    def b9Pressed(): button9Pressed(canvas)
    b9 = Button(root, text="High Scores", command=b9Pressed)
    canvas.data.button9=b9
    canvas.pack()
    def b10Pressed(): button10Pressed(canvas)
    b10 = Button(root, text="Main Menu", command=b10Pressed)
    canvas.data.button10=b10
    canvas.pack()
    

def run():
    # create the root and the canvas
    root = Tk()
    margin=20
    cellSize=130
    canvasWidth=830
    canvasHeight=700
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    # Set up canvas data and call init
    root.canvas = canvas.canvas = canvas
    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin=margin
    canvas.data.cellSize=cellSize
    canvas.data.width=canvasWidth
    canvas.data.height=canvasHeight
    canvas.data.rows=4
    canvas.data.cols=4
    init(root,canvas)
    # set up events
    def f(event):mousePressed(canvas,event)
    root.bind("<Button-1>", f)
    root.bind("<Key>", lambda event: keyPressed(canvas,event))
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()

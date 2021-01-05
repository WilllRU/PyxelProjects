import pyxel

class Note:
    def __init__(self, x, y, l):
        self.x = x
        self.y = y
        self.l = l
        self.hbp = False

class Combo:
    def __init__(self, s, color):
        self.s = s
        self.color = color

class App:
    def __init__(self):

        #Game Settings
        self.gamefps = 60
        self.timedilation = 3 # DO NOT CHANGE THIS VALUE
        self.play = False

        #Song Vars
        self.barPosY = 0
        self.songB = 0
        self.songL = 0
        self.bPos1 = 20
        self.bPos2 = 43
        self.speed = 0.5

        #Button Vars
        self.posC = {self.bPos1:1, self.bPos2:2}

        #Point System
        self.combo = 0
        self.score = 0
        self.points = 300
        self.pText = Combo("", 0)

        #Notes of the song

        self.notes = {}
        self.notes[1] = [Note(self.bPos1, 0, 0),Note(self.bPos1, -20, 0), Note(self.bPos1, -40, 0), Note(self.bPos2, -60, 0),Note(self.bPos2, -80, 0),Note(self.bPos2, -100, 0)]
        self.notes[2] = [Note(self.bPos2, -20, 0)]
        self.notes[3] = [Note(self.bPos2, -50, 100)]
        self.notes[4] = [Note(self.bPos1, 0, 0),Note(self.bPos2, 0, 0), Note(self.bPos2, -20, 0), Note(self.bPos2, -50, 100)]

        self.aNote = []
        pyxel.init(200, 200, caption = "Rhythm Test", fps = self.gamefps )
        #pyxel.image(0).load(0, 0, "kirbcodePyxel.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.play == True:
            self.songL += 1

        self.playerinput()

    def playerinput(self):

        if pyxel.btnp(pyxel.KEY_P):
            self.play = True

        if pyxel.btnp(pyxel.KEY_Z):
            self.button(True, self.bPos1)

        if pyxel.btnr(pyxel.KEY_Z):
            self.button(False, self.bPos1)
        
        if pyxel.btnp(pyxel.KEY_X):
            self.button(True, self.bPos2)

        if pyxel.btnr(pyxel.KEY_X):
            self.button(False, self.bPos2)
            


    def button(self, hold, btn):
        for aN in self.aNote:
            offset = 0
            if not hold and aN.l != 0:
                offset = aN.l
                
            if (aN.x == btn):
                if (aN.y >= pyxel.height - 30 - 15 + offset):
                    aN.hbp = True
                    print (offset)
                    print ("Button: " + str(hold))
                    if hold:
                        self.hitbutton(aN, offset)
                    if (aN.l == 0 and hold):
                        self.aNote.remove(aN)
                if (aN.l != 0 and not hold and aN.hbp):
                    self.hitbutton(aN, offset)
                    self.aNote.remove(aN)
                return
                

    def hitbutton(self, note, offset):
            difference = abs(note.y - (pyxel.height - 30 + offset))
            self.combo += 1
            if difference < 3:
                self.score += (250 * self.combo)
                self.pText = Combo("Amazing\n  250", 6)
                
            elif difference < 6:
                self.score += (150 * self.combo)
                self.pText = Combo("Great\n 150", 5)

            elif difference < 8:
                self.score += (100 * self.combo)
                self.pText = Combo("Good\n 100", 4)

            elif difference < 11:
                self.score += (50 * self.combo)
                self.pText = Combo("OK\n50", 3)

            else:
                self.combo = 1
                self.pText = Combo("Miss", 2)
            self.pText.s += " x" + str(self.combo)
            #print(self.pText)

    def draw(self):

        pyxel.cls(0)
        pyxel.text(80, 41, "Progress is being made...", pyxel.frame_count % 16)
        #pyxel.blt(140, 66, 0, 0, 0, 48, 48)
        # to set the time before a new bar is played
        if self.songL % ((self.gamefps * self.timedilation) / self.speed) == 1:
            self.songB += 1
            self.barPosY = 10
            print (self.songB)
            for note in self.notes.get(self.songB, []):
                self.aNote.append(note)

        for aN in self.aNote:
            aN.y += self.speed
            # This is to remove any active blocks that were missed  
            if aN.y - aN.l >= pyxel.height:
                self.aNote.remove(aN)
                continue
            pyxel.rect(aN.x + 1, aN.y - aN.l, 18, 8 + aN.l, self.posC[aN.x])
        
        pyxel.line(18, self.barPosY,64,self.barPosY,7)
        #Menu
        if not self.play:
            pyxel.text(100,100, "Press \'p\' to play", 7)
        else:
            self.barPosY += self.speed

        #Background lines
        pyxel.line(18, 0, 18, pyxel.height, 7)
        pyxel.line(41, 0, 41, pyxel.height, 7)
        pyxel.line(64, 0, 64, pyxel.height, 7)

        #Buttons
        pyxel.rectb(20, 170, 20, 10, 1) #color 1 when pressed
        if pyxel.btn(pyxel.KEY_Z):
            pyxel.rect(22, 172, 16, 6, 1)
        pyxel.rectb(43, 170, 20, 10, 2) #color 2 when pressed
        if pyxel.btn(pyxel.KEY_X):
             pyxel.rect(45, 172, 16, 6, 2)

        #Score system
            #Total Score
        pyxel.text(70, 0, str(self.score) +" x " + str(self.combo), 7)
            #Point Text
        pyxel.text(100, 100, self.pText.s, self.pText.color)

        #Debug
        #pyxel.text(0, 0, "SongB = " + str(self.songL), 7)
        #pyxel.text(0, 10, str(pyxel.btn(pyxel.KEY_X)), 7)
        #pyxel.text(90, 10,"Bar Length in sec = " + str((self.timedilation) / self.speed), 7 )
        

App()
from fieldgen import fieldgen
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QButtonGroup, QWidgetAction
import sys
import random
from PyQt6.QtGui import QAction
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QTimer
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,400,720)
        self.setWindowTitle("Light it up")
        self.w = 0
        self.h = 0
        self.sec = 0 #Seconds 
        self.scl = 35 #Square cell length
        
        self.endmessage = QtWidgets.QMessageBox(self)
        self.endmessage.hide()


        self.tiletexture = ['n0.png','n1.png','n2.png','n3.png','n4.png','n5.png','n6.png','n7.png','n8.png','mine.png']
        self.numtexture = ['zero.png','one.png','two.png','three.png','four.png','five.png','six.png','seven.png','eight.png','nine.png']
        
        self.btns = [] #Array for buttons
        self.mode = 0 #Marking/opening mode
        
        self.chmodbtn = QtWidgets.QPushButton(self)
        self.chmodbtn.clicked.connect(self.change_mod)
        self.chmodbtn.setStyleSheet("background-image : url(Textv/point);")
        
        self.create_menubar()
        self.create_timer()
        self.create_mineflags_conunter()
    def counter_update(self):
        self.mncount1.setStyleSheet(f"background-image : url(Textv/{self.numtexture[self.m//100]});")
        self.mncount2.setStyleSheet(f"background-image : url(Textv/{self.numtexture[self.m//10%10]});")
        self.mncount3.setStyleSheet(f"background-image : url(Textv/{self.numtexture[self.m%10]});")        

    def create_timer(self):
        self.timer=QTimer(self)
        self.started = False
        self.timer.timeout.connect(self.timerx)
        self.rect1 = QtWidgets.QLabel(self)
        self.rect2 = QtWidgets.QLabel(self)
        self.rect3 = QtWidgets.QLabel(self)
        self.rect1.setStyleSheet(f"background-image : url(Textv/zero);")
        self.rect2.setStyleSheet(f"background-image : url(Textv/zero);")
        self.rect3.setStyleSheet(f"background-image : url(Textv/zero);")
    def create_menubar(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.newgamemenu = self.menubar.addMenu("New game")
        self.newbie = QAction("Newbie",self)
        self.newbie.triggered.connect(self.dnewbie)
        self.amateur = QAction("Amateur",self)
        self.amateur.triggered.connect(self.damateur)
        self.professional = QAction("Proffesional",self)
        self.professional.triggered.connect(self.dprof)
        self.newgamemenu.addAction(self.newbie)
        self.newgamemenu.addAction(self.amateur)
        self.newgamemenu.addAction(self.professional)
        self.setMenuBar(self.menubar)
    def create_mineflags_conunter(self):
        self.mncount1 = QtWidgets.QLabel(self)
        self.mncount2 = QtWidgets.QLabel(self)
        self.mncount3 = QtWidgets.QLabel(self)
        self.mncount1.setStyleSheet(f"background-image : url(Textv/zero);")
        self.mncount2.setStyleSheet(f"background-image : url(Textv/zero);")
        self.mncount3.setStyleSheet(f"background-image : url(Textv/zero);")
        self.mncount1.setGeometry(0,30,29,50)
        self.mncount2.setGeometry(29,30,29,50)
        self.mncount3.setGeometry(58,30,29,50)
    #This procedure updates information about a grid(amount of cells, mines placement, etc.)
    #And makes buttons that represent cells
    
    def field_configuration(self,field,h,w,m):
        self.chmodbtn.setEnabled(True)
        self.sec = 0
        self.opennum = 0
        self.started = False
        self.btns = [[ [QtWidgets.QPushButton(self),self.tiletexture[field[i][j][0]],0] for j in range(w)]for i in range(h)]
        self.btn_grp= QButtonGroup()
        self.field = field[:]
        self.setGeometry(0,0,w*35,h*35+90)
        self.btn_grp.setExclusive(True)
        self.h = h
        self.w = w
        self.m = m
        self.mines = m
        #Changing number of remained mineflags in the ui
        self.counter_update()
        #Relocation of ui elements
        self.rect1.setGeometry(self.w * 35 - 29 * 3 ,30,29,50 )
        self.rect2.setGeometry(self.w * 35 - 29 * 2 ,30,29,50 )
        self.rect3.setGeometry(self.w * 35 - 29 * 1 ,30,29,50 )
        self.chmodbtn.setGeometry(((w * self.scl) // 2 )-25, 30, 50, 50)
        #Setting all cells textures to closed ones
        for i in range(h):
            for j in range(w):
                self.btns[i][j][0].setGeometry(j*35,90+i*35,35,35)
                self.btns[i][j][0].show()
                self.btns[i][j][0].setStyleSheet(f"background-image : url(Textv/closed);")
                
                self.btns[i][j][0].setObjectName(str(i*w+j))
                self.btn_grp.addButton(self.btns[i][j][0],i*w+j)

        self.btn_grp.buttonPressed.connect(self.button_pressed)
        self.btn_grp.buttonReleased.connect(self.button_released)
    def button_pressed(self,btn):#Different actions depending button and grid status
        t=self.btn_grp.id(btn)
        h = t // self.w
        w = t % self.w
        #self.pressedbutton = t
        if self.mode == 0:#Cell open mode
            if self.btns[h][w][2] == 0: #Pressed cell is closed
                self.btns[h][w][0].setStyleSheet(f"background-image : url(Textv/n0);")
            elif self.btns[h][w][2] == 1:#Pressed cell is opened
                minemarks = 0
                for i in self.field[h][w][1]:#Counting amount of mine marks nearby
                    if (self.btns[i[0]][i[1]][2] == 2):
                        minemarks+=1
                if minemarks < self.field[h][w][0]:#
                    for i in self.field[h][w][1]:
                        if (self.btns[i[0]][i[1]][2] == 0):
                            self.btns[i[0]][i[1]][0].setStyleSheet(f"background-image : url(Textv/n0);")
    def button_released(self,btn):
        t=self.btn_grp.id(btn)
        h = t // self.w
        w = t % self.w
        if self.mode == 0:
            if self.btns[h][w][2] == 0:
                self.opent(t)
            elif self.btns[h][w][2] == 1:
                for i in self.field[h][w][1]:
                    if (self.btns[i[0]][i[1]][2] == 0):
                        self.btns[i[0]][i[1]][0].setStyleSheet(f"background-image : url(Textv/closed);")
        if self.mode == 1:
            if self.btns[h][w][2]==0:
                if self.m > 0:
                    self.m-=1
                    self.btns[h][w][2]=2
                    self.btns[h][w][0].setStyleSheet(f"background-image : url(Textv/fl);")
                else:
                    self.btns[h][w][2]=3
                    self.btns[h][w][0].setStyleSheet(f"background-image : url(Textv/q);")
            elif self.btns[h][w][2]==2:
                self.btns[h][w][2]=3
                self.m+=1
                self.btns[h][w][0].setStyleSheet(f"background-image : url(Textv/q);")
            elif self.btns[h][w][2]==3:
                self.btns[h][w][2]=0
                self.btns[h][w][0].setStyleSheet(f"background-image : url(Textv/closed);")
            self.counter_update()
    @QtCore.pyqtSlot()
    def timerx(self):
        self.sec+=1

        if self.sec == 999:
            self.timer.stop()
        self.rect1.setStyleSheet(f"background-image : url(Textv/{self.numtexture[self.sec//100]});")
        self.rect2.setStyleSheet(f"background-image : url(Textv/{self.numtexture[self.sec//10%10]});")
        self.rect3.setStyleSheet(f"background-image : url(Textv/{self.numtexture[self.sec%10]});")
    def a(self):
        self.btn_grp.buttonClicked.connect(self.button_pressed)
        pass
    #field configuration with different difficulties
    def dnewbie(self):
        self.field_configuration(fieldgen(10,10,10),10,10,10)
    def damateur(self):
        self.field_configuration(fieldgen(16,16,40),16,16,40)
    def dprof(self):
        self.field_configuration(fieldgen(16,30,99),16,30,99)

    def change_mod(self):
        self.mode = (self.mode + 1 )%2
        if self.mode == 1:
            self.chmodbtn.setStyleSheet(f"background-image : url(Textv/flag);")
        else:
            self.chmodbtn.setStyleSheet("background-image : url(Textv/point);")
    def opent(self,btn):
        if  not self.started:
            self.started = True
            self.timer.start(1000)
        h = btn//self.w
        w = btn % self.w
        self.btns[h][w][0].setStyleSheet(f"background-image : url(Textv/{self.btns[h][w][1]});")
        self.btns[h][w][2]=1
        self.opennum +=1
        if self.field[h][w][0]==9:
            self.end(False)
        elif self.field[h][w][0]==0:#Opens area of empty cells
            stack = [[h,w]]
            while len(stack) != 0:
                t = stack.pop()
                for i in self.field[t[0]][t[1]][1]:
                    if (self.field[i[0]][i[1]][0] == 0)and(self.btns[i[0]][i[1]][2] == 0):
                        stack+=[i]
                    if self.btns[i[0]][i[1]][2]!=1:
                        self.btns[i[0]][i[1]][2] = 1
                        self.btns[i[0]][i[1]][0].setStyleSheet(f"background-image : url(Textv/{self.btns[i[0]][i[1]][1]});")
                        self.opennum +=1
        if (self.w * self.h - self.opennum) == self.mines:
            self.end(True)
    def end(self,victory):
        self.timer.stop()
        self.chmodbtn.setEnabled(False)
        self.endmessage.show()
        self.endmessage.setWindowTitle("")
        for i in range(self.h):
            for j in range(self.w):

                self.btns[i][j][0].setEnabled(False)
                if not victory:
                    if self.field[i][j][0] == 9:
                        self.btns[i][j][0].setStyleSheet(f"background-image : url(Textv/{self.btns[i][j][1]});")
        if victory:
            self.endmessage.setText("You won")
        else:
            self.endmessage.setText("You lost")
app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.field_configuration(fieldgen(10,10,10),10,10,10)
app.exec()
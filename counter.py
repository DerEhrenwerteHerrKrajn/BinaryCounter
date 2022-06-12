#!/usr/bin/env python3
# 2021 nr@bulme.at
#Aufgabe gelöst durch Krajina Luka

'''
Programmierung

Auf Basis des existierenden Code-Gerüstes soll ein Modulo-16-Zähler programmiert werden, der den Zählerstand im grafischen Widget und über die LEDs am Zusatzboard anzeigt.

Spezifikationen:

    Druck auf Taster GPIO17: erhöhe Zählerstand um 1
    Druck auf Taster GPIO22: erniedrige Zählerstand um 1
    Druck auf Taster GPIO27: Zählerstand auf 0 zurücksetzen
    Der Zählvorgang wird durch die fallende Flanke beim Drücken des Tasters ausgelöst. Längeres Drücken löst keinen weiteren Zählvorgang aus.
    Der Zähler soll von 0 bis 15 zählen. Auf den Höchstwert 15 folgt wieder 0. Beim Abwärtszählen folgt auf 0 der Wert 15.
    Anzeige des Zählerstandes im Widget durch QLCDNumber dezimal.
    Anzeige des Zählerstandes am Zusatzboard: dual über die 4 LEDs (GPIO18 = MSB, GPIO25 = LSB).
    Umrechnung dezimal-dual bitte nicht mit mehrfach-if-Bedingungen, sondern mittels geeignetem Algorithmus.
    Ein funktionsfähiges Beispielprogramm ist unter bin/BinaryCounter zu finden.

Abgabe:   Hochladen auf github:

git add .
git commit -m "Abgabe"
git push origin main


button = Button(BUTTON_PIN)

button.when_pressed = say_hello
pause()

'''
from gpiozero import Button
from signal import pause
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLCDNumber,
    QVBoxLayout, QApplication)
from gpiozero import LEDBoard
from threading import Thread

DOWN_PIN = 22
RESET_PIN = 27
UP_PIN = 17
leds = LEDBoard(18, 23, 24, 25, pwm=True)

class QtButton(QObject):
    changed = pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        self.button = Button(pin) 
        self.button.when_pressed = self.gpioChange        

    def gpioChange(self):
        self.changed.emit()
        print("changed")
        gui.checker()

class Counter(QWidget):
    
    nrButtons = len(leds)
    print("Anzahl an Knöpfen: " + str(nrButtons))
    decMax = 0
    decMin = 0
    
    
    def __init__(self):
        super().__init__()
        self.initUi()
        self.count = 0
        for i in range(self.nrButtons):
            self.decMax += 2**i
        print("Maximum: " + str(self.decMax))
    def initUi(self):
        self.lcd = QLCDNumber()
        self.lcd.display(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)

        self.setLayout(vbox)
        self.setMinimumSize(400, 200)
        self.setWindowTitle('Counter')
        self.show()


    def countUp(self):
        if (self.count == self.decMax):
            self.count = self.decMin
        else: 
            self.count += 1
        self.lcd.display(self.count)
        
    def countReset(self):
        self.count = self.decMin
        self.lcd.display(self.count)
        
    def countDown(self):
        if (self.count == self.decMin):
            self.count = self.decMax
        else: 
            self.count -= 1
        self.lcd.display(self.count)
        
    def checker(self):
        for i in range(self.nrButtons):
            leds[i].off()
            if (self.count & 1<<i):
                leds[i].on()

if __name__ ==  '__main__':
    app = QApplication([])
    gui = Counter()
    buttonUp = QtButton(UP_PIN)
    buttonReset = QtButton(RESET_PIN)
    buttonDown = QtButton(DOWN_PIN)
    buttonReset.changed.connect(gui.countReset)
    buttonDown.changed.connect(gui.countDown)
    buttonUp.changed.connect(gui.countUp)
    app.exec_()
    

#buttonUp = Button(UP_PIN)
#buttonReset = Button(RESET_PIN)
#buttonDown = Button(DOWN_PIN)

#buttonUp.when_pressed = countUp
#buttonReset.when_pressed = resetCounter
#buttonDown.when_pressed = decrCounter
#pause()
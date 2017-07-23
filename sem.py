#!/usr/bin/env python3

#
#   Semestrálna práca BI-PYT - Jednoduchý grafický editor
#   Autor: Patrik Jantošovič ( jantopat )
#

from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image 
from PIL import ImageTk
from numpy import array
from numpy import rot90
from numpy import invert
from numpy import clip
from numpy import zeros
from numpy import asarray
from numpy import float
from numpy import uint8
from numba import jit

 #nové okno Tkinter
root = Tk()
root.title("Grafický editor - Jantošovič")
root.update()

# prve otvorenie programu
def getimage():
    filename = filedialog.askopenfilename(parent=root)
    return filename

# otvorenie noveho obrazka, pomocou tlacidla
def openimage():
    global img
    filename = filedialog.askopenfilename(parent=root)
    img2 = Image.open(filename)
    photo2 = ImageTk.PhotoImage(img2)
    plocha.configure(image = photo2)
    plocha.image = photo2
    img = img2

#ulozenie obrazka pomocou tlacidla
def saveimage():
    img.save("edit.jpg")

#otocenie obrazka pomocou vstavanej funkcie numpy - rot90 , 3 => o 90 stupnov vpravo
def rotateimage():
    global img
    arr = array(img)
    rotated = rot90(arr,3)
    img2 = Image.fromarray(rotated)
    photo2 = ImageTk.PhotoImage(img2)
    plocha.configure(image=photo2)
    plocha.image = photo2
    img = img2

#invertovanie farieb obrazka pomocou vstavanej funkcie numpy - invert
def inverseimage():
    global img
    arr = array(img)
    inverted = invert(arr)
    img2 = Image.fromarray(inverted)
    photo2 = ImageTk.PhotoImage(img2)
    plocha.configure(image=photo2)
    plocha.image = photo2
    img = img2

#prevod do odtienovej sedej pomocou rozobratia na pixely
# a upravy farebnych zloziek pomocou vzorca z cvicenia
def grayimage():
    global img
    arr = img.getdata()
    img2 = Image.new('RGB', img.size)
    gray_list = []
    for pixel in arr:
        gray_val = (0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])
        new_pixel = (int(gray_val), int(gray_val), int(gray_val))
        gray_list.append(new_pixel)
    img2.putdata(gray_list)
    photo2 = ImageTk.PhotoImage(img2)
    plocha.configure(image=photo2)
    plocha.image = photo2
    img = img2

#zosvetlenie obrazka pomocou prenasobenia far. zloziek pixelov koeficientom > 1
def lightimage():
    global img
    arr = img.getdata()
    light = Image.new('RGB', img.size)
    light_list = []
    for pixel in arr:
        new_pixel = (int(pixel[0] * 1.1) , int(pixel[1] * 1.1) , int(pixel[2] * 1.1))
        for p in new_pixel:
            if p > 255:
                p = 255
            if p < 0:
                p = 0
        light_list.append(new_pixel)

    light.putdata(light_list)

    photo2 = ImageTk.PhotoImage(light)
    plocha.configure(image=photo2)
    plocha.image = photo2
    img = light

#ztmavenie obrazka pomocou prenasobenie far. zlozek pixelob koeficientom < 1
def darkimage():
    global img
    arr = img.getdata()
    dark = Image.new('RGB', img.size)
    dark_list = []
    for pixel in arr:
        new_pixel = (int(pixel[0] * 0.9) , int(pixel[1] * 0.9) , int(pixel[2] * 0.9))
        for p in new_pixel:
            if p > 255:
                p = 255
            if p < 0:
                p = 0
        dark_list.append(new_pixel)

    dark.putdata(dark_list)

    photo2 = ImageTk.PhotoImage(dark)
    plocha.configure(image=photo2)
    plocha.image = photo2
    img = dark

# funkcia aplikujuca filter na farebnu zlozku obrazka
# numba jit na zrychlenie
@jit
def applyfilter(arr,filter,output):
    w,h = arr.shape
    for y in range(1,h - 2):
        for x in range(1,w - 2):
            vyrez = arr[x-1:x+2,y-1:y+2]
            output[x, y] =  (vyrez * filter).sum()

#funkcia na zvyraznenie hran obrazka pomocou filtru
def edgeimage():
    global img
    arr = asarray(img, dtype=float)
    filter = array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1],
])
    X,Y,Z = arr.shape
    out = zeros([X- 2, Y - 2, Z])
    for i in range(3):
        applyfilter(arr[:,:,i], filter, out[:,:,i])

    out_img = clip(out,0,255)
    out_img = asarray(out_img, dtype=uint8)
    edgeImg = Image.fromarray(out_img,"RGB")
    photo2 = ImageTk.PhotoImage(edgeImg)
    plocha.configure(image=photo2)
    plocha.image = photo2
    img = edgeImg
    

#Tlacidla
toolbar = Frame(root)
insertButt = Button(toolbar, text="Otvoriť súbor", command=openimage)
saveButt = Button(toolbar, text="Uložiť súbor", command=saveimage)
rotateButt = Button(toolbar, text="Otoč o 90", command=rotateimage)
inverseButt = Button(toolbar, text="Invertovať", command=inverseimage)
grayButt = Button(toolbar, text="Odtiene šedej", command=grayimage)
lightButt = Button(toolbar, text="Zosvetlenie", command=lightimage)
darkButt = Button(toolbar, text="Ztmavenie", command=darkimage)
edgeButt = Button(toolbar, text="Zvýraznenie hran", command=edgeimage)

insertButt.pack(side=LEFT, padx=2, pady=2)
saveButt.pack(side=LEFT, padx=2, pady=2)
rotateButt.pack(side=LEFT, padx=2, pady=2)
inverseButt.pack(side=LEFT, padx=2, pady=2)
grayButt.pack(side=LEFT, padx=2, pady=2)
lightButt.pack(side=LEFT, padx=2, pady=2)
darkButt.pack(side=LEFT, padx=2, pady=2)
edgeButt.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

#Uvodne vyprintovanie obrazku
img = Image.open(getimage())
photo = ImageTk.PhotoImage(img)
plocha = Label(root, image = photo)
plocha.pack(side = "bottom")

root.mainloop()

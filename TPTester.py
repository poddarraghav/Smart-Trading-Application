# -*- coding: utf-8 -*-
#!/usr/bin/env python
#nltk python library
#Logo Credit: https://logomakr.com/0Al0oe
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import sys
import requests
import json
import urllib.request
from alchemyapi import AlchemyAPI
from yahoo_finance import Share
import time
import datetime
import unicodedata
import pprint
import numpy as np
import matplotlib.finance
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinter import *
import matplotlib as mpl
import webbrowser
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import tkinter.messagebox
import tkinter.simpledialog
from PIL import Image, ImageTk
import os
import threading
from queue import Queue
from AlchemyClassWithThreading import AlchemyYahoo
import random


####################################
# init
####################################

def createsearchbarlist(data):
    if data.query!="":
        data.searchstocklist=[]
        for stockobject in data.stocklist:
            if data.query==stockobject.stock[:len(data.query)]:
                data.searchstocklist.append(stockobject)
    else:
        pass

def init(data):
    data.currentstock=None
    # There is only one init, not one-per-mode
    data.mode = "login"
    data.articlerow=6
    data.articlecol=1
    data.cellx=250
    data.celly=100
    data.starty=150
    data.startx=380
    data.endx=630
    data.stocklist=[]
    if len(data.stocklist)!=0:
        data.currentstock=data.stocklist[0]
    data.searchoutline="red"
    data.searchbar=False
    data.query=""
    data.loginuserbar=False
    data.passwordbar=False
    data.username=""
    data.password=""
    data.graphmotion=False
    data.yahoocalltimer=0
    data.dropdownmenu=False
    calculateborderdatathread=CalculateBorderDataThread(calculateborderdata,
        data)
    calculateborderdatathread.start()
    data.searchindex=None
    data.drawusername=False
    data.drawpassword=False
    data.gridmotion=False
    data.nikkeiprice=None
    data.nasdaqprice=None
    data.sandpprice=None
    data.dowprice=None
    data.oilprice=None
    data.searchstocklist=[]
    data.keywordindex=None
    createsearchbarlist(data)

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "login"): 
        LoginMousePressed(event, data)
    elif (data.mode == "main"):   
        MainMousePressed(event, data)
    elif (data.mode=="signup"):
        SignupMousePressed(event,data)
    elif (data.mode == "logout"):       
        LogoutMousePressed(event, data)

def mouseMotion(event, data):
    if (data.mode == "login"): 
        LoginMouseMotion(event, data)
    elif (data.mode == "main"):   
        MainMouseMotion(event, data)
    elif (data.mode=="signup"):
        SignupMouseMotion(event,data)
    elif (data.mode == "logout"):       
        LogoutMouseMotion(event, data)

def keyPressed(event, data):

    if (data.mode == "login"): 
        LoginKeyPressed(event, data)
    elif (data.mode == "main"):   
        MainKeyPressed(event, data)
    elif  (data.mode=="signup"):
        SignupKeyPressed(event,data)
    elif (data.mode == "logout"):       
        LogoutKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "login"): 
        LoginTimerFired(data)
    elif (data.mode == "main"):   
        MainTimerFired(data)
    elif (data.mode=="signup"):
        SignupTimerFired(data)
    elif (data.mode == "logout"):       
        LogoutTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "login"):
        LoginRedrawAll(canvas, data)
    elif (data.mode == "main"):
        MainRedrawAll(canvas, data)
    elif (data.mode=="signup"):
        SignupRedrawAll(canvas,data)
    elif (data.mode == "logout"):       
        LogoutRedrawAll(canvas, data)

####################################
# Signup mode
####################################

def setupaccount(filename,contents):
    with open(filename, "wt") as f:
        f.write(contents)

def drawusernamefaded(canvas,data):
    if len(data.username)==0:
        canvas.create_text(665,390,text="Username",fill="gray35")

def drawpasswordfaded(canvas,data):
    if len(data.password)==0:
        canvas.create_text(665,425,text="Password",fill="gray35")


def SignupMouseMotion(event,data):
    if 560<event.x<770 and 380<event.y<405:
        data.drawusername=True
    elif 560<event.x<770 and 415<event.y<440:
        data.drawpassword=True
    else:
        data.drawusername=False
        data.drawpassword=False

def SignupMousePressed(event,data):
    if 560<event.x<770 and 380<event.y<405:
        if data.username=="Enter Username":
            data.username=""
        data.loginuserbar=True
        data.passwordbar=False
        data.drawusername=False
    elif 560<event.x<770 and 415<event.y<440:
        if data.password=="Enter Password":
            data.password=""
        data.passwordbar=True
        data.loginuserbar=False
        data.drawpassword=False
    elif 560<event.x<770 and 450<event.y<475:
        setupaccount("AccountInfo/"+data.username+".txt", data.password)
        data.username=""
        data.password=""
        data.mode="login"
    pass

def SignupKeyPressed(event,data):
    if data.loginuserbar==True:
        if event.keysym!="Return":
            data.username+=event.char
        if event.keysym=="Return":
            data.loginuserbar=False
            data.passwordbar=True
        if event.keysym=="BackSpace":
            if len(data.username)>0:
                data.username=data.username[:-2]
    if data.passwordbar==True and data.loginuserbar==False:
        if event.keysym!="Return":
            data.password+=event.char
        if event.keysym=="Return":
            checkvalidpassword(data)
        if event.keysym=="BackSpace":
            if len(data.password)>0:
                data.password=data.password[:-2]
    pass

def SignupTimerFired(data):
    pass

def drawsignup(canvas,data):
    canvas.create_rectangle(560,380,770,405,outline="darkorchid4", width=2.5)
    canvas.create_rectangle(560,415,770,440,outline="darkorchid4", width=2.5)
    canvas.create_rectangle(560,450,770,475,fill="darkorchid4", width=2.5, 
        outline="darkorchid4")
    canvas.create_text(665,462, text="Make Account", fill="white", 
        font="Helvetica 12")
    canvas.create_text(665,500, text="Smart Trading", fill="darkorchid4", 
        font="Helvetica 9")

def SignupRedrawAll(canvas,data):
    if data.drawpassword==True:
        drawpasswordfaded(canvas,data)
    if data.drawusername==True:
        drawusernamefaded(canvas,data)
    drawusernamepassword(canvas,data)
    drawsignup(canvas,data)
    drawdesignlogout(canvas,data)
    logo(canvas,data)
    pass   

####################################
# Login mode
####################################

def checkfilename(data,filename,path="AccountInfo"):
    if os.path.isdir(path)==False:
        if path=="AccountInfo/"+filename:
            return True
    else:
        for file in os.listdir(path):
            checking=checkfilename(data,filename,path +"/"+file)
            if checking==True:
                return True
    return False


def errorinpassword(data):
    global canvas
    message = "Warning! Wrong Password"
    title = "Warning"
    tkinter.messagebox.showwarning(title, message)
    pass

def errorinusername(data):
    global canvas
    message = "Warning! Wrong Username"
    title = "Warning"
    tkinter.messagebox.showwarning(title, message)
    pass

def checkaccount(data):
    #Checkfilename
    #If there is file open it and check password then load the data
    account=checkfilename(data,data.username+".txt")
    if account==True:
        with open("AccountInfo/"+data.username+".txt","rt") as f:
            contents=f.read()
            info=contents.splitlines()
            if info[0]==data.password:
                if len(info)>1:
                    for stocks in info[1:]:
                        if AlchemyYahoo(stocks) not in data.stocklist:
                            data.stocklist.append(AlchemyYahoo(stocks))
                    data.currentstock=data.stocklist[0]
                    data.mode="main"
                else:
                    data.mode="main"
            else:
                return errorinpassword(data)
    else:
        return errorinusername(data)

def LoginMouseMotion(event,data):
    if 560<event.x<770 and 380<event.y<405:
        data.drawusername=True
    elif 560<event.x<770 and 415<event.y<440:
        data.drawpassword=True
    else:
        data.drawusername=False
        data.drawpassword=False


def LoginMousePressed(event, data):
    if 560<event.x<770 and 380<event.y<405:
        if data.username=="":
            data.username=""
        data.loginuserbar=True
        data.passwordbar=False
        data.drawusername=False
    elif 560<event.x<770 and 415<event.y<440:
        if data.password=="":
            data.password=""
        data.passwordbar=True
        data.loginuserbar=False
        data.drawpassword=False
    elif 560<event.x<770 and 485<event.y<510:
        data.mode="signup"
    elif 560<event.x<770 and 450<event.y<475:
        checkaccount(data)

def drawusernamepassword(canvas,data):
    canvas.create_text(665,392,text=data.username,fill="gray2")
    canvas.create_text(665,429,text="*"*len(data.password),fill="gray2")

def LoginKeyPressed(event, data):
    if data.loginuserbar==True:
        if event.keysym!="Return":
            data.username+=event.char
        if event.keysym=="Return":
            data.loginuserbar=False
            data.passwordbar=True
        if event.keysym=="BackSpace":
            if len(data.username)>0:
                data.username=data.username[:-2]
    if data.passwordbar==True and data.loginuserbar==False:
        if event.keysym!="Return":
            data.password+=event.char
        if event.keysym=="Return":
            checkaccount(data)
        if event.keysym=="BackSpace":
            if len(data.password)>0:
                data.password=data.password[:-2]

def LoginTimerFired(data):
    pass

def logo(canvas,data):
    im=Image.open("Logo.png")
    im=im.resize((180,150),Image.ANTIALIAS)
    canvas.logoimage= ImageTk.PhotoImage(im)
    canvas.create_image(data.width//2+20,300, image=canvas.logoimage)

def drawlogin(canvas,data):
    canvas.create_rectangle(560,380,770,405,outline="darkorchid4", width=2.5)
    canvas.create_rectangle(560,415,770,440,outline="darkorchid4", width=2.5)
    canvas.create_rectangle(560,450,770,475,fill="darkorchid4", width=2.5, 
        outline="darkorchid4")
    canvas.create_text(665,462, text="Sign in", fill="white", 
        font="Helvetica 12")
    canvas.create_rectangle(560,485,770,510,fill="darkorchid4", width=2.5, 
        outline="darkorchid4")
    canvas.create_text(665,496, text="No account? Create one!", fill="white", 
        font="Helvetica 12")
    canvas.create_text(665,540, text="Smart Trading", fill="darkorchid4", 
        font="Helvetica 10")

def LoginRedrawAll(canvas, data):
    if data.drawpassword==True:
        drawpasswordfaded(canvas,data)
    if data.drawusername==True:
        drawusernamefaded(canvas,data)
    drawusernamepassword(canvas,data)
    logo(canvas,data)
    drawlogin(canvas,data)
    drawdesignlogout(canvas,data)


####################################
# Main mode
####################################
alchemyapi = AlchemyAPI()

class CalculateBorderDataThread(threading.Thread):
    def __init__(self,target,data):
        threading.Thread.__init__(self)
        self.target=target
        self.data=data

    def run(self):
        self.target(self.data)

class OpenUrlClass(threading.Thread):
    def __init__(self,target,number,data):
        threading.Thread.__init__(self)
        self.target = target
        self.number = number
        self.data=data

    def run(self):
        openurl(self.number,self.data)


def openurl(number,data):
    if (data.currentstock.articledata!= None and 
    data.currentstock.articledata!=False):
        if number<len(data.currentstock.articledata):
            try:
                articles=data.currentstock.articledata
                dictionary=articles[number]
                webbrowser.open(dictionary["url"])
            except:
                pass
    

def checkurl(x,y,data):
    if data.startx<x<data.endx and data.starty<y<data.starty+data.celly:
        openurlthread = OpenUrlClass(openurl, 0,data)
        openurlthread.start()
    if (data.startx<x<data.endx and 
        data.starty+data.celly<y<data.starty+(data.celly*2)):
        openurlthread = OpenUrlClass(openurl, 1,data)
        openurlthread.start()       
    if (data.startx<x<data.endx and 
        data.starty+(data.celly*2)<y<data.starty+(data.celly*3)):
        openurlthread = OpenUrlClass(openurl, 2,data)
        openurlthread.start()  
    if (data.startx<x<data.endx and 
        data.starty+(data.celly*3)<y<data.starty+(data.celly*4)):
        openurlthread = OpenUrlClass(openurl, 3,data)
        openurlthread.start()  
    if (data.startx<x<data.endx and 
        data.starty+(data.celly*4)<y<data.starty+(data.celly*5)):
        openurlthread = OpenUrlClass(openurl, 4,data)
        openurlthread.start()  
    if (data.startx<x<data.endx and 
        data.starty+(data.celly*5)<y<data.starty+(data.celly*6)):
        openurlthread = OpenUrlClass(openurl, 5,data)
        openurlthread.start()  


def assignstock(number,data):
    if number<len(data.stocklist):
        data.currentstock=data.stocklist[number]
    
def checkstock(x,y,data):
    start=80
    end=330
    if start<x<end and data.starty<y<data.starty+data.celly:
        assignstock(0,data)
    if start<x<end and data.starty+data.celly<y<data.starty+(data.celly*2):
        assignstock(1,data)
    if start<x<end and data.starty+(data.celly*2)<y<data.starty+(data.celly*3):
        assignstock(2,data)
    if start<x<end and data.starty+(data.celly*3)<y<data.starty+(data.celly*4):
        assignstock(3,data)
    if start<x<end and data.starty+(data.celly*4)<y<data.starty+(data.celly*5):
        assignstock(4,data)
    if start<x<end and data.starty+(data.celly*5)<y<data.starty+(data.celly*6):
        assignstock(5,data)

def errormessageforadding(data):
    global canvas
    message = "Warning! Cannot Add More than Six Stocks"
    title = "Warning"
    tkinter.messagebox.showwarning(title, message)

def stockalreadyinportfolio(data):
    global canvas
    message = "Warning! You already have "+data.currentstock.companyname+" \
    in your portfolio"
    title = "Warning"
    tkinter.messagebox.showwarning(title, message)

def addstock(data):
    if len(data.stocklist)<6:
        if data.currentstock not in data.stocklist:
            data.stocklist.append(data.currentstock)
        else:
            stockalreadyinportfolio(data)
    else:
        errormessageforadding(data)

def saveaccountinfo(data):
    result=""
    with open("AccountInfo/"+data.username+".txt","rt") as f:
        contents=f.read()
    info=contents.splitlines()
    password=info[0]
    result+=password
    for eachstock in data.stocklist:
        result+="\n"+eachstock.stock
    with open("AccountInfo/"+data.username+".txt","wt") as f:
        f.write(result)
    data.mode="logout"
    data.username=""
    data.password=""
    data.currentstock=None
    data.stocklist=[]
    data.searchindex=None
    data.query=""
    data.searchoutline="red"

class GetKeywordsClass(threading.Thread):
    def __init__(self,target,number,data):
        threading.Thread.__init__(self)
        self.target=target
        self.number=number
        self.data=data

    def run(self):
        self.target(self.number,self.data)

def checkwhicharticle(x,y,data):
    if data.startx<x<data.endx and data.starty<y<data.starty+data.celly:
        data.keywordx=x
        data.keywordy=y
        data.keywordindex=0
    elif (data.startx<x<data.endx and 
        data.starty+data.celly<y<data.starty+(data.celly*2)):
        data.keywordx=x
        data.keywordy=y
        data.keywordindex=1
    elif (data.startx<x<data.endx and 
        data.starty+(data.celly*2)<y<data.starty+(data.celly*3)):
        data.keywordx=x
        data.keywordy=y
        data.keywordindex=2
    elif (data.startx<x<data.endx and 
        data.starty+(data.celly*3)<y<data.starty+(data.celly*4)):
        data.keywordx=x
        data.keywordy=y
        data.keywordindex=3
    elif (data.startx<x<data.endx and 
        data.starty+(data.celly*4)<y<data.starty+(data.celly*5)):
        data.keywordx=x
        data.keywordy=y
        data.keywordindex=4
    elif (data.startx<x<data.endx and 
        data.starty+(data.celly*5)<y<data.starty+(data.celly*6)):
        data.keywordx=x
        data.keywordy=y
        data.keywordindex=5

def drawkeywords(data,canvas):
    if (data.currentstock.articledata==None or 
        data.currentstock.articledata==False):
        return
    if data.keywordindex==None:
        return
    if len(data.currentstock.articlekeywords)<data.keywordindex+1:
        return
    keywordsfromclass=data.currentstock.articlekeywords[data.keywordindex]
    if len(keywordsfromclass)==0:
        time.sleep(.001)
    if (data.currentstock.articledata==None or 
        data.currentstock.articledata==False):
        return
    canvas.create_rectangle(data.keywordx,data.keywordy,data.keywordx+215,
        data.keywordy+250,outline="darkorchid4",fill="white")
    if type(keywordsfromclass)==set:
        keywords="Keywords:\n"
        for word in keywordsfromclass:
            keywords+=word + ", "
        canvas.create_text(data.keywordx+10,data.keywordy+10,anchor=NW,
            text=keywords.strip()[:-1],width=200)

def MainMouseMotion(event,data):
    if 717<event.x<1265 and 175<event.y<590:
        data.graphx=event.x
        data.graphy=event.y
        data.graphmotion=True
    elif (data.startx<event.x<data.endx and 
        data.starty<event.y<data.starty+(data.celly*6)):
        data.gridmotion=True
        checkwhicharticle(event.x,event.y,data)
    else:
        data.gridmotion=False
        data.graphmotion=False

def drawdropdownmenu(data,canvas):
    data.dropdown=[]
    data.dropdownarticle=[]
    celly=20
    if data.query=="":
        for row in range(len(data.stocklist)):
            for col in range(1):
                left=450+(col*data.cellx)
                top=95+(row*celly)
                if data.searchindex==None:
                    data.dropdown.append(canvas.create_rectangle(left,top,
                        left+data.cellx, 
                        top+celly, outline="violetred2", width=1,fill="white"))
                    data.dropdownarticle.append(canvas.create_text(left+20,
                        top+celly -18,anchor=NW,text=data.stocklist[row].stock))
                elif row==data.searchindex:
                    (canvas.create_rectangle(left,top,left+data.cellx, 
                        top+celly, outline="violetred2", width=1,
                        fill="darkorchid4"))
                    (canvas.create_text(left+20,top+celly -18,anchor=NW,
                        text=data.stocklist[row].stock,fill="white"))

                else:
                    (canvas.create_rectangle(left,top,left+data.cellx, 
                        top+celly, outline="violetred2", width=1,fill="white"))
                    (canvas.create_text(left+20,top+celly -18,anchor=NW,
                        text=data.stocklist[row].stock))
    else:
        if data.searchstocklist!=[]:
            for row in range(len(data.searchstocklist)):
                for col in range(1):
                    left=450+(col*data.cellx)
                    top=95+(row*celly)
                    if data.searchindex==None:
                            data.dropdown.append(canvas.create_rectangle(left,top,
                                left+data.cellx, 
                                top+celly, outline="violetred2", width=1,fill="white"))
                            data.dropdownarticle.append(canvas.create_text(left+20,
                                top+celly -18,anchor=NW,text=data.searchstocklist[row].stock))
                    elif row==data.searchindex:
                            (canvas.create_rectangle(left,top,left+data.cellx, 
                                top+celly, outline="violetred2", width=1,
                                fill="darkorchid4"))
                            (canvas.create_text(left+20,top+celly -18,anchor=NW,
                                text=data.searchstocklist[row].stock,fill="white"))

                    else:
                            (canvas.create_rectangle(left,top,left+data.cellx, 
                                top+celly, outline="violetred2", width=1,fill="white"))
                            (canvas.create_text(left+20,top+celly -18,anchor=NW,
                                text=data.searchstocklist[row].stock))

def MainMousePressed(event, data):
    checkminus(event.x,event.y,data)
    if 820<event.x<840 and 80<event.y<100:
        addstock(data)
    elif 1145<event.x<1355 and 61<event.y<86:
        saveaccountinfo(data)
    elif (data.startx<event.x<data.endx and 
        data.starty<event.y<data.starty+(data.celly*6)):
        checkurl(event.x,event.y,data)
    elif (80<event.x<80+data.cellx and 
        data.starty<event.y<data.starty+(data.celly*6)):
        checkstock(event.x,event.y,data)
    elif 450<event.x<700 and 65<event.y<95 and data.searchbar==False:
        data.searchbar=True
        data.searchoutline="darkorchid4"
        data.dropdownmenu=True
    elif 450<event.x<700 and 65<event.y<95 and data.searchbar==True:
        data.searchbar=False
        data.dropdownmenu=False
        data.searchoutline="red"

def drawlogo(canvas,data):
    im=Image.open("Finallogo.png")
    im=im.resize((150,80),Image.ANTIALIAS)
    canvas.image= ImageTk.PhotoImage(im)
    data.logo=canvas.create_image(210,40, image=canvas.image,anchor=NW)
    pass

def errormessage(data):
    global canvas
    message = "Warning! Stock Symbol Not Valid"
    title = "Warning"
    tkinter.messagebox.showwarning(title, message)

def checkvalidsymbol(data):
    try: 
        yahoo=Share(data.query)
        if yahoo.get_price()!=None:
            data.currentstock=AlchemyYahoo(data.query)
        else:
            errormessage(data)
    except:
        errormessage(data)

def removestock(data, number):
    data.stocklist.pop(number)

def drawminussign(canvas,data):
    celly=100
    for i in range(len(data.stocklist)):
        canvas.create_text(315,160+(i*celly), text="-", font="Helvetica 30", 
            fill="red")

def checkminus(x,y,data):
    celly=100
    for i in range(len(data.stocklist)):
        if 305<x<325 and 155+(i*celly)<y<170+(i*celly):
            removestock(data,i)



def MainKeyPressed(event, data):
    createsearchbarlist(data)
    if len(data.searchstocklist)==0:
        data.searchindex=None
    if data.searchbar==True:
        if event.keysym=="Down" and data.searchindex==None and len(data.stocklist)>0:
            data.searchindex=0
        elif data.searchindex!=None and event.keysym=="Return" and len(data.stocklist)>0:
            if data.query=="":
                if data.searchindex<len(data.stocklist):
                    data.currentstock=data.stocklist[data.searchindex]
            else:
                if data.searchindex<len(data.searchstocklist):
                    data.currentstock=data.searchstocklist[data.searchindex]
        elif event.keysym=="Up":
            if data.searchindex!=None and data.searchindex>0:
                data.searchindex-=1
            elif data.searchindex==0:
                data.searchindex=None
        elif event.keysym=="Down":
            if data.searchindex!=None:
                if data.query=="":
                    if data.searchindex<len(data.stocklist)-1:
                        data.searchindex+=1
                else:
                    if data.searchindex<len(data.searchstocklist)-1:
                        data.searchindex+=1
        elif event.keysym=="BackSpace":
            if len(data.query)>0:
                data.query=data.query[:-2]
        elif (event.keysym!="Return" and (event.keysym!="Up" or 
            event.keysym!="Down" or event.keysym!="BackSpace")):
            data.query+=event.char
        elif event.keysym=="Return":
            data.loadingsearch=True
            checkvalidsymbol(data)
        

def drawsearchtext(canvas,data):
    canvas.create_text(460,71, text=data.query, anchor=NW)

def MainTimerFired(data):
    createsearchbarlist(data)
    pass

def drawgrid(data,canvas):
    data.grid=[]
    for row in range(data.articlerow):
        for col in range(data.articlecol):
            left=380+(col*data.cellx)
            top=150+(row*data.celly)
            data.grid.append(canvas.create_rectangle(left,top,left+data.cellx, 
                top+data.celly, width=(2*2)-1,dash=(20,),dashoff=5,
                outline="darkorchid4"))

def drawstocksgrid(data,canvas):
    data.stocksgrid=[]
    for row in range(data.articlerow):
        for col in range(data.articlecol):
            left=80+(col*data.cellx)
            top=150+(row*data.celly)
            data.stocksgrid.append(canvas.create_rectangle(left,top,
                left+data.cellx, top+data.celly, dash=(20,),dashoff=5,
                outline="darkorchid4", width=(2*2)-1))

def drawusername(canvas,data):
    data.usernameinfo=[]
    data.usernameinfo.append(canvas.create_rectangle(0,68,170,92,
        fill="darkorchid4",width=2.5,outline="darkorchid4"))
    data.usernameinfo.append(canvas.create_text(85,78,text=data.username, 
        fill="white"))

def drawstocks(canvas,data):
    gap=0
    for stock in data.stocklist:
        stock.drawstockinfo(canvas,gap)
        gap+=1

def searchbar(canvas,data):
    data.search=[]
    data.search.append(canvas.create_text(390,70,text="Search:", anchor=NW, 
        font="Helvetica 15 italic"))
    data.search.append(canvas.create_rectangle(450,65,700,95,
        outline=data.searchoutline,width=3))


def drawbutton(canvas,data):
    data.logout=[]
    data.logout.append(canvas.create_rectangle(1145,68,1355,92,
        fill="darkorchid4",width=2.5,outline="darkorchid4"))
    data.logout.append(canvas.create_text(1225,78,text="Logout", 
        fill="white",font="Helvetica 13"))
    
def givestockinfo(stock):
    volume=0
    Url = ("""http://chartapi.finance.yahoo.com/instrument/1.0/"""
           +stock+
           """/chartdata;type=quote;range=1d/csv""")
    data=requests.get(Url).text
    info=data.splitlines()
    lineforlastclose=info[8].split(":")
    lastclose=lineforlastclose[1]
    lastprice=info[-1]
    mostrecent=lastprice.split(",")
    price=mostrecent[1]
    change=float(price)-float(lastclose)
    alldata=data.splitlines()
    stockdata=[]
    for line in alldata:
        databydate=[]
        for info in line.split(","):
            if line[0].isdigit():
                databydate+=[info]
                stockdata+=[databydate]
    for dates in stockdata:
        volume+=int(dates[5])
    return (price,volume//4,change)

def calculatesandpdata(data):
    (data.sandpprice,data.sandpvolume,data.sandpchange)=givestockinfo("^GSPC")

def calculatedowdata(data):
    (data.dowprice,data.dowvolume,data.dowchange)=givestockinfo("DOW")

def calculatenikkeiprice(data):
    (data.nikkeiprice,data.nikkeivolume,data.nikkeichange)=givestockinfo("^N225")

def calculateoilprice(data):
    (data.oilprice,data.oilvolume,data.oilchange)=givestockinfo("OIL")

def calculatenasdaqprice(data):
    (data.nasdaqprice,data.nasdaqvolume,data.nasdaqchange)=givestockinfo("^IXIC")

class SandPThread(threading.Thread):
    def __init__(self,target,data):
        threading.Thread.__init__(self)
        self.target=target
        self.data=data

    def run(self):
        self.target(self.data)

class DowThread(threading.Thread):
    def __init__(self,target,data):
        threading.Thread.__init__(self)
        self.target=target
        self.data=data

    def run(self):
        self.target(self.data)

class NikkeiThread(threading.Thread):
    def __init__(self,target,data):
        threading.Thread.__init__(self)
        self.target=target
        self.data=data

    def run(self):
        self.target(self.data)

class OilThread(threading.Thread):
    def __init__(self,target,data):
        threading.Thread.__init__(self)
        self.target=target
        self.data=data

    def run(self):
        self.target(self.data)

class NasdaqThread(threading.Thread):
    def __init__(self,target,data):
        threading.Thread.__init__(self)
        self.target=target
        self.data=data

    def run(self):
        self.target(self.data)

def calculateborderdata(data):
    sandpthread=SandPThread(calculatesandpdata,data)
    sandpthread.start()
    dowthread=DowThread(calculatedowdata,data)
    dowthread.start()
    nikkeithread=NikkeiThread(calculatenikkeiprice,data)
    nikkeithread.start()
    oilthread=OilThread(calculateoilprice,data)
    oilthread.start()
    nasdaqthread=NasdaqThread(calculatenasdaqprice,data)
    nasdaqthread.start()
    

def drawsandp(canvas,data):
    data.sandp=[]
    while data.sandpprice==None:
        time.sleep(.0001)
    data.sandp.append(canvas.create_text(290,7,text="S&P 500", anchor=NW, 
        fill="white"))
    data.sandp.append(canvas.create_text(360,7,
        text=round(float(data.sandpprice),2), anchor=NW, fill="white"))
    if data.sandpchange!=None:
            if data.sandpchange<0:
                data.sandp.append(canvas.create_text(420,7,
                    text=round(data.sandpchange,2), anchor=NW, fill="red"))
            else:
                data.sandp.append(canvas.create_text(420,7,
                    text=round(data.sandpchange,2), anchor=NW, fill="green"))

def ibmlogo(data,canvas):
    im=Image.open("IBMLOGO.png")
    im=im.resize((190,75),Image.ANTIALIAS)
    canvas.ibmimage= ImageTk.PhotoImage(im)
    canvas.create_image(1190,720, image=canvas.ibmimage)
    
def yahoologo(data,canvas):
    jm=Image.open("YahooFinance.jpg")
    jm=jm.resize((180,45),Image.ANTIALIAS)
    canvas.yahooimage= ImageTk.PhotoImage(jm)
    canvas.create_image(1000,720, image=canvas.yahooimage)
    canvas.create_text(880,720,text="Powered by:", fill="black",
        font="Helvetica 12 italic")

def drawdowjones(canvas,data):
    data.dow=[]
    while data.dowprice==None:
        time.sleep(.0001)
    data.dow.append(canvas.create_text(520,7,text="Dow Jones", anchor=NW, 
        fill="white"))
    data.dow.append(canvas.create_text(620,7,text=round(float(data.dowprice),2), 
        anchor=NW, fill="white"))
    if data.dowchange!=None:
            if data.dowchange<0:
                data.dow.append(canvas.create_text(670,7,
                    text=round(data.dowchange,2), anchor=NW, fill="red"))
            else:
                data.dow.append(canvas.create_text(670,7,
                    text=round(data.dowchange,2), anchor=NW, fill="green"))


def drawnikkei(canvas,data):
    data.NIKKEI=[]
    while data.nikkeiprice==None:
        time.sleep(.0001)
    data.NIKKEI.append(canvas.create_text(760,7,text="Nikkei 225", 
        anchor=NW, fill="white"))
    data.NIKKEI.append(canvas.create_text(840,7,
        text=round(float(data.nikkeiprice),2), anchor=NW, fill="white"))
    if data.nikkeichange!=None:
            if data.nikkeichange<0:
                data.NIKKEI.append(canvas.create_text(920,7,
                    text=round(data.nikkeichange,2), anchor=NW, fill="red"))
            else:
                data.NIKKEI.append(canvas.create_text(920,7,
                    text=round(data.nikkeichange,2), anchor=NW, fill="green"))

def drawoil(canvas,data):
    data.OIL=[]
    while data.oilprice==None:
        time.sleep(.0001)
    data.OIL.append(canvas.create_text(1050,7,text="Crude Oil", 
        anchor=NW, fill="white"))
    data.OIL.append(canvas.create_text(1120,7,
        text=round(float(data.oilprice),2), anchor=NW, fill="white"))
    if data.oilchange!=None:
            if data.oilchange<0:
                data.OIL.append(canvas.create_text(1170,7,
                    text=round(data.oilchange,2), anchor=NW, fill="red"))
            else:
                data.OIL.append(canvas.create_text(1170,7,
                    text=round(data.oilchange,2), anchor=NW, fill="green"))


def drawtopborder(canvas,data):
    data.topborder=[]
    data.NASDAQ=[]
    while data.nasdaqprice==None:
        time.sleep(.0001)
    data.topborder.append(canvas.create_line(0,0,data.width,0,
        fill="black", width=70))
    data.topborder.append(canvas.create_line(0,30,data.width,30,
        fill="red", width=5))
    data.topborder.append(canvas.create_line(0,35,data.width,35,
        fill="darkorchid4", width=5))
    data.topborder.append(canvas.create_line(0,32.5,data.width,32.5,
        fill="white", width=1))
    data.NASDAQ.append(canvas.create_text(50,7,text="NASDAQ", anchor=NW, 
        fill="white"))
    data.NASDAQ.append(canvas.create_text(120,7,
        text=round(float(data.nasdaqprice),2), anchor=NW, fill="white"))
    if data.nasdaqchange!=None:
            if data.nasdaqchange<0:
                data.NASDAQ.append(canvas.create_text(190,7,
                    text=round(data.nasdaqchange,2), anchor=NW, fill="red"))
            else:
                data.NASDAQ.append(canvas.create_text(190,7,
                    text=round(data.nasdaqchange,2), anchor=NW, fill="green"))
    drawsandp(canvas,data)
    drawdowjones(canvas,data)
    drawnikkei(canvas,data)
    drawoil(canvas,data)

def drawleftborder(canvas,data):
    pass
    
def drawdesign(canvas,data):
    data.designline=[]
    data.designline.append(canvas.create_line(0,130,data.width,130, 
        fill="firebrick", width=15))
    data.designline.append(canvas.create_line(0,130,data.width,130, 
        fill="darkviolet", width=5))
    data.designline.append(canvas.create_line(0,130,data.width,130, 
        fill="white", width=1))
    data.designline.append(canvas.create_line(355,135,355,data.height,
        fill="firebrick", width=15))
    data.designline.append(canvas.create_line(355,135,355,data.height,
        fill="darkviolet", width=5))
    data.designline.append(canvas.create_line(355,135,355,data.height,
        fill="white", width=1))
    data.designline.append(canvas.create_line(0,770,data.width,770, 
        fill="firebrick", width=15))
    data.designline.append(canvas.create_line(0,770,data.width,770, 
        fill="darkviolet", width=5))
    data.designline.append(canvas.create_line(0,770,data.width,770, 
        fill="white", width=1))
    drawleftborder(canvas,data)
        



def MainRedrawAll(canvas, data):
    drawminussign(canvas,data)
    drawsearchtext(canvas,data)
    searchbar(canvas,data)
    drawbutton(canvas,data)
    drawstocksgrid(data,canvas)
    drawusername(canvas,data)
    drawstocks(canvas,data) #REALLY SLOW
    drawdesign(canvas,data)
    drawgrid(data,canvas)
    drawtopborder(canvas,data) #REALLY SLOW
    drawlogo(canvas,data)
    if data.currentstock!=None:
        data.currentstock.drawcurrentstock(canvas)
        data.currentstock.drawinformation(canvas)
        data.currentstock.draw_figure(canvas)
        if data.graphmotion==True:
            data.currentstock.drawgraphbox(canvas,data.graphx,data.graphy)
        if data.gridmotion==True:
            drawkeywords(data,canvas)
    ibmlogo(data,canvas)
    yahoologo(data,canvas)
    if data.dropdownmenu==True:
        drawdropdownmenu(data,canvas)
    

####################################
# Logout mode
####################################

def LogoutMouseMotion(event,data):
    pass

def LogoutMousePressed(event, data):
    if 560<event.x<770 and 450<event.y<475:
        data.mode="login"
    pass

def LogoutKeyPressed(event, data):
    pass
   
def LogoutTimerFired(data):
    pass

def drawlogologout(canvas,data):
    im=Image.open("Logo.png")
    im=im.resize((220,200),Image.ANTIALIAS)
    canvas.image= ImageTk.PhotoImage(im)
    canvas.create_image(data.width//2,data.height//2-100, image=canvas.image)
    pass

def drawdesignlogout(canvas,data):
    canvas.create_line(0,100,data.width,100, fill="firebrick", width=15)
    canvas.create_line(0,100,data.width,100, fill="darkviolet", width=5)
    canvas.create_line(0,100,data.width,100, fill="white", width=1)
    canvas.create_line(100,0,100,data.height,fill="firebrick", width=15)
    canvas.create_line(100,0,100,data.height,fill="darkviolet", width=5)
    canvas.create_line(100,0,100,data.height,fill="white", width=1)
    canvas.create_line(150,0,150,data.height,fill="firebrick", width=15)
    canvas.create_line(150,0,150,data.height,fill="darkviolet", width=5)
    canvas.create_line(150,0,150,data.height,fill="white", width=1)
    canvas.create_line(data.width-100,0,data.width-100,data.height,
        fill="firebrick", width=15)
    canvas.create_line(data.width-100,0,data.width-100,data.height,
        fill="darkviolet", width=5)
    canvas.create_line(data.width-100,0,data.width-100,data.height,
        fill="white", width=1)
    canvas.create_line(data.width-150,0,data.width-150,data.height,
        fill="firebrick", width=15)
    canvas.create_line(data.width-150,0,data.width-150,data.height,
        fill="darkviolet", width=5)
    canvas.create_line(data.width-150,0,data.width-150,data.height,
        fill="white", width=1)
    canvas.create_line(0,data.height-100,data.width,data.height-100, 
        fill="firebrick", width=15)
    canvas.create_line(0,data.height-100,data.width,data.height-100, 
        fill="darkviolet", width=5)
    canvas.create_line(0,data.height-100,data.width,data.height-100, 
        fill="white", width=1)

def LogoutRedrawAll(canvas, data):
    logo(canvas,data)
    drawdesignlogout(canvas,data)
    canvas.create_rectangle(560,450,770,475,fill="darkorchid4", width=2.5, 
        outline="darkorchid4")
    canvas.create_text(665,462, text="Sign in", fill="white", 
        font="Helvetica 12")

#Below code from 112 course notes but I've added my own features such as 
#mouse motion
def run(width=1300, height=775):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas,data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def mouseMotionWrapper(event,canvas,data):
        mouseMotion(event,data)
        redrawAllWrapper(canvas,data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 0# milliseconds
    root = Tk()
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    canvas.bind("<Motion>", lambda event:
                            mouseMotionWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()



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

#

class ArticleDataThread(threading.Thread):
    def __init__(self,target):
        threading.Thread.__init__(self)
        self.target=target

    def run(self):
        self.target()

class GetUrlAndTitleThread(threading.Thread):
    def __init__(self,target,convertedtopython):
        threading.Thread.__init__(self)
        self.target=target
        self.convertedtopython=convertedtopython

    def run(self):
        self.target(self.convertedtopython)

class GiveStockInfoThread(threading.Thread):
    def __init__(self,target):
        threading.Thread.__init__(self)
        self.target=target

    def run(self):
        self.target()

class AlchemyYahoo(object):
    def __init__(self,stock):
        self.apikey="8490c1022cc805b491e2cf81b243c07e1606282c"
        self.stock=stock
        self.todaydate=datetime.datetime.now()
        self.todaydatetimestamp=int(time.time())
        self.startdate=str((self.todaydate-datetime.timedelta(days=10)).date())
        self.startdatetimestamp=int(datetime.datetime.strptime(self.startdate, 
            '%Y-%m-%d').strftime("%s"))
        self.result=[]
        self.articlecount=[]
        self.stockdates=[]
        self.positive="positive"
        self.negative="negative"
        self.articlerow=6
        self.articlecol=1
        self.cellx=250
        self.celly=100
        self.articledata=None
        self.companyname=None
        self.articledatathread = ArticleDataThread(self.AlchemyURL)
        self.articledatathread.start()
        self.price=None
        self.change=None
        self.volume=None
        self.articlekeywords=[]
        self.givestockinfothread=GiveStockInfoThread(self.givestockinfo)
        self.givestockinfothread.start()
        self.drawgraph()
        self.graph = None
        self.listofarticlekeywords()

    def getcompanyname(self):
        Url=("http://chartapi.finance.yahoo.com/instrument/1.0/"
            +self.stock+"""/chartdata;type=quote;range=1d/csv""")
        data=requests.get(Url).text
        info=data.splitlines()
        companyline=info[2]
        companynamelist=companyline.split(":")
        self.companyname=companynamelist[1]

    def listofarticlekeywords(self):
        while self.articledata==None:
            time.sleep(.001) 
        if self.articledata==False:
            return
        for i in range(len(self.articledata)):
            self.articlekeywords.append(self.getkeywords(i))

    def geturlandtitle(self,info,newlist=None):
        if newlist==None:
            newlist=[]
        if type(info)==str or type(info)==int:
            return newlist
        if type(info)==list:
            for dictionaries in info:
                self.geturlandtitle(dictionaries,newlist)            
        else:
            for key,value in info.items():
                if type(value)==dict:
                    if key=="url":
                        newlist.append(info[key])
                    else:
                        self.geturlandtitle(info[key],newlist)
                else:
                    self.geturlandtitle(info[key],newlist)
        self.articledata=newlist

    def chartdata(self):
        stockinfo=[]
        Url=("http://chartapi.finance.yahoo.com/instrument/1.0/"
            +self.stock+"/chartdata;type=quote;range=2m/csv")
        data=requests.get(Url).text
        info=data.splitlines()
        highline=info[14].split(",")
        #self.high=highline[1]
        lowline=info[15].split(":")
        #self.low=lowline[1].split(",")[0]
        for line in data.splitlines():
            eachline=[]
            for info in line.split(","):
                if line[0].isdigit():
                    eachline+=[info]
                    stockinfo+=[eachline]
        return stockinfo

    def AlchemyURL(self):
        companynamethread=threading.Thread(target=self.getcompanyname,args=())
        companynamethread.start()
        while self.companyname==None:
            time.sleep(.0001)
        keys=[]
        QueryURL=("""https://access.alchemyapi.com/calls/data/GetNews?apikey=8490c1022cc805b491e2cf81b243c07e1606282c&return=enriched.url.title,enriched.url.url&start="""
            +str(self.startdatetimestamp)+"&end="+str(self.todaydatetimestamp)
            +"""&q.enriched.url.entities.entity=|text="""
            +self.stock+""",type=company|&q.enriched.url.docSentiment.type=positive&q.enriched.url.taxonomy.taxonomy_.label=technology%20and%20computing&count=6&outputMode=json""")
        r = requests.get(QueryURL).text
        string=json.dumps(r)
        convertedtopython=json.loads(r)
        if convertedtopython["status"]=='OK':
            geturlandtitlethread=GetUrlAndTitleThread(self.geturlandtitle,
                convertedtopython)
            geturlandtitlethread.start()
        else:
            self.articledata=False


    def draw_figure(self,canvas,loc=(650, 140)):
        #Draw a matplotlib figure onto a Tk canvas
        #loc: location of top-left corner of figure on canvas in pixels.
        #Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
        self.figure_canvas_agg = FigureCanvasAgg(self.figure)
        self.figure_canvas_agg.draw()
        self.figure_x, self.figure_y, self.figure_w, self.figure_h = (
            self.figure.bbox.bounds)
        self.figure_w, self.figure_h = int(self.figure_w), int(self.figure_h)
        self.photo = PhotoImage(master=canvas, width=self.figure_w, 
            height=self.figure_h)
        # Position: convert from top-left anchor to center anchor
        canvas.delete(self.graph)
        self.graph = canvas.create_image(loc[0] + self.figure_w/2, loc[1] + 
            self.figure_h/2, image=self.photo)
        # Unfortunatly, there's no accessor for the pointer to the native renderer
        tkagg.blit(self.photo, self.figure_canvas_agg.get_renderer()._renderer, 
            colormode=2)
        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        #return self.photo
        #Don't create the image, store the image and then add it
    
    def drawgraph(self):
        #Learnt how to use matoplotlib from youtube videos
        while self.companyname==None:
            time.sleep(0.001)
        self.stockinfo=self.chartdata()
        date=[]
        closeprice=[]
        highprice=[]
        lowprice=[]
        openprice=[]
        for line in self.stockinfo:
            date.append(datetime.datetime.strptime(line[0],"%Y%m%d"))
            closeprice.append((float((line[1]))))
            highprice.append((float(line[2])))
            lowprice.append((float((line[3]))))
            openprice.append((float((line[4]))))
        # Create the figure we desire to add to an existing canvas
        fig = plt.figure(facecolor="white",figsize=(7, 6), dpi=90)
        graph=plt.subplot(1,1,1)
        graph.plot(date,highprice, '#008080',label="High Price")
        graph.plot(date,lowprice, label="Low Price", linestyle=":",linewidth=2)
        graph.plot(date,openprice, label="Open Price",linestyle="--")
        graph.plot(date,closeprice, label="Close Price",linestyle="-.",
            linewidth=2)
        plt.legend(loc=2,fontsize="x-small",fancybox=True,shadow=True, 
            frameon=True,framealpha=None)
        graph.grid(True,which="major",axis="both",color="red")
        plt.xlabel("Date", color="green",fontsize=11)
        plt.ylabel("Price", color="green",fontsize=11)
        graph.spines["bottom"].set_color("purple")
        graph.spines["top"].set_color("purple")
        graph.spines["right"].set_color("purple")
        graph.spines["left"].set_color("purple")
        graph.tick_params(axis="y",colors="navy")
        graph.tick_params(axis="x",colors="navy")
        plt.title(self.companyname, color="purple")
        graph.xaxis.set_major_locator(mticker.MaxNLocator(6))
        graph.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        labelsx = graph.get_xticklabels()
        plt.setp(labelsx, rotation=30, fontsize=11)
        labelsy=graph.get_yticklabels()
        plt.setp(labelsy,rotation=0,fontsize=11)
        self.low,self.high=graph.get_ylim()
        plt.tight_layout()
        self.figure=fig

    def drawinformation(self,canvas):
        self.drawarticle=[]
        if self.articledata!=False and self.articledata!=None:
            gap = 0
            while len(self.articledata)<6:
                self.articledata.append({"title":"Could not find enough article\
                    s in recent times"})
            for article in self.articledata:
                left=400
                top=160+(gap*self.celly)
                if article["title"]!="Could not find enough articles in recent \
                times. There's not much information about the stock in \
                the news":
                    self.drawarticle.append(canvas.create_text(left,top,
                        text=article["title"], anchor=NW, width=210, 
                        fill="medium blue", font="Helvetica 13 underline"))
                    gap+=1
                else:
                    self.drawarticle.append(canvas.create_text(left,top,
                        text=article["title"], anchor=NW, width=210, 
                        fill="orangered2", font="Helvetica 13 underline"))
                    gap+=1
        else:
            canvas.create_text(400,160, text="""You've exhausted your daily 
                limit. \n\n Sincerely, \n Smart Trading.""", 
                fill="darkorchid4",anchor=NW)

    def givestockinfo(self):
        self.volume=0
        Url=("http://chartapi.finance.yahoo.com/instrument/1.0/"
            +self.stock+"""/chartdata;type=quote;range=1d/csv""")
        data=requests.get(Url).text
        info=data.splitlines()
        lineforlastclose=info[8].split(":")
        self.lastclose=lineforlastclose[1]
        lastprice=info[-1]
        mostrecent=lastprice.split(",")
        self.price=mostrecent[1]
        self.change=float(self.price)-float(self.lastclose)
        alldata=data.splitlines()
        stockdata=[]
        for line in alldata:
            databydate=[]
            for info in line.split(","):
                if line[0].isdigit():
                    databydate+=[info]
                    stockdata+=[databydate]
        for dates in stockdata:
            self.volume+=int(dates[5])
            self.volume=self.volume

    def drawstockinfo(self,canvas,gap):
        self.displaystockinfo=[]
        while self.price==None:
            time.sleep(.0001)
        price=round(float(self.price),2)
        change=round(self.change,2)
        left=205
        top=170+(gap*self.celly)
        self.displaystockinfo.append(canvas.create_text(left,top,
            text=self.stock, width=210, fill="red2", font="Helvetica 15"))
        self.displaystockinfo.append(canvas.create_line(96,195+(gap*self.celly)
            , 317, 195+(gap*self.celly) , fill="grey"))
        self.displaystockinfo.append(canvas.create_line(250,200+(gap*self.celly)
            , 250, 240+(gap*self.celly) , fill="grey"))
        self.displaystockinfo.append(canvas.create_line(160,200+(gap*self.celly)
            , 160, 240+(gap*self.celly) , fill="grey"))
        self.displaystockinfo.append(canvas.create_text(100,200+(gap*self.celly)
            ,text="Price", anchor=NW, fill="gray25"))
        self.displaystockinfo.append(canvas.create_text(100,220+(gap*self.celly)
            ,text=price, anchor=NW))
        self.displaystockinfo.append(canvas.create_text(175,200+(gap*self.celly)
            ,text="Volume", anchor=NW, fill="gray25"))
        self.displaystockinfo.append(canvas.create_text(175,220+(gap*self.celly)
            ,text=self.volume, anchor=NW))
        self.displaystockinfo.append(canvas.create_text(260,200+(gap*self.celly)
            ,text="Change", anchor=NW, fill="gray25"))
        if change!=None:
            if change<0:
                self.displaystockinfo.append(canvas.create_text(260,
                    220+(gap*self.celly),text=change, anchor=NW, fill="red"))
            else:
                self.displaystockinfo.append(canvas.create_text(260,
                    220+(gap*self.celly),text=change, anchor=NW, fill="green"))
            gap+=1

    def drawcurrentstock(self,canvas):
        self.displaycurrentstock=[]
        while self.price==None:
            time.sleep(.0001)
        price=round(float(self.price),2)
        change=round(self.change,2)
        self.displaycurrentstock.append(canvas.create_rectangle(800,50,1100,
            110,outline="purple", width=3))
        self.displaycurrentstock.append(canvas.create_rectangle(800,50,1100,
            110,outline="red", width=2))
        self.displaycurrentstock.append(canvas.create_text(830,70,
            text=self.stock,fill="purple"))
        self.displaycurrentstock.append(canvas.create_text(830,90,
            text="+", fill="green3", font="Helvetica 17 bold"))
        self.displaycurrentstock.append(canvas.create_text(870,60,
            text="Price", anchor=NW, fill="gray25"))
        self.displaycurrentstock.append(canvas.create_text(870,85,
            text=price, anchor=NW))
        self.displaycurrentstock.append(canvas.create_text(945,60,
            text="Volume", anchor=NW, fill="gray25"))
        self.displaycurrentstock.append(canvas.create_text(945,85,
            text=self.volume, anchor=NW))
        self.displaycurrentstock.append(canvas.create_text(1025,60,
            text="Change", anchor=NW, fill="gray25"))
        self.displaycurrentstock.append(canvas.create_line(860,60, 
            860, 100, fill="grey"))
        self.displaycurrentstock.append(canvas.create_line(935,60, 935, 100, 
            fill="grey"))
        self.displaycurrentstock.append(canvas.create_line(1015,60, 1015, 100, 
            fill="grey"))
        if change!=None:
            if change<0:
                self.displaycurrentstock.append(canvas.create_text(1025,85,
                    text=change, anchor=NW, fill="red"))
            else:
                self.displaycurrentstock.append(canvas.create_text(1025,85,
                    text=change, anchor=NW, fill="green"))

    def drawgraphbox(self,canvas,x,y):
        differenceinpixels=415
        differenceinprice=abs(self.high-self.low)
        change=differenceinprice/differenceinpixels
        top=175
        ydifference=y-top
        difference=(change*ydifference)
        canvas.create_rectangle(x-30,y-30,x+30,y-10,fill="white", 
            outline="darkorchid4", width=2)
        canvas.create_rectangle(x-30,y-30,x+30,y-10,outline="white", width=1)
        canvas.create_text(x,y-20,text=abs(round(float(self.high)-difference,2))
            , fill="darkorchid4")

    def getkeywords(self,number):
        keywords=set()
        if self.articledata==None or self.articledata==False:
            return
        articles=self.articledata
        dictionary=articles[number]
        url=dictionary["url"]
        QueryURL=("http://gateway-a.watsonplatform.net/calls/url/URLGetRankedKeywords?apikey=8490c1022cc805b491e2cf81b243c07e1606282c&url="+url+"&outputMode=json")    
        r = requests.get(QueryURL).text
        string=json.dumps(r)
        convertedtopython=json.loads(r)
        if convertedtopython['status'] == 'OK':
            for keyword in convertedtopython['keywords']:
                if len(keywords)<15:
                    keywords.add(keyword["text"].strip())
                else:
                    break
        else:
            if len(keywords)==0:
                keywords.add("We're sorry but you've hit the transactions per \
                    day.\n\n Sincerely,  Smart Trading.")
        return keywords

    def __eq__(self,other):
        return isinstance(other,AlchemyYahoo) and self.stock==other.stock
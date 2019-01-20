import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
failure=[]
def get_data(i):
    try:
        url=requests.get("https://www.boxofficeindia.com/movie.php?movieid="+str(i)).text
        Movie={}
        soup = BeautifulSoup(url,"lxml")
        Movie["Title"]=soup.find("div",{"class":"bl_tle_mvi blue_tlte"}).text.strip()
        boxoffice=soup.find("div",{"class":"movieboxssec"}).text.split("\xa0")
        Movie["Release Date"]=boxoffice[0].split(":")[1].strip()
        Movie["Runtime"]=boxoffice[3].split("\n")[2].strip()
        Movie["Genre"]=boxoffice[-1].split(":")[1].strip()
        collection=soup.find("div",{"style":"overflow:hidden;"})
        row=collection.text.split("\xa0")
        new_row=[x.replace("\n","") for x in row]
        Movie["Screens"]=new_row[1].replace("First Day:","")
        Movie["First Day"]=new_row[2].replace("Opening Note:","")
        Movie["First Weekend"]=new_row[4]
        collection2=soup.findAll("table",{"class":"mviedtailstbe"})
        row=collection2[5].text.split("\xa0")
        Movie['First Week']=row[1].replace("\n","").replace("Budget:","")
        Movie['Budget']=row[2].replace("\n","").replace("India Gross:","")
        Movie['India Gross']=row[3].replace("\n","").replace("Overseas Gross:","")
        Movie['Overseas Gross']=row[4].replace("\n","").replace("Worldwide Gross:","")
        Movie['Worldwide Gross']=row[5].replace("\n","")
        
        crewurl=requests.get("https://www.boxofficeindia.com/cast_crew.php?movieid="+str(i)).text
        crewsoup =BeautifulSoup(crewurl,"lxml")
        production=crewsoup.find("div",{"class":"movieboxssec bluelink movieim7"})
        Movie["Production Banner"] = production.find("a").text
        crew=crewsoup.find("div",{"class":"movieim6"}).text.replace("\xa0","").split("\n\n\n")
        crew=[x for x  in crew if x]
        try:
            for row in crew:
                row = row.split("\n")
                row = [x for x in row if x]
                Movie[row[0]]=",".join(row[1:])
            cast=crewsoup.find("div",{"class":"moviegraybox bluelink"}).text.split("\n\n\n\n\n\n")
            cast=[x for x in cast if x]
            
        
            for i in range(7):
                Movie["Actors "+str(i+1)]=cast[i].split("\n\n\n\n")[0]
        except IndexError:
            pass
        
    except:
        failure.append(i)
        pass
    return Movie

import pandas as pd
import numpy as np
import time




from bs4 import BeautifulSoup
import requests
import re
import sys


i=0
df = pd.DataFrame(columns=['Amazon Site','ASIN','Review Rating','Quantity of Reviews','Monteray Unit','Selling Price','Link'])
with open('input.txt', 'r') as file:
   lines = file.readlines()
for line in lines:
     cc=line.split()
     
     URL = 'https://'+cc[0]+'/dp/'+cc[1]
   
     headersf = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
     try:
         req = requests.get(URL,headers=headersf)
     except requests.exceptions.ConnectionError:
         print("Connection refused")
         continue

     
     s=BeautifulSoup(req.content,features="lxml")
     quantr=""
     try:
         
         quantity_reviews=s.select("#acrCustomerReviewText.a-size-base")[0].get_text().strip()
         quantity_reviews=quantity_reviews.replace("ratings","")
         quantity_reviews = re.findall("(\d+(?:,d+)*)", quantity_reviews)
         
         for x in range(len(quantity_reviews),0,-1):
                    quantr=str(quantity_reviews[x-1])+quantr
                   
                    
             
         
        
     except IndexError:
         quantr='N/A'
     
     
     try:   
       review=s.select("#averageCustomerReviews")[0].get_text().strip()
       review=str(review)
       r=review.split()
       review=r[0]
       if(len(review)>4):
           
           review=review[-3:]
           
   
     except IndexError:
        review='N/A'
    
    
     if(review=='N/A'): 
          try: 
            price=s.select("#acr-average-stars-rating-text")[0].get_text().strip()
            if("-" in str(price)):
              a=str(price).split("-")
              f=a[0]
              g=a[1]
              price=f[1:]+"-"+g[2:]
              memontary_unit=f[0:1]
              memontary_unit=g[0:1]
            elif (" " in str(price)):
                a=str(price).split()
                price=a[0]
                memontary_unit=a[1]
            else:
          
              g=str(price)
            
              price=price[1:]
              memontary_unit=g[0:1]
          
          except IndexError:
            price='N/A'
            memontary_unit='N/A'
     
     try:
        price=s.select("#priceblock_saleprice")[0].get_text().strip()
        
        if("-" in str(price)):
           
           a=str(price).split("-")
          
           f=a[0]
           g=a[1]
           price=f[1:]+"-"+g[2:]
           
           memontary_unit=f[0:1]
           
           memontary_unit=f[0:1]
        elif ("," in str(price)):
               
                a=str(price).split()
                price=a[0]
                
                memontary_unit=a[1]
                
        else:
           
           g=str(price)
           
           
           price=price[1:]
           memontary_unit=g[0:1]
        
          
     except IndexError:
          
         
          price='N/A'
          memontary_unit='N/A'
     
     
     if price=='N/A':
          
          try: 
            price=s.select("#priceblock_ourprice")[0].get_text().strip()
            if("-" in str(price)):
              a=str(price).split("-")
              f=a[0]
              g=a[1]
              price=f[1:]+"-"+g[2:]
              memontary_unit=f[0:1]
              memontary_unit=g[0:1]
            elif (" " in str(price)):
                a=str(price).split()
                price=a[0]
                memontary_unit=a[1]
            else:
          
              g=str(price)
            
              price=price[1:]
              memontary_unit=g[0:1]
          
          except IndexError:
            price='N/A'
            memontary_unit='N/A'
    
     if price=='N/A':
          
          try: 
            price=s.select("#priceblock_dealprice")[0].get_text().strip()
            print("zaza")
            if("-" in str(price)):
              a=str(price).split("-")
              f=a[0]
              g=a[1]
              price=f[1:]+"-"+g[2:]
              memontary_unit=f[0:1]
              memontary_unit=g[0:1]
            elif (" " in str(price)):
                a=str(price).split()
                price=a[0]
                memontary_unit=a[1]
            else:
          
              g=str(price)
            
              price=price[1:]
              memontary_unit=g[0:1]
          
          except IndexError:
            price='N/A'
            memontary_unit='N/A'
        
     try: 
            cp=s.select("#captchacharacters")[0].get_text().strip()
            print("captcha")
            
            
     except IndexError:
         print("")
           
     
     
     
     
     i=i+1
     print("ASIN: "+cc[1]+" ,Review_Rating "+review+" ,Price "+memontary_unit+price+" Quantity Reviews "+quantr)
     time.sleep(2)
     
     df = df.append({'Amazon Site': cc[0], 'ASIN': cc[1], 'Review Rating': review,'Monteray Unit':memontary_unit,'Selling Price':price,'Link':URL,'Quantity of Reviews':str(quantr)},ignore_index=True)
     

     
df.to_excel("finalout.xlsx",encoding='utf-8-sig',index=False)


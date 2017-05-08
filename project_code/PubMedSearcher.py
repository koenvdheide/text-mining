# -*- coding: utf-8 -*-
"""
Created on Sun May  7 20:31:12 2017

@author: RICK
"""

from Bio import Entrez
from Bio import Medline

#Simple class to search for articles in pubMed
class PubMed_searcher:
    
    #Telling Entrez who we are
    def __init__(self):
        Entrez.email = "Anonymous@anonymous.com" #always tell who your are :)
    
    #Seraching using a specific term in a specific database
    def search(self, term, db="pubmed", retmax=1000):
       try:
            if term:
                handle = Entrez.esearch(db=db, term=term, retmax = retmax)
                records = Entrez.read(handle)  
                handle.close() #close connection
                return self.__fetchArticles(records['IdList']) 
            else:
                print("Please provide a search term!")
                return None
       except Exception as e:
           print("A server error occured")
           print(e) #REMOVE AFTER DEVELOPMENT
            
    
    #parse the articles in MedLine format 
    def __fetchArticles(self,IDlist):
        if IDlist:
            handle = Entrez.efetch(db="pubmed", id=",".join(IDlist), rettype="medline",retmode="text")
            return Medline.parse(handle)
        else:
            return None

    


        
        
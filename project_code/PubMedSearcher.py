# -*- coding: utf-8 -*-
"""
Created on Sun May  7 20:31:12 2017

@author: RICK
"""

from Bio import Entrez
from Bio import Medline


# Simple class to search for articles in pubMed
class PubMedSearcher:
    Entrez.email = "r.beeloo@outlook.com"

    # Seraching using a specific term in a specific database
    @staticmethod
    def search(term, db="pubmed", retrieve_max=100):
        try:
            if term:
                handle = Entrez.esearch(db=db, term=term, retmax=retrieve_max)
                records = Entrez.read(handle)
                handle.close()  # close connection
                return records['IdList']
            else:
                print("Please provide a search term!")
                return None
        except Exception as e:
            print("A server error occured")
            print(e)  # REMOVE AFTER DEVELOPMENT


    # parse the articles in MedLine format
    @staticmethod
    def fetch_articles(id_list):
        articles = []
        count = 0
        if id_list:
            for ID in id_list:
                count += 1
                handle = Entrez.efetch(db="pubmed", id=ID, rettype="medline", retmode="text")
                try:
                    article = Medline.parse(handle)
                    articles.append(article)
                    print("appended" + str(count))
                except:
                    continue
            return articles
        else:
            return None

    # parse the genes in tab format
    @staticmethod
    def fetch_genes(id_list, common_name=False):
        organisms = []
        if id_list:
            handle = Entrez.esummary(db="gene", id=",".join(id_list), retmode="xml")
            record = Entrez.read(handle)
            handle.close()
            for entry in record["DocumentSummarySet"]['DocumentSummary']:
                if common_name:
                    organisms.append(entry['Organism']['CommonName'])
                else:
                    organisms.append(entry['Organism']['ScientificName'])
            return organisms
        else:
            return None

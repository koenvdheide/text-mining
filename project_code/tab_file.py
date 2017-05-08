# -*- coding: utf-8 -*-
"""
Created on Sun May  7 21:37:11 2017

@author: RICK
"""

class NCBI_tab_file():
    def __init__(self,file_path):
        self.file_path = file_path
    
    #returns list with dictionaries containing the parsed lines
    def search(self,word):
        found_genes = []
        with open(self.file_path, 'r') as file:
            for line in file:
                if word in line:
                    found_genes.append(self.__parse(line))
        return found_genes
                 
    #parses the NCBI tab file, COULD BE EXPANDED TO INCLUDE ALL OTHER COLUMNS
    def __parse(self,line):
        line = line.strip().split("\t")
        return {"tax_id":line[0],
                "organisme": line[1],
                "symbol": line[5],
                "alt_sybmols": line[6].split(", "),
                }
        
        
    
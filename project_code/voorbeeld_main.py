# -*- coding: utf-8 -*-
"""
Created on Sun May  7 20:30:23 2017

@author: RICK
"""

from PubMedSearcher import PubMed_searcher
from TextMiner import Text_miner
from ConditionSearcher import Condition_searcher
from tab_file import NCBI_tab_file

#setting global variables
miner = Text_miner()
searcher = PubMed_searcher()
condition_sent_model = miner.build_filter_from_file("docs//conditie_zinnen.txt")
condition_model = miner.build_filter_from_file("docs//conditie_groepen.txt")
anto_file = NCBI_tab_file("docs//antho_genes.txt")
condition_searcher = Condition_searcher(condition_sent_model, "anthocyanin", 0.53)


def main():
    articles = searcher.search("anthocyanin AND plants[ORGN]",retmax=100)
    for article in articles:
        title = article.get("TI", "?")
        abstract = article.get("AB", "?")
        condition = condition_searcher.search(abstract)
        if len(condition) >0: #only show titles and conditions of articles in which something was found
            print(">>" + title)
            print("\t-" + str(condition) + "\n\n")
        

        
main()
    
        
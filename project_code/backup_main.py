# -*- coding: utf-8 -*-
"""
Created on Sun May  7 20:30:23 2017

@author: RICK
"""

from PubMedSearcher import PubMedSearcher
from TextMiner import TextMiner
from GeneSearcher import GeneSearcher
from ConditionSearcher import ConditionSearcher
from multiprocessing import Process


#setting global variables
miner = TextMiner()
condition_sent_model = miner.build_filter_from_file("docs//conditie_zinnen.txt")
gene_searcher = GeneSearcher()
condition_searcher = ConditionSearcher(condition_sent_model, "anthocyanin", 0.45)
import timeit

file = open('output.txt','w')
 
def split(list_to_split, n):
    return(list(list_to_split[i:i+n] for i in range(0, len(list_to_split), n)))
    

def gather_data(listje):
    print("input_data" + str(listje))
    articles = PubMedSearcher.fetchArticles(listje)
    for article in articles:
        article = list(article)[0]
        title = article.get("TI", "?") 
        abstract = article.get("AB", "?")
        condition_entries = condition_searcher.search(abstract)
        buffer = {}
        if len(condition_entries) >0: #only show titles and conditions of articles in which something was found
              for entry in condition_entries:
                  score = entry[0]
                  condition = entry[1]
                  sentence = entry[2]
                  if sentence in buffer:
                      genes = buffer[sentence]
                  else:
                      genes = gene_searcher.search(sentence, "plants[ORGN]")
                      buffer[sentence] = genes
                  for gene in genes:
                      file.write(condition.strip() + ";"+ str(gene[1]) + ";" + str(gene[0] + '\n'))
    return "done"
    
def main():
    start = timeit.default_timer()
    file.write("condition;organism;gene\n")
    articleIDs = PubMedSearcher.search("anthocyanin AND plants[ORGN]",'pubmed',500)
    splitted_list = split(articleIDs,100)
    count = 0
    procs = []
    for listje in splitted_list:
        count +=1
        print("proces: " + str(count) + " started")
        p = Process(target=gather_data, args=(listje,))
        procs.append(p)
    
    for p in procs:
        p.start()
    
    for p in procs:
        p.join()
    
    file.close()
    stop = timeit.default_timer()
    secs = stop-start
    minutes = secs/60
    print ("secs: " + str(secs))
    print ("secs: " + str(minutes))


if __name__ == '__main__':
    main()
    
        
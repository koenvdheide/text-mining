# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 16:16:19 2017

@author: RICK
"""
from Bio import Entrez
from Bio import Medline
from itertools import chain
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import wordnet

def main():
    records=searchPubMed("anthocyanin","pubmed",7000)
    ids = getResultIDs(records)
    articles = fetchArticles(ids)
    keyWords = getKeyWordsFromList("influenced decreased accumulation reduced under condition low high induced deficiency inhibited elevated stress circumstance during exposed directing".split())
    for art in articles:
        abstract = getArticleAbstract(art)
        score_dict = {}
        for sent in sent_tokenize(abstract):
            if "anthocyanin" in sent:
                score = getMatchScore(keyWords, sent)
                if score > 3: #number of matching words
                    score_dict[score] = sent
        if len(score_dict) > 0:
            print("<TITLE> " + getArticleTitle(art))
            maxScore = max(list(score_dict.keys()))
            print(str(maxScore)+ "> ")
            print(score_dict[maxScore] + "\n")


def getSynonyms(word):
    synonyms = wordnet.synsets(word)
    return(set(chain.from_iterable([word.lemma_names() for word in synonyms])))
    
def getMatchScore(keyWordList, sentence):
    score = 0
    for word in word_tokenize(sentence):
        if word in keyWordList:
            score+=1
    return score
        
  
def getKeyWordsFromList(word_list):
    all_words = set()
    for word in word_list:
        all_words.update(getSynonyms(word))
    return all_words

def getKeyWordsFromFile(filePath):
    file = open(filePath)
    words = file.readlines()[0].split()
    all_words = []
    for word in words:
        all_words.extend(getSynonyms(word))
    return(all_words)
    

def searchPubMed(term, db, retmax):
    Entrez.email = "Anonymous@anonymous.com" #always tell who your are :)
    handle = Entrez.esearch(db=db, term=term, retmax = retmax)
    return(Entrez.read(handle)) #return records
    
def getResultIDs(records):
    return(records['IdList'])

def fetchArticles(IDlist):
    if IDlist:
        handle = Entrez.efetch(db="pubmed", id=",".join(IDlist), rettype="medline",retmode="text")
        articles = Medline.parse(handle)
        return articles
    else:
        print("No ID's provided!")
        return None

def getArticleTitle(article):
        return article.get("TI", "?")
    
def getArticleAbstract(article):
    return article.get("AB","?")

def getPublicationDate(article):
    return article.get("PD","?")

def getSentences(text):
    return (sent_tokenize(text))


    










main()

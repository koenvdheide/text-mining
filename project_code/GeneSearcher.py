# -*- coding: utf-8 -*-
"""
Created on Wed May 10 08:13:24 2017

@author: RICK
"""
from PubMedSearcher import PubMedSearcher
from TextMiner import TextMiner
from nltk.corpus import stopwords

# global vars
cachedStopWords = set(stopwords.words("english"))  # enhances speed by ~70 times
cachedStopWords.update(["MESSAGE:", "MESSAGE", "CONCLUSION:", "KEY:", "KEY", "MATERIAL:", "METHODS:", "INTRODUCTION:"])


class GeneSearcher:
    def __init__(self):
        self.gene_regex = r'([A-Z][^\s]*[A-Z|-].?)'  # has to be imporved a lot!

    # This method first removes stopwords(e.g to, either etc.) to reduce searchs space
    # Then a regex is used to extract genes from the text
    def __extract_genes(self, text):
        text = ' '.join([word for word in text.split() if word not in cachedStopWords])
        genes = TextMiner.extract_regex(text, self.gene_regex)
        return genes

    # extract organism from hit
    def __get_organism(self, possible_gene, keyword=None):
        term = possible_gene + "[Gene/Protein Name]"
        if keyword:
            term += ' AND ' + keyword
        gene_ids = PubMedSearcher.search(term, "gene", 1)
        genes = PubMedSearcher.fetch_genes(gene_ids)
        return genes

    # search through text for genes
    def search(self, text, keyword=""):
        correct_genes = []
        for possible_gene in self.__extract_genes(text):
            gene_entry = self.__get_organism(possible_gene, keyword)
            if gene_entry:
                correct_genes.append((possible_gene, gene_entry[0]))
        return correct_genes

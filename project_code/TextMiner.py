# -*- coding: utf-8 -*-
"""
Created on Sun May  7 21:01:53 2017

@author: RICK
"""

import retinasdk
import re


class TextMiner:
    
    def __init__(self):
        api_key = "407a69c0-3192-11e7-b22d-93a4ae922ff1"
        self.lite_client = retinasdk.LiteClient(api_key)
        self.full_client = retinasdk.FullClient(api_key, apiServer="http://api.cortical.io/rest", retinaName="en_associative")

    #build filter based on train sentences
    def build_filter(self,sentences):
        text_filter = self.lite_client.createCategoryFilter(sentences)
        return text_filter
    
    #use every line as sentence for the "buildFilter" method
    def build_filter_from_file(self,file_path):
        sentences = []
        with open(file_path, 'r') as file:
            for line in file: 
                sentences.append(line.replace(".","").lower().strip())
        return self.build_filter(sentences)
                
    #compare the sentence with the model build from the training sentences
    def compare_to_model(self,sentence,text_filter):
        return self.lite_client.compare(sentence, text_filter)
    
    #extract valuable terms in sentences
    @staticmethod
    def extract_regex(self,sentence, regex):
        regex = re.compile(regex)
        matches = re.findall(regex, sentence)
        return matches
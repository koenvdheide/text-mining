# -*- coding: utf-8 -*-
"""
Created on Sun May  7 21:01:53 2017

@author: RICK
"""

import retinasdk
import re
API_KEY = "407a69c0-3192-11e7-b22d-93a4ae922ff1"
CLIENT = retinasdk.little_client = retinasdk.LiteClient(API_KEY)


class TextManipulator:


    @staticmethod
    def build_filter(sentences):
        sentence_filter = CLIENT.createCategoryFilter(sentences)
        return sentence_filter
    
    @staticmethod
    def build_filter_from_file(file_path):
        sentences = []
        with open(file_path, 'r') as file:
            for line in file: 
                sentences.append(line.replace(".","").lower().strip())
        return TextManipulator.build_filter(sentences)

    @staticmethod
    def compare_to_model(sentence,text_filter):
        return CLIENT.compare(sentence, text_filter)
    

    @staticmethod
    def extract_regex(sentence, regex):
        regex = re.compile(regex)
        matches = re.findall(regex, sentence)
        return matches
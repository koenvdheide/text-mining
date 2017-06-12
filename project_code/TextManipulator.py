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
        """
        This function build a filter based on a set of sentences provided. 
        :param sentences: The sentences which should be used to build a model. 
        :return: A category filter. 
        """
        sentence_filter = CLIENT.createCategoryFilter(sentences)
        return sentence_filter

    @staticmethod
    def build_filter_from_file(file_path):
        """
        This function converts the content of a file in a sentence list
        and uses the build_filter function to build a category filter.
        :param file_path: The path to the file that should be used to build the filter.
        :return: A caterogry filter. 
        """
        sentences = []
        with open(file_path, 'r') as file:
            for line in file:
                sentences.append(line.replace(".", "").lower().strip())
        return TextManipulator.build_filter(sentences)

    @staticmethod
    def compare_to_model(sentence, text_filter):
        """
        This function compares a sentence with a category filter and
        returns the similarity score. 
        :param sentence: The sentence which should be compared with the model.
        :param text_filter: The category filter to compare the sentence with. 
        :return: A similarity score indicating how well the sentence fits the model. 
        """
        return CLIENT.compare(sentence, text_filter)

    @staticmethod
    def extract_regex(text, regex):
        """
        This function extract matches a regex with the text provided. 
        :param text: The text which needs to searched using a regex.
        :param regex: The regex which will be used to search trough the text.
        :return: A list of matches. 
        """
        regex = re.compile(regex)
        matches = re.findall(regex, text)
        return matches

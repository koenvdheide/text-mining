# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:46:29 2017

@author: RICK
"""

from TextMiner import TextMiner
from nltk.tokenize import sent_tokenize

# global vars
miner = TextMiner()


class ConditionSearcher:
    def __init__(self, condition_sent_model, keyword=None, cut_off=0.4):
        self.keyword = keyword
        self.model = condition_sent_model
        self.cut_off = cut_off
        self.__build_condition_regex()


    # build regex to search through sentences for conditions
    # see
    def __build_condition_regex(self):
        stress_terms = ["stress", "deficiency", "limiting condition", "limiting", "acclimation"]
        rex_parts = r"(?:\s(?:low|high)\s)?(?:\S+\s+and\s)?\S+[ \t]+(?:", ")"
        self.condition_regex = rex_parts[0] + "|".join(stress_terms) + rex_parts[1]


    # extracts conditions from a sentence. Sometimes two terms are mentioned using "and"
    # these will be splitted to avoid redundancy
    def __extract_conditions(self, sentence):
        condition_list = []
        conditions = TextMiner.extract_regex(sentence, self.condition_regex)
        conditions = self.__after_filter(conditions)
        for condition in conditions:
            if "and" in condition:
                first, second = self.__parse_condition(condition)
                condition_list.extend([first, second])
            else:
                condition_list.append(condition)
        return condition_list


    # After filter to reduce regex complexity and enhance efficiency
    # (lookbehind regex would be less efficient)
    # removes conditions like their stress, the stress, under stress etc.
    def __after_filter(self, conditions):
        remove = ["their", "the", "under", "during", "against", "to", "from", "a", "in", "these"]
        for condition in conditions:
            if len(condition.split()) == 2 and condition.split()[0] in remove:
                conditions.remove(condition)
        return conditions


    # This function splits a combined condition
    # ONLY SUPPORTS TWO TYPES NOW, namely thing like "salt and water stress" and "low temp and high temp"
    # probably more forms are possible and should be added
    def __parse_condition(self, combined_condition):
        cond_list = combined_condition.split()
        if len(cond_list) == 4:  # like salt and water stress
            first, second = self.__split_condition(cond_list)
        else:
            first, second = combined_condition.split("and")[0], combined_condition.split("and")[1]
            return first, second


    # split words seperated by 'AND'
    def __split_condition(self, cond_list):
        first, second, cond_type = cond_list[0], cond_list[2], cond_list[3]
        return first + " " + cond_type, second + " " + cond_type


    # this function will check for every sentence in the abstract if this sentence fits
    # the model and uses the similarity (score) to determine if this is above the cut_off.
    # if this is the case the condition will be extracted from this sentence
    def search(self, abstract):
        conditions = []
        for sent in sent_tokenize(abstract):
            if self.keyword in sent:
                score = miner.compare_to_model(sent, self.model)  # returns similarity percentage (decimal)
                if score > self.cut_off:
                    for condition in self.__extract_conditions(sent):
                        conditions.append((score, condition, sent))
        return conditions

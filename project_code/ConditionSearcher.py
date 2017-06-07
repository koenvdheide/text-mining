from TextManipulator import TextManipulator
from nltk.tokenize import sent_tokenize
from Condition import Condition


class ConditionSearcher:
    """
    This Class can be used to search for conditions in a text corpus. The condition 
    identification is based on roughly three steps: keyword check, model comparison
    and regex condition extraction. 
    NOTE: We choose to use the after_filter function instead of further complicating
    the regex. This choice also increases runtime becuase a lookbehind regex is 
    relatively slow (see: https://stackoverflow.com/questions/35476547/regex-negative-lookbehind-and-lookahead-equivalence-and-performance)
    """

    def __init__(self, condition_sent_model, keyword=None, cut_off=0.4):
        """
        The default cut_off of 0.4 (i.e. 40%) performed really well during testing, however this 
        can be adjusted to (possibly) reduce false positives. 
        :param condition_sent_model: The model to which a conditions sentence should be compared.
        :param keyword: A keyword that should be present in the same sentence as the condition.
        :param cut_off: The cut_off that should be used when comparing a sentence with the model
        """
        self.keyword = keyword
        self.model = condition_sent_model
        self.cut_off = cut_off
        self.__build_condition_regex()


    def __build_condition_regex(self):
        """
        This function builds a regex which will match relevant conditions.
        See https://regex101.com/r/ZVIeYO/1 for some examples.
        :return: A regex that can be used to search for conditions.
        """
        stress_terms = ["stress", "deficiency", "limiting condition", "limiting", "acclimation"]
        rex_parts = r"(?:\s(?:low|high)\s)?(?:\S+\s+and\s)?\S+[ \t]+(?:", ")"
        self.condition_regex = rex_parts[0] + "|".join(stress_terms) + rex_parts[1]


    def __extract_conditions(self, sentence):
        """
        This function extracts conditions from the text provided using a regex.
        Sometimes conditions are combined (e.g. water AND heat stress), these
        conditions are first splitted using the  __parse_condition function.
        :param sentence: The sentence in which the conditions should be searched.
        :return: A list of conditions found in the sentence.
        """
        condition_list = []
        conditions = TextManipulator.extract_regex(sentence, self.condition_regex)
        conditions = self.__after_filter(conditions)
        for condition in conditions:
            if "and" in condition:
                first, second = self.__parse_condition(condition)
                condition_list.extend([first, second])
            else:
                condition_list.append(condition)
        return condition_list


    def __after_filter(self, conditions):
        """
        This function serves as filter after the regex. This choice was made to reduce
        regex complexity and enhance regex search speed.
        :param conditions: A list of conditions which should be filtered.
        :return: A list of filtered conditions.
        """
        remove = ["their", "the", "under", "during", "against", "to", "from", "a", "in", "these","of"]
        for condition in conditions:
            if len(condition.split()) == 2 and condition.split()[0] in remove:
                conditions.remove(condition)
        return conditions


    def __parse_condition(self, combined_condition):
        """
        This function splits combined conditions (e.g. "salt and water stress" or "low temperature and
        high temperature".
        NOTE: We assumed that we encounter two combined conditions only, probably three or more conditions
        could be combined an this should be added. 
        :param combined_condition: A combined condition.
        :return: the first and second part of the condition.
        """
        cond_list = combined_condition.split()
        if len(cond_list) == 4:  # like salt and water stress
            first, second, cond_type = cond_list[0], cond_list[2], cond_list[3]
            first,second = first + " " + cond_type, second + " " + cond_type
        else:
            first, second = combined_condition.split("and")[0], combined_condition.split("and")[1]
        return first, second


    def search(self, abstract):
        """
        This function searches through the abstract for conditions.
        :param abstract: The abstract in which the condition should be searched.
        :return: A list of the conditions found in the abstract.
        """
        if abstract:
            conditions = []
            for sent in sent_tokenize(abstract):
                if self.keyword in sent:
                    score = TextManipulator.compare_to_model(sent, self.model)  # returns similarity percentage (decimal)
                    if score > self.cut_off:
                        for condition in self.__extract_conditions(sent):
                            conditions.append(Condition((score, condition, sent)))
            return conditions
        else:
            return None

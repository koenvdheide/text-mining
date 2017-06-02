class Condition:
    """
    This class stores the information for the conditions found in the article.
    This information consists of the condition, a similarity score (see TextManipulator class) 
    and the sentence in which the condition was found.
    """

    def __init__(self,entry):
        """
        :param entry: A tuple/list containing the score, condition and sentence.
        """
        self.score = entry[0]
        self.condition = entry[1]
        self.sentence = entry[2]

    def set_condition(self,condition):
        """
        :param condition: The condition 
        """
        self.condition = condition

    def set_score(self, score):
        """
        :param score: The similarity score belonging tot the condition. 
        """
        self.score = score

    def set_sentence(self,sentence):
        """
        :param sentence: The sentence in which the condition was found.
        """
        self.sentence = sentence

    def get_condition(self):
        """
        :return: The condition.
        """
        return self.condition

    def get_score(self):
        """
        :return: The similarity score belonging tot the condition.
        """
        return self.score

    def get_sentence(self):
        """
        :return: The sentence in which the condition was found.
        """
        return self.sentence

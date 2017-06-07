class TaggedArticle:
    """
    This class stores the annotation found in an PubMed article.
    We chose to use a dictionary to store all the annotation over
    the usage of specific annotation getter/setters. Because this
    dictionary is generic. 
    """

    def __init__(self, pmid):
        """
        :param pmid: The article id. 
        """
        self.id = pmid
        self.annotation = {}


    def get_id(self):
        """
        :return: The article id.
        """
        return self.id

    def get_annotation(self):
        """
        This function will return a dicitonary in which the key
        represents the type of annotations (e.g. Gene) and the 
        value contains a list of words which belong to the type
        of annotations.
        :return: A dictionary containing the annotation. 
        """
        return self.annotation

    def add_annotation(self, tag_type, value):
        """
        This function adds annotation to the dictionary.
        :param tag_type: The type of annotation (e.g. Gene, Species, Chemical)
        :param value: The word corresponding to the annotation (e.g. PAP1)
        """
        if tag_type in self.annotation:
            old = self.annotation[tag_type]
            old.add(value)
            self.annotation[tag_type] = old
        else:
            self.annotation[tag_type] = set([value])







class AnnotatedArticle:
    """
    This Class stores all the information found in the article or belonging to the article, such as:
    PMID, article title, authors, abstract, organisms, genes and conditions. All this information 
    can be manipulated and retrieved using getters/setters.
    """

    def __init__(self):
        """
        This functions initializes all the information entities with None 
        """
        self.organisms = None
        self.genes = None
        self.id = None
        self.authors = None
        self.conditions = None
        self.abstract = None
        self.title = None

    def set_all(self,id,title,authors,abstract,conditions,genes,organisms):
        """
        This method can be used to "set" all the data entities at once
        :param id: The PubMed identifier (id) for the article. 
        :param title: The title of the abstract.
        :param authors: The authors of the article.
        :param abstract: The article abstract.
        :param conditions: The conditions found in the article (as Condition objects).
        :param genes: The genes present in the article (as Gene objects).
        :param organisms: The organisms present in the article (as Organism objects).
        """
        self.id = id
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.conditions = conditions
        self.genes = genes
        self.organisms = organisms

    def set_id(self, pmid):
        """
        :param pmid: The PubMed identifier (id) for the article. 
        """
        self.id = pmid

    def set_title(self, title):
        """
        :param title: The title of the abstract.
        """

    def set_genes(self,genes):
        """
        :param genes: The genes found in the article (as Gene objects).
        """
        self.genes = genes

    def set_organisms(self, organisms):
        """
        :param organisms: The organisms found in the article (as Organism objects).
        """
        self.organisms = organisms

    def set_conditions(self, conditions):
        """
        :param organisms: The conditions found in the article (as Condition objects).
        """
        self.conditions = conditions

    def set_abstract(self, abstract):
        """
        :param abstract: The article abstract.
        """
        self.abstract = abstract

    def set_authors(self, authors):
        """
        :param authors: The authors of the article.
        """
        self.authors = authors

    def get_id(self):
        """
        :return: The PubMed identifier (id).
        """
        return self.id

    def get_title(self):
        """
        :return: The article title.
        """
        return self.title

    def get_genes(self):
        """
        :return: The genes present in the article (as Gene objects).
        """
        return self.genes

    def get_organisms(self):
        """
        :return: The organisms present in the article (as Organism objects).
        """
        return self.organisms

    def get_authors(self):
        """
        :return: The authors of the article.
        """
        return self.authors

    def get_conditions(self):
        """
        :return: organisms: The conditions found in the article (as Condition objects).
        """
        return self.conditions

    def __str__(self):
        """
        Override this function to print the content of the object instead of it's reference.
        Note: Every value is converted to string to be able to print None type values
        :return: A string containing the content of the object.
        """
        new_line = "\n"
        content = ""
        content += "id: " + str(self.id) + new_line
        content += "title: " + str(self.title) + new_line
        content += "authors: " + str(self.authors) + new_line
        content += "abstract: " + str(self.abstract) + new_line
        if self.conditions:
            content += "conditions: " + \
                       ", ".join([condition.get_condition() for condition in self.conditions if condition.get_condition is not None]) \
                       + new_line
        else:
            content += "conditions: " + str(None) + new_line
        if self.genes:
            content += "genes: " + \
                       ", ".join([gene.get_gene_name() for gene in self.genes if gene.get_gene_name is not None]) \
                       + new_line
        else:
            content += "genes: " + str(None) + new_line
        if self.organisms:
            content += "organisms: " + \
                       ", ".join([organism.get_scientific_name() for organism in self.organisms if organism.get_scientific_name() is not None]) \
                       + new_line
        else:
            content += "organisms: " + str(None) + new_line
        return content
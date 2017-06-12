class AnnotatedArticle:
    """
    This Class stores all the information found in the article or belonging to the article, such as:
    PMID, article title, authors, abstract, organisms, genes and conditions. All this information 
    can be manipulated and retrieved using getters/setters.
    """

    def __init__(self,id, title, authors,abstract, conditions, genes, organisms ):
        """ 
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

    def to_dict(self):
        """
        This function convert the AnnotatedArticle object to a dictionary.        
        :return: A dictionary of the AnnotatedArticle.
        """
        return {"Article": {
            "pubmed_id": self.get_id(),
            "title":self.get_title(),
            "authors":self.get_authors(),
        },
            "Gene": set([gene.to_dict() for gene in self.get_genes() if gene]),
            "Organism": set([organism.to_dict() for organism in self.get_organisms() if organism]),
            "Condition": set([condition.to_dict() for condition in self.get_conditions()])
        }



class Organism:
    """
    This class is a wrapper for all the information regarding organisms.
    A organism name is needed to initialize this Class. Further a NCBI
    gene entry can be added. This entry will be parsed to retrieve
    the scientific name, common name and tax ID. Which are 
    subsequently stored in the Organism object. The genus is derived
    from the scientific name.
    """

    def __init__(self, organism_name):
        """
        This function saves the organism name and stores None in all other entities.
        :param organism_name: The name of the organism
        """
        self.name = str(organism_name)
        self.scientific_name = None
        self.common_name = None
        self.genus = None
        self.tax_id = None

    def load_entry(self, entry):
        """
        This function parses a NCBI gene entry and stores the corresponding information.
        :param Entry: NCBI organism entry. 
        NOTE: This function is purposely separated from the __init__ because the tex-mining
        algorithm can find organisms which do not have annotation in NCBI and this separation
        will allow the initiation of a Organism object without having to pass a gene entry. 
        """
        self.scientific_name = str(entry.get('ScientificName', None))
        self.common_name = str(entry.get('CommonName', None))
        self.tax_id = entry.get('Id', None)

    def get_scientific_name(self):
        """
        :return: The scientific name of the organism.
        """
        return self.scientific_name

    def get_name(self):
        """
        :return: The name as found in the text.
        """
        if self.get_scientific_name():
            return self.scientific_name
        else:
            return self.name

    def get_common_name(self):
        """
        :return: The common name of the organism.
        """
        return self.common_name

    def get_id(self):
        """
        :return: The taxonomic ID.
        """
        return self.tax_id

    def get_genus(self):
        """
        :return: The genus of the organism.
        """
        if self.get_scientific_name():
            return self.get_scientific_name().split()[0]
        else:
            return None

    def to_dict(self):
        """
        :return: Dictionary of this Gene object.
        """
        return {"taxonomy_id": self.get_id(), "name": self.get_scientific_name(), "common_name": self.get_common_name(),
                "genus": self.get_genus()}


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
        self.name = organism_name
        self.scientific_name = None
        self.common_name = None
        self.genus = None
        self.tax_id = None


    def load_entry(self, entry):
        """
        This function parses a NCBI gene entry and stores the corresponding information.
        :param Entry: NCBI organism entry. 
        """
        self.scientific_name = entry.get('ScientificName',None)
        self.common_name = entry.get('CommonName',None)
        self.tax_id = entry.get('Id',None)

    def get_scientific_name(self):
        """
        :return: The scientific name of the organism.
        """
        return self.scientific_name

    def get_name(self):
        """
        :return: The name as found in the text
        """
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
        return {"taxonomy_id":self.get_id(),"name":self.get_scientific_name(),"common_name":self.get_common_name(),"genus":self.get_genus()}

    def __eq__(self,other):
        """
        Override this function to be able to extract unique genes from a list.
        preferable based on the scientific name, but if this information isn't 
        available the initialisation name will be used. 
        :param other: The (Organism) object which should be compared with THIS organism object.
        :return: True if both object share the same name, otherwise False will be returned. 
        """
        if not isinstance(other, Organism):
            return False
        if self.get_scientific_name() and other.get_scientific_name():
            return self.get_scientific_name() == other.get_scientific_name()
        return self.get_name() == other.get_name()

    def __hash__(self):
        """
        Override this function to hash based on the scientific_name (proffered) or
        the initialisation name. 
        :return: 
        """
        if self.get_scientific_name():
            return hash(self.get_scientific_name())
        return hash(self.get_name())

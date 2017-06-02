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
        self.tax_id = entry.get('TaxID',None)

    def get_scientific_name(self):
        """
        :return: The scientific name of the organism.
        """
        return self.entry['ScientificName']

    def get_name(self):
        """
        :return: The name as found in the text
        """
        return self.name

    def get_common_name(self):
        """
        :return: The common name of the organism.
        """
        return self.entry['CommonName']

    def get_id(self):
        """
        :return: The taxonomic ID.
        """
        return self.entry['TaxID']

    def get_genus(self):
        """
        :return: The genus of the organism.
        """
        return self.get_scientific_name().split()[0]


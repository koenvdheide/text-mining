class Gene:
    """
    This class is a wrapper for all the information regarding genes.
    A gene name is needed to initialize this Class. Further a NCBI
    gene entry can be added. This entry will be parsed to retrieve
    the chromosomal location, description and aliases. Which are 
    subsequently stored in the Gene object. 
    """

    def __init__(self, gene_name):
        """
        This function saves the gene name and stores None in all other entities.
        :param gene_name: The name of the gene.
        """
        self.name = gene_name
        self.location = None
        self.description = None
        self.aliases = None

    def load_entry(self, entry):
        """
        This function parses a NCBI gene entry and stores the corresponding information.
        :param Entry: NCBI gene entry.
        """
        genomic_info = entry.get('GenomicInfo',None)
        if len(genomic_info) > 0:   #need to check if there is genomic info
            self.location = genomic_info[0].get('ChrLoc',None)
        self.aliases = entry.get('OtherAliases',None)
        self.description = entry.get('Description', None)


    def get_gene_name(self):
        """
        :return: The gene name.
        """
        return self.name

    def get_location(self):
        """
        :return: The genomic location of the gene.
        """
        return self.location

    def get_description(self):
        """
        :return: The description of NCBI corresponding to this gene.
        """
        return self.description

    def get_aliases(self):
        """
        :return: Commonly used aliases for the gene
        """
        return self.aliases




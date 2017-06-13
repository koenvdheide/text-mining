from Organism import Organism


class Gene:
    """
    This class is a wrapper for all the information regarding genes.
    A gene name is needed to initialize this Class. Further a NCBI
    gene entry can be added. This entry will be parsed to retrieve
    the chromosomal location, description, orthologs/homologs,
    gene id and aliases. Which are subsequently stored in the 
    Gene object. 
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
        self.accession = None
        self.id = None
        self.homologs = None
        self.organism = None

    def load_entry(self, entry):
        """
        This function parses a NCBI gene entry and stores the corresponding information.
        :param Entry: NCBI gene entry.
        NOTE: This function is purposely separated from the __init__ because the tex-mining
        algorithm can find genes which do not have annotation in NCBI and this separation
        will allow the initiation of a Gene object without having to pass a gene entry. 
        """
        genomic_info = entry.get('GenomicInfo', None)
        if len(genomic_info) > 0:  # need to check if there is genomic info
            self.location = genomic_info[0].get('ChrLoc', None)
        self.aliases = entry.get('OtherAliases', None)
        self.description = entry.get('Description', None)
        self.id = entry.get('Id', None)
        self.homologs = entry.get('homologs', None)
        self.organism = entry.get('Organism', None)

    def get_id(self):
        """
        :return: The gene id.
        """
        return self.id

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

    def get_organism(self):
        """
        :return: The organism information as Organism object. 
        """
        if self.organism:
            organism = Organism(self.organism['ScientificName'])
            organism.load_entry(self.organism)
        return organism

    def get_homologs(self):
        """
        :return: The homologs as dictionary. 
        """
        return self.homologs

    def to_dict(self):
        """
        :return: Dictionary of this Gene object.
        """
        if self.get_id():
            return ({"gene_id": self.get_id(), "name": self.get_gene_name(), "aliasses": self.get_aliases(),
                     "description": self.get_description(), "location": self.get_location(),
                     "Orthologs": self.get_homologs(),
                     "Organism": self.get_organism().to_dict() if self.organism else self.get_organism()})

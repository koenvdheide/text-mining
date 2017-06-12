import time
from Bio import Entrez
from Bio import Medline


class NCBISearcher:
    """
    This Class can be used to query the NCBI PubMed, Gene and Taxonomy database.
    The id's found while querying these databases can be "fetched", this will
    return an MedLine article in the case of PubMed and dictionaries in the case
    of Gene and Taxonomy. These dictionaries can be used as "input" for the 
    Gene or Organisms class. 
    """

    Entrez.email = "r.beeloo@outlook.com"

    @staticmethod
    def search(term, db="pubmed", retrieve_max=100):
        """
        This function can be used to search a specific term in a specific database.
        :param term: The term which should be searched.
        :param db: The database which should be searched using the term provided.   
        :param retrieve_max: The maximum number of articles which should be retrieved.
        :return: A list of article id's. 
        """
        try:
            if term:
                handle = Entrez.esearch(db=db, term=term, retmax=retrieve_max)
                records = Entrez.read(handle)
                handle.close()  # close connection
                return records['IdList']
            else:
                print("Please provide a search term!")
                return None
        except Exception:
            print("A server error occured")

    @staticmethod
    def fetch_articles(id_list):
        """
        This function retrieves the articles corresponding to the given id's and 
        subsequently parses them using the MedLine (BioJava) parser. 
        :param id_list: A list of id's.
        :return: A list of parsed articles corresponding to the given id's.
        """
        articles = []
        count = 0
        if id_list:
            for ID in id_list:
                count += 1

                try:
                    handle = Entrez.efetch(db="pubmed", id=ID, rettype="medline", retmode="text")
                    article = Medline.parse(handle)
                    articles.append(list(article)[0])
                    if count == 500:  # being nice to NCBI
                        print("pause for 30 seconds")
                        time.sleep(30)
                except:
                    continue
            return articles
        else:
            return None

    @staticmethod
    def fetch_genes(id_list):
        """
        This function retrieves NCBI gene entries based on the provided id's.
        :param id_list: A list of NCBI gene id's.
        :return: A list of dictionaries, in which each dictionary represents one gene entry. 
        """
        if id_list:
            record = NCBISearcher.get_records_from_id(db="gene", id_list=id_list)
            genes = [NCBISearcher.add_id(dict(entry), id)
                     for entry in record["DocumentSummarySet"]['DocumentSummary']
                     for id in id_list]
            if len(genes) == 1:
                return genes[0]
            return genes
        else:
            return None

    @staticmethod
    def fetch_organisms(id_list):
        """
        This function retrieves NCBI taxonomy entries based on the provided id's
        :param id_list: A list of NCBI taxonomy id's.
        :return: A list of dictionaries, in which each dictionary represents one organism entry. 
        """
        if id_list:
            record = NCBISearcher.get_records_from_id(db="taxonomy", id_list=id_list)
            organisms = [dict(entry) for entry in record]
            if len(organisms) == 1:
                return organisms[0]
            return organisms
        else:
            return None

    @staticmethod
    def fetch_homologs(id_list):
        """
        This function retrieves NCBI homolog entries based on the provided id's.
        :param id_list: A  list of NCBI homolog id's
        :return: A list of dictionaries, in which each dictionary represents one homolog entry.
        """
        if id_list:
            record = NCBISearcher.get_records_from_id(db="homologene", id_list=id_list)
            homologs = [dict(entry) for entry in record[0]['HomoloGeneDataList']]
            if len(homologs) == 1:
                return homologs[0]
            return homologs
        else:
            return None

    @staticmethod
    def get_records_from_id(db, id_list):
        """
        This function opens a handle, extracts the records and closes the handle.
        :param db: The database from which a summary entry has to be retrieved.
        :param id_list: A list of id's corresponding the provided database.
        :return: The records. 
        """
        if id_list:
            if len(id_list) > 1:
                handle = Entrez.esummary(db=db, id=",".join(id_list), retmode="xml")
            else:
                handle = Entrez.esummary(db=db, id=id_list, retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            return records
        else:
            return None

    @staticmethod
    def add_id(dict, id):
        """
        The NCBI esummary option doesn't return the entry ID. This could be fixed by using efetch, however
        using efetch will drastically increase runtime and won't result in more useful info besides the
        ID. Therefore this function couples the ID's to the esummary results.
        :param dict: Esummary result dictionary
        :param id: A gene id which needs to be added to the esummary dictionary.
        :return: The updated dictionary. 
        """
        dict['Id'] = id
        return dict

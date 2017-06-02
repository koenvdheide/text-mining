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
                handle = Entrez.efetch(db="pubmed", id=ID, rettype="medline", retmode="text")
                try:
                    article = Medline.parse(handle)
                    articles.append(list(article)[0])
                    if count ==500: #being nice to NCBI
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
        :return: A list of dictionaries, in which each dictionary represents one entry. 
        """
        if id_list:
            if len(id_list) > 1:
                handle = Entrez.esummary(db="gene", id=",".join(id_list), retmode="xml")
            else:
                handle = Entrez.esummary(db="gene", id=id_list, retmode="xml")
            record = Entrez.read(handle)
            handle.close()
            genes = [dict(entry) for entry in record["DocumentSummarySet"]['DocumentSummary']]
            return genes
        else:
            return None

    @staticmethod
    def fetch_organisms(id_list):
        """
        This function retrieves NCBI taxonomy entries based on the provided id's
        :param id_list: A list of NCBI taxonomy id's.
        :return: A list of dictionaries, in which each dictionary represents one entry. 
        """
        if id_list:
            if len(id_list) > 1:
                handle = Entrez.esummary(db="taxonomy", id=",".join(id_list), retmode="xml")
            else:
                handle = Entrez.esummary(db="taxonomy", id=id_list, retmode="xml")
            record = Entrez.read(handle)
            handle.close()
            organisms = [dict(entry) for entry in record]
            return organisms
        else:
            return None



import urllib.request
import bioc
from nltk.stem.wordnet import WordNetLemmatizer
from TaggedArticle import TaggedArticle

ENCODING = "utf-8"
URL_BASE = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/"
LEMMATIZER = WordNetLemmatizer()


class Tagger:
    """
    This class uses the PubTator API (available at: https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/)
    to retrieve Gene, Chemical and Species information based on a list of PMID's (PubMed ID's). 
    """

    def __init__(self):
        """
        Initialize the concept to use (meaning which "kind" of words need to be tagged,
        in this case: Genes, Chemicals and Species) and to initialize which format
        should be used when the results are returned by the API. 
        """
        self.concept = "BioConcept"
        self.format = "BioC"

    def change_concept(self, new_concept):
        """
        This function can be used to change the concept (see __init__)
        :param new_concept: The new concept that should be used.
        """
        self.concept = new_concept

    def change_format(self, new_format):
        """
        This function can be used to change the format returned by the API (see __init__).
        :param new_format: The new retrieval format that should be used.
        """
        self.format = new_format

    def tag(self, pmid_list, wanted_tags=["Gene", "Species"]):
        """
        This function tags a set of articles based on the PMID's provided. 
        :param pmid_list: The PMID's of the articles which need to be tagged.
        :param wanted_tags: The tags of the words which should be returned. 
        :return: A Tag object containing article information accompanied by
                 the words corresponding to the wanted_tags. 
        """
        tagged_articles = []
        for pmid in pmid_list:
            pmid = str(pmid).replace("PMID:", "").strip()
            document = self.__retrieve_document(pmid)
            if document:
                tagged_article = TaggedArticle(pmid)
                tagged_article = self.__extract_tags(tagged_article, document, wanted_tags)
                tagged_articles.append(tagged_article)
        return tagged_articles

    def __retrieve_document(self, pmid):
        """
        This function communicates with the PubTator API to retrieve the tagged article.
        :param pmid: The PMID corresponding to the article which needs to be tagged.
        :return: A tagged document. 
        """
        url = URL_BASE + self.concept + "/" + pmid + "/" + self.format + "/"
        try:
            response = urllib.request.urlopen(url).read()
            collection = self.__decode(response)
            document = collection.documents[0]  # index 0 because we only searcher one PMID
        except:
            return None
        return document

    def __decode(self, response):
        """
        This function decodes the response from the API to a collection from which
        the tag information can be read. 
        :param response: 
        :return: 
        """
        response_decoded = response.decode(ENCODING)
        collection = bioc.loads(response_decoded, ENCODING)
        return collection

    def __extract_tags(self, tagged_article, document, wanted_tags):
        """
        This function extract the words corresponding to the wanted_tags and 
        lemmatizes these, to reduce redundancy. These words are saved in 
        the Tag object. 
        :param tagged_article: A tagged article.
        :param document: The document corresponding to the tagged_article. 
        :param wanted_tags: The words corresponding to these tags are saved.
        :return: An Tag object containing the article information + the wanted words. 
        """
        for anno in list(bioc.annotations(document)):
            tag = anno.infons['type']
            for wanted_tag in wanted_tags:
                if wanted_tag == tag:
                    word = LEMMATIZER.lemmatize(anno.text)  # e.g. rats --> rat, so to reduce redundancy
                    tagged_article.add_annotation(tag, word)
        return tagged_article

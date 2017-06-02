import urllib.request
import bioc
from nltk.stem.wordnet import WordNetLemmatizer
from Tag import Tag

ENCODING = "utf-8"
URL_BASE = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/"
LEMMATIZER = WordNetLemmatizer()


class Tagger:

    def __init__(self):
        self.concept = "BioConcept"
        self.format = "BioC"

    def change_concept(self,new_concept):
        self.concept = new_concept

    def change_format(self, new_format):
        self.format = new_format

    def tag(self,pmid_list, wanted_tags = ["Gene","Species"]):
        tagged_articles = []
        for pmid in pmid_list:
            pmid = str(pmid).replace("PMID:","").strip()
            document = self.__retrieve_document(pmid)
            if document:
                tagged_article = Tag(pmid)
                tagged_article = self.__extract_tags(tagged_article, document, wanted_tags)
                tagged_articles.append(tagged_article)
        return tagged_articles


    def __retrieve_document(self,pmid):
        url = URL_BASE + self.concept + "/" + pmid + "/" + self.format + "/"
        try:
            response = urllib.request.urlopen(url).read()
            collection = self.__decode(response)
            document = collection.documents[0] #index 0 because we only searcher one PMID
        except:
            return None
        return document


    def __decode(self,response):
        response_decoded = response.decode(ENCODING)
        collection = bioc.loads(response_decoded, ENCODING)
        return collection


    def __extract_tags(self,tagged_article, document, wanted_tags):
        for anno in list(bioc.annotations(document)):
            tag = anno.infons['type']
            for wanted_tag in wanted_tags:
                if wanted_tag == tag:
                    word = LEMMATIZER.lemmatize(anno.text) #e.g. rats --> rat, so to reduce redundancy
                    tagged_article.add_annotation(tag, word)
        return tagged_article








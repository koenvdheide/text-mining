from NCBISearcher import NCBISearcher
from Tagger import Tagger
from Gene import Gene
from Organism import Organism
from ConditionSearcher import ConditionSearcher
from TextManipulator import TextManipulator
from AnnotatedArticle import AnnotatedArticle


def gather_info(terms, type, search_keyword=""):
    final_objects = []
    for term in terms:
        if type == "gene":
            object = Gene(term)
        if type =="taxonomy":
            object = Organism(term)
        ids = NCBISearcher.search(term + search_keyword, type, 1)
        if ids:
            id = ids[0] #we only searched for one se we can use index 0
            if type == "gene":
                entries = NCBISearcher.fetch_genes([id])
            elif type == "taxonomy":
                entries = NCBISearcher.fetch_organisms([id])
            object.load_entry(entries[0])
        final_objects.append(object)
    return(final_objects)

def get_entities(id):
    tagger = Tagger()
    tagged_article = tagger.tag([id], wanted_tags = ["Gene","Species"])[0]
    annotation = tagged_article.get_annotation()
    genes = annotation.get('Gene', None)
    organisms = annotation.get("Species", None)
    if genes:
        genes = gather_info(genes,type="gene", search_keyword="[SYMBOL]")
    if organisms:
        organisms = gather_info(organisms,type="taxonomy")
    return genes,organisms


def save_in_database(annotated_articles):
    for article in annotated_articles:
        print("title: " + article.get_title())


def main():
    condition_model = TextManipulator.build_filter_from_file("docs/conditie_zinnen.txt")
    condition_searcher = ConditionSearcher(condition_model,keyword="anthocyanin")

    #let's search
    ids = NCBISearcher.search("anthocyanin","pubmed",50)
    annotated_articles = []
    for article in NCBISearcher.fetch_articles(ids):
        title = article.get("TI",None)
        abstract = article.get("AB", None)
        authors = article.get("AU",None)
        pmid = article.get("PMID",None)
        conditions = condition_searcher.search(abstract)
        if conditions:
            genes, organisms = get_entities(pmid)
            annotated_article = AnnotatedArticle()
            annotated_article.set_all(pmid,title,authors,abstract,conditions,genes,organisms)
            print(annotated_article)
            annotated_articles.append(annotated_article)
    save_in_database(annotated_articles)



main()
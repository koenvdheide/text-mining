from NCBISearcher import NCBISearcher
from ConditionSearcher import ConditionSearcher
from AnnotatedArticle import AnnotatedArticle
from Tagger import Tagger
from TextManipulator import TextManipulator
from Gene import Gene
from Organism import Organism
from SQLConnector import SQLConnector
from Bio import Entrez

Entrez.email = "r.beeloo@outlook.com"


def extract_entities(pmid):
    """
    This function tags genes and species in the PubMed article (based on the id provided).
    If possible these genes and species are further annotated using information present
    in the NCBi gene/taxonomy database. 
    :param pmid: The id of the article that should be tagged.
    :return: The genes (as Gene objects) and the organisms (as Organism object) found in the article. 
    """
    tagger = Tagger()
    tag_object = tagger.tag([pmid])
    if tag_object:
        tag_object = tag_object[0]
        annotation = tag_object.get_annotation()
        genes = annotation.get("Gene", {None})
        organisms = annotation.get("Species", {None})
        genes = [convert_to_object(gene, "Gene") for gene in genes]
        organisms = [convert_to_object(organism, "Species") for organism in organisms]
    return genes, organisms


def convert_to_object(data, type):
    """
    This function creates either a Gene or Organism object and adds extra information from NCBI (if possible). 
    :param data: A gene or species name.
    :param type: The type of the data, this could be Gene or Organism. 
    :return: An Organism of Gene object (depending on the input type). 
    """
    if data is not None:
        if type == "Gene":
            gen = Gene(data)
            gen = gather_extra_data(gen, data, "gene")
            return gen
        if type == "Species":
            organism = Organism(data)
            organism = gather_extra_data(organism, data, "taxonomy")
            return organism
    return None


def gather_extra_data(entity_object, term, database):
    """
    This function searches through NCBI for extra information about
    a specific gene or organism. 
    :param entity_object: A Gene or Organism object.
    :param term: The term that should be used to search through NCBI
    :param database: The database that needs to be searched.
    :return: A entity object containing additional information from NCBI (if available)
    """
    ids = NCBISearcher.search(term, database, 1)
    if ids:
        id = ids[0]  # we only searched for one
        if database == "gene":
            entry = NCBISearcher.fetch_genes([id])
            homologs_ids = NCBISearcher.search(term, "homologene", 1)
            if homologs_ids:
                homologs = NCBISearcher.fetch_homologs(homologs_ids)
                entry['homologs'] = homologs  # add homolog data to NCBI gene entry
        if database == "taxonomy":
            entry = NCBISearcher.fetch_organisms([id])
        if entry:
            entity_object.load_entry(entry)
    return entity_object


# AL DEZE SHIT NOG IN EIGEN CLASS INCLUSIEF GLOBALE VARIABELEN
GENUS_ID = 1


def insert_article(annotation_data):
    sqlconnection = SQLConnector(database="test")  # LET OP DATABASE NAAM
    session = sqlconnection.get_session()

    organisms_data = annotation_data['Organism']
    gene_data = annotation_data['Gene']
    article_data = annotation_data['Article']
    textmatch_data = annotation_data['Condition']

    global GENUS_ID

    for organism in organisms_data:  # organisms without genes
        genus_present = sqlconnection.check_data(session, 'organism_genus', str(organism['genus']))
        organism_present = sqlconnection.check_data(session, 'organism', int(organism['taxonomy_id']))

        if genus_present == False:
            genus_insert = sqlconnection.insertion(table_name='organism_genus',
                                                   values={'id': GENUS_ID, 'name': str(organism['genus'])})
            if organism_present == False:
                organism_insert = sqlconnection.insertion(table_name='organism',
                                                          values={'taxonomy_id': int(organism['taxonomy_id']),
                                                                  'name': str(organism['name']),
                                                                  'common_name': str(organism['common_name']),
                                                                  'organism_genus': genus_insert})
            elif organism_present:
                print("HELP")

            elif organism_present == None:
                print("Empty organism data found")

        elif genus_present:
            if organism_present == False:
                organism_insert = sqlconnection.insertion(table_name='organism',
                                                          values={'taxonomy_id': int(organism['taxonomy_id']),
                                                                  'name': str(organism['name']),
                                                                  'common_name': str(organism['common_name']),
                                                                  'organism_genus': genus_present})
            elif organism_present:
                print("HELP")

            elif organism_present == None:
                print("Empty organism data found")

        elif genus_present == None:
            print("Empty genus data found")

        session.add(organism_insert)
        GENUS_ID = genus_insert.id + 1

    # for gene in gene_data:
    #     gene_insert = sqlconnection.insertion(table_name='gene',
    #                                           values={'gene_id': int(gene['gene_id']), 'name': str(gene['name']),
    #                                                   'location': str(gene['location']),
    #                                                   'aliases': str(gene['aliasses']),
    #                                                   'description': str(gene['description'])})
    #     session.add(gene_insert)
    #
    # article_insert = sqlconnection.insertion(table_name='article', values={'pubmed_id': int(article_data['pubmed_id']),
    #                                                                        'authors': str(article_data['authors']),
    #                                                                        'title': str(article_data['title'])})
    #
    # session.add(article_insert)

    # stress_insert = sqlconnection.insertion(table_name='stress',values={'name':textmatch_data['name']})
    # session.add(stress_insert)
    #
    # textmatch_insert = sqlconnection.insertion(table_name='textmatch',values={})
    # session.add(textmatch_insert)

    session.commit()



def main():
    condition_model = TextManipulator.build_filter_from_file("docs/conditie_zinnen.txt")
    condition_searcher = ConditionSearcher(condition_model, keyword="anthocyanin")

    ids = NCBISearcher.search("anthocyanin", "pubmed", 1000)
    for id in ids:
        article = NCBISearcher.fetch_articles([id])[0]
        abstract = article.get("AB", "?")
        conditions = condition_searcher.search(abstract)
        if conditions:
            id = article.get("PMID", None)
            title = article.get("TI", None)
            authors = article.get("AU", None)
            print("condition found: " + str(id))
            genes, organisms = extract_entities(id)
            anno_article = AnnotatedArticle(id, title, authors, abstract, conditions, genes, organisms)
            # print(anno_article.to_dict())
            insert_article(anno_article.to_dict())


main()

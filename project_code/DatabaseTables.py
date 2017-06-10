# from SQLConnector import SQLConnector
#
# from sqlalchemy import inspect
#
# DATABASE = SQLConnector()
# SESSION = DATABASE.get_session()
# BASE = DATABASE.get_base()
#
#
# GeneTable = BASE.classes.gene
# OrganismTable = BASE.classes.organism
# GenusTable = BASE.classes.organism_genus
# SentenceTable = BASE.classes.textmatch
# GeneCategoryTable = BASE.classes.gene_category
# ConditionTable = BASE.classes.stress
# ArticleTable = BASE.classes.article
# OrthologsTable = BASE.classes.orthologs
#
# i = inspect(GeneTable).relationships
# print([rel.mapper.class_ for rel in i])
#
# SESSION.add(GeneTable(gene_id=4, name="lol", sequence="mkay", location="space", aliases="bruh,duh",
#                       description="HELP I AM STUCK IN A DATABASE", gene_category=(GeneCategoryTable(id=3))))
#
# SESSION.commit()
#
# # class GeneTable:
# #     def __init__(self, dictvalues={'gene_id': 1, 'location': 'great'}, table=database.get_table("gene")):
# #         insertion = table(**dictvalues)
# #
# #
# # GeneTable()
#
# # gene_id=1, name=None, sequence=None, location=None, aliases=None, description=None,category_id=1

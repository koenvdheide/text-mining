import mysql.connector


class SQLInsertor:

    genus_id = 0
    stress_id = 0
    category_id = 0
    match_id = 0

    def __init__(self, host="127.0.0.1", user="root", password="usbw", db='test', port=3307):

        try:
            self.cnx = mysql.connector.connect(user, password, host, port, db)

            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as error:
            print("Error occured while connecting to SQL database: {}".format(error))


SQLInsertor()






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

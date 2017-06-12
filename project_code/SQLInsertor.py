from SQLConnector import SQLConnector


class SQLInsertor:
    genus_id = 0
    stress_id = 0
    category_id = 0
    match_id = 0

    def insert_article(annotation_data):
        sqlconnection = SQLConnector(database="test")  # LET OP DATABASE NAAM
        session = sqlconnection.get_session()

        organisms_data = annotation_data['Organism']
        gene_data = annotation_data['Gene']
        article_data = annotation_data['Article']
        textmatch_data = annotation_data['Condition']

        global GENUS_ID

        for organism in organisms_data:  # organisms without genes

            if organism['taxonomy_id'] is not None:
                genus_check = sqlconnection.get_or_create(session=session, table_name='organism_genus',
                                                          id=GENUS_ID, name=str(organism['genus']))

                genus_insert = genus_check[0]
                genus_present = genus_check[1]

                if genus_present == False:
                    organism_check = sqlconnection.get_or_create(session=session, table_name='organism',
                                                                 taxonomy_id=int(organism['taxonomy_id']),
                                                                 name=str(organism['name']),
                                                                 common_name=str(organism['common_name']),
                                                                 organism_genus=genus_insert)
                    organism_insert = organism_check[0]
                    organism_present = organism_check[1]

                    if organism_present == False:
                        session.add(organism_insert)

                    elif organism_present:
                        print("genus niet maar organisme wel, wtf m8")



                elif genus_present:
                    organism_check = sqlconnection.get_or_create(session=session, table_name='organism',
                                                                 taxonomy_id=int(organism['taxonomy_id']),
                                                                 name=str(organism['name']),
                                                                 common_name=str(organism['common_name']),
                                                                 Organism_genus_id=genus_insert.id)
                    organism_insert = organism_check[0]
                    organism_present = organism_check[1]

                    if organism_present == False:
                        session.add(organism_insert)

                    elif organism_present:
                        print("identieke shizzle gevonden")


                    else:
                        print("ERROR")

                GENUS_ID += 1

                session.commit()
            else:
                print("Empty organism data found: " + str(organism))


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

from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


class ColumnLengthMismatchException(Exception):
    """

    """
    pass


class TableNotFoundException(Exception):
    """

    """
    pass


class SQLConnector:
    genus_id = 0
    stress_id = 0
    category_id = 0
    match_id = 0
    """
    
    """

    def __init__(self, sqldialect="mysql", driver="mysqlconnector", username="root", password="usbw", host="localhost",
                 port="3307", database="test"):
        """
        
        :param sqldialect: 
        :param driver: 
        :param username: 
        :param password: 
        :param host: 
        :param port: 
        :param database: 
        """
        engine_argument = sqldialect + "+" + driver + "://" + username + ":" + password + "@" + host + ":" + port + "/" + database
        self.engine = create_engine(engine_argument, echo=True)  # mogelijk text encoding nog toevoegen

        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)

    def get_tables_as_classes(self):
        """

        :return: 
        """
        return self.Base.classes

    def get_table_class(self, table_name):
        """
        
        :param table_name: 
        :return: 
        """
        tables = self.get_tables_as_classes()
        if table_name in tables:
            return getattr(self.Base.classes, table_name)
        else:
            raise TableNotFoundException("Specified table not found")

    def get_session(self):
        """
        
        :return: 
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def insertion(self, table_name, values):
        """
        
        :param table_name: 
        :param values: 
        :return: 
        """
        table_class = self.get_table_class(table_name)
        return table_class(**values)

    # https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    def get_or_create(self, session, table_name, **kwargs):

        table = self.get_table_class(table_name)
        instance = session.query(table).filter_by(**kwargs).first()
        if instance:
            return instance, True
        else:
            instance = table(**kwargs)
            return instance, False

    def get_primary_key(self, table_name):
        table = self.get_table_class(table_name)
        pk = inspect(table).identity
        return pk

    def insert_article(self, annotation_data):

        organisms_data = annotation_data['Organism']
        gene_data = annotation_data['Gene']
        article_data = annotation_data['Article']
        textmatch_data = annotation_data['Condition']

        session = self.get_session()

        for organism in organisms_data:  # organisms without genes

            if organism and organism['taxonomy_id'] is not None:
                genus_check = self.get_or_create(session=session, table_name='organism_genus',
                                                 id=self.genus_id, name=str(organism['genus']))
                genus_insert = genus_check[0]
                genus_present = genus_check[1]

                if genus_present == False:
                    organism_check = self.get_or_create(session=session, table_name='organism',
                                                        taxonomy_id=int(organism['taxonomy_id']),
                                                        name=str(organism['name']),
                                                        common_name=str(organism['common_name']),
                                                        organism_genus=genus_insert)
                    organism_insert = organism_check[0]
                    organism_present = organism_check[1]

                    if organism_present == False:
                        session.merge(organism_insert)
                        session.commit()
                        self.genus_id += 1

                    elif organism_present:
                        print("genus niet maar organisme wel, wtf m8")
                        self.genus_id += 1

                elif genus_present:
                    organism_check = self.get_or_create(session=session, table_name='organism',
                                                        taxonomy_id=int(organism['taxonomy_id']),
                                                        name=str(organism['name']),
                                                        common_name=str(organism['common_name']),
                                                        Organism_genus_id=genus_insert.id)  # wordt iedere keer als uniek beschouwd omdat je nieuwe id krigt?
                    organism_insert = organism_check[0]
                    organism_present = organism_check[1]

                    if organism_present == False:
                        session.merge(organism_insert)
                        session.commit()

                    elif organism_present:
                        print("identieke shizzle gevonden")

                    else:
                        print("ERROR")
            else:
                print("Empty organism data found: " + str(organism))

        for gene in gene_data:
            if gene and gene['gene_id'] is not None:
                gene_check = self.get_or_create(session=session, table_name='gene',
                                                gene_id=int(gene['gene_id']), name=str(gene['name']),
                                                location=str(gene['location']),
                                                aliases=str(gene['aliasses']),
                                                description=str(gene['description']))
                gene_insert = gene_check[0]
                gene_present = gene_check[1]
                if gene_present == False:
                    session.add(gene_insert)
                    session.commit()
        if article_data and article_data['pubmed_id'] is not None:
            article_check = self.get_or_create(session=session, table_name='article',
                                               pubmed_id=int(article_data['pubmed_id']),
                                               authors=str(article_data['authors']),
                                               title=str(article_data['title']))
            article_insert = article_check[0]
            article_present = article_check[1]
            if article_present == False:
                session.add(article_insert)
                session.commit()

        for stress in textmatch_data:
            if stress and stress['name'] is not None:
                stress_check = self.get_or_create(session=session, table_name='stress', name=str(stress['name']),
                                                  id=self.stress_id)

                stress_insert = stress_check[0]
                stress_present = stress_check[1]
                if stress_present == False:
                    session.add(stress_insert)
                    session.commit()
                    self.stress_id += 1

                    # textmatch_insert = self.get_or_create(table_name='textmatch', values={})
                    # session.add(textmatch_insert)

# k = SQLConnector()
# insertoo = k.insertion(table_name='organism', values={'taxonomy_id': 2,
#                                                       'name': 'hoi',
#                                                       'common_name': 'hallo'
#                                                       ,'organism_genus':k.insertion(table_name='organism_genus',values={'id':2,'name':'HELP'})})
# sessiono = k.get_session()
# sessiono.add(insertoo)
# sessiono.commit()
# print(insertoo.id)

# try:
#     ThingOne().go(session)
#     ThingTwo().go(session)
#
#     session.commit()
# except:
#     session.rollback()
#     raise
# finally:
#     session.close()

# inserto = k.insertion(table_name='gene',
#                       values={'gene_id': 9, 'name': "lol", 'sequence': "mkay", 'location': "space",
#                               'aliases': "bruh,duh",
#                               'description': "HELP I AM STUCK IN A DATABASE",
#                               'gene_category': k.insertion(table_name='gene_category',
#                                                            values={'id': 9, 'name': 'ricardo'})})
#
# sessiono = k.get_session()
# sessiono.add(inserto)
# sessiono.commit()
#
# q = sessiono.query(k.get_table_class('gene'))
# print(q)


# # Return list with table names
# def get_table_names(self):
#     """
#
#     :return:
#     """
#     return list(self.Base.metadata.tables)

# Return dictionary with table names as keys and column names as values
# def get_tables(self):
#     """
#
#     :return:
#     """
#     return self.Base.metadata.tables
#
# # Return the table object containing the information of the specified table
# def get_table(self, table_name):
#     """
#
#     :param table_name:
#     :return:
#     """
#     if table_name in self.Base.metadata.tables:
#         return self.Base.metadata.tables[table_name]
#     else:
#         raise TableNotFoundException("Specified table not found")
#
# def __execute(self, query):
#     """
#
#     :param query:
#     :return:
#     """
#     connection = self.engine.connect()
#     connection.execute(query)
#
# def insert_values(self, table_name, values, column_check=False):
#     """
#
#     :param table_name:
#     :param values:
#     :param column_check:
#     :return:
#     """
#     table_object = self.get_table(table_name)  # get table object belonging to the table_name
#
#     if column_check == True and len(values) != len(table_object.columns):
#         raise ColumnLengthMismatchException("Amount of columns does not match amount of values to be inserted")
#
#     else:
#         ins = table_object.insert().values(values)
#         self.__execute(ins)
#         return ins

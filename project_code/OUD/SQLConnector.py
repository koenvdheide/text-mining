from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


class TableNotFoundException(Exception):
    """
    This exception gets called if an invalid table name is specified for retrieval
    """
    pass


class SQLConnector:
    """
    This class facilitates all the inserting and selecting done with the database
    """
    genus_id = 0
    stress_id = 0
    category_id = 0
    match_id = 0

    def __init__(self, sqldialect="mysql", driver="mysqlconnector", username="root", password="usbw", host="localhost",
                 port="3307", database="motor"):
        """
        
        :param sqldialect: the specific SQL implementation that the database runs on(such as mysql)
        :param driver: the API to use to actually connect with the db
        :param username: name of the database user
        :param password: password of the user
        :param host: name/adress of the host
        :param port: port to connect through
        :param database: name of the database
        """
        engine_argument = sqldialect + "+" + driver + "://" + username + ":" + password + "@" + host + ":" + port + "/" + database
        self.engine = create_engine(engine_argument, echo=False)  # mogelijk text encoding nog toevoegen

        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)

    def text_select(self, table_name, columns, keyword_column, keyword):
        """
        creates a select statement
        :param table_name: name of table to select from
        :param columns: columns to be select for result
        :param keyword_column: columns to check 
        :param keyword: keyword to check columns against
        :return: list of all rows matching the select statement
        """

        sql = text('select ' + str(columns).strip('[]').replace('"',
                                                                '') + ' from ' + table_name + ' where ' + keyword_column + '=' + '"' + keyword + '"')
        result = self.engine.execute(sql)
        results = []
        for row in result:
            results.append(row)
        return results

    def get_tables_as_classes(self):
        """
        returns all of the tables from a reflected database
        :return: all tables present in the database as Table objects
        """
        return self.Base.classes

    def get_table_class(self, table_name):
        """
        returns a specific table from a reflected database
        :param table_name: the name of the table to retrieve
        :return: the specific table as a Table object
        """
        tables = self.get_tables_as_classes()
        if table_name in tables:
            return getattr(self.Base.classes, table_name)
        else:
            raise TableNotFoundException("Specified table not found")

    def get_session(self):
        """
        creates a new session for the current database
        :return: the Session object
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def insertion(self, table_name, values):
        """
        creates an insert statement from given table name and values
        :param table_name: table to insert values into
        :param values: values to be inserted
        :return: the insert statement to be committed 
        """
        table_class = self.get_table_class(table_name)
        return table_class(**values)

    # https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    def get_or_create(self, session, table_name, **kwargs):
        """
        checks if given values already exist in a table, if not an insert will be made for these new values
        :param session: current session
        :param table_name: table to check
        :param kwargs: values to check for
        :return: the instance and a True (if instance was present) or False (if instance is newly created)
        """

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

    # def strip_none(self):



    def insert_article(self, annotation_data):  # FIX DIT NOG DAMN

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
            if gene and gene['gene_id'] is not None and \
                            self.get_or_create(session=session, table_name='gene', gene_id=int(gene['gene_id']))[
                                1] is False:
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

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

    def __init__(self, sqldialect="mysql", driver="mysqlconnector", username="root", password="usbw", host="localhost",
                 port="3307", database="test"):
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
        self.engine = create_engine(engine_argument, echo=False)  # turn echo to see sql statements

        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)  # reflect needed to load the db that is already present
        self.meta = MetaData()

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

    def text_select_join(self, table_name, columns, keyword_column, keyword, second_table='article',
                         first_id='organism.taxonomy_id', second_id='article.Organism_taxonomy_id'):
        """
        create a select statement with an additional join
        :param table_name: name of table to select from
        :param columns: columns to be select for result
        :param keyword_column: columns to check 
        :param keyword: keyword to check columns against
        :param second_table: table to join with
        :param first_id: column (probably id) to join on from first table
        :param second_id: column (probably id) to join on from second table 
        :return: list of all rows matching the select statement
        """

        sql = text('select ' + str(columns).strip('[]').replace('"',
                                                                '') + ' from ' + table_name + ' join ' + second_table + ' on ' + first_id + '=' + second_id + ' where ' + keyword_column + '=' + '"' + keyword + '"')
        result = self.engine.execute(sql)
        results = []
        for row in result:
            results.append(row)
        return results

    def get_tables(self):
        """
        returns all of the tables from a reflected database
        :return: all tables present in the database as automapped Table classes
        """
        return self.Base.classes

    def get_table(self, table_name):
        """
        returns a specific table from a reflected database
        :param table_name: the name of the table to retrieve
        :return: the specific table as a automapped Table class
        """
        tables = self.get_tables()
        if table_name in tables:
            return getattr(self.Base.classes, table_name)  # append table_name to Base.classes
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
        table_class = self.get_table(table_name)
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

        table = self.get_table(table_name)
        instance = session.query(table).filter_by(**kwargs).first()
        if instance:  # instance exists in table
            return instance, True
        else:  # instance does not exist (yet)
            instance = table(**kwargs)
            return instance, False

    def create_id(self, session, table):
        """
        create a primary key id for tables that lack unique identifiers
        :param session: database session to query database with
        :param table_name: name of the table to create id for
        :return: the newly made primary key
        """
        last_row = session.query(table).order_by(table.id.desc()).first()

        if last_row:  # has a row been inserted?
            return last_row.id + 1
        else:  # return 0 if not
            return 0

    def check_entry_exists(self, table, table_column, entry):
        """
        Checks if a given entry is already present in a column
        :param table: table to check
        :param table_column: column in table to check
        :param entry: entry to check for in the column
        :return: entry if it exists, None if it does not
        """
        session = self.get_session()
        entry_present = session.query(table).filter(table_column == entry).first()

        if entry_present:
            return entry_present
        else:
            return None

    def insert_data(self, annotation_data):
        """
        inserts the specific data obtained from the text mining
        :param annotation_data: the data in dictionary form
        """
        Gene = self.get_table('gene')
        Ortholog = self.get_table('orthologs')
        Organism = self.get_table('organism')
        Genus = self.get_table('organism_genus')
        Article = self.get_table('article')
        Textmatch = self.get_table('textmatch')
        Stress = self.get_table('stress')

        session = self.get_session()

        # database lacks auto increment ids, these tables have no unique identifiers themselves and so need to get ids this way
        genus_id = self.create_id(session, Genus)
        stress_id = self.create_id(session, Stress)
        match_id = self.create_id(session, Textmatch)

        genes = []
        for gene_data in annotation_data['Gene']:
            if gene_data:  # entry exists?
                if gene_data['gene_id']:  # skip entries without gene id
                    gene = self.check_entry_exists(Gene, Gene.gene_id, gene_data['gene_id'])
                    if not gene:
                        gene = Gene(gene_id=int(gene_data['gene_id']), name=str(gene_data['name']),
                                    aliases=str(gene_data['aliasses']),
                                    description=str(gene_data['description']))
                    genes.append(gene) # build a list with genes per article to link with stress conditions
                   # session.merge(gene) #unneeded as ortholog will also insert the genes
                    if gene_data['Orthologs']:
                        for orthologs_data in gene_data.pop('Orthologs'):
                            if orthologs_data: # ortholog exists?
                                if orthologs_data['GeneID']: # skip entries without ortholog id
                                    ortholog = Ortholog(ortholog_id=int(orthologs_data['GeneID']),
                                                        description=str(orthologs_data['Title']),
                                                        gene=gene)
                                    session.merge(ortholog)

        authors = str(annotation_data['Article'].pop('authors'))  # get authors as string instead of list

        for organism_data in annotation_data['Organism']:
            if organism_data:  # entry exists?
                if organism_data['taxonomy_id']:  # skip entries without tax id
                    genus_name = organism_data.pop('genus') # genus is stored as part of the organism data
                    genus = self.check_entry_exists(Genus, Genus.name, genus_name)
                    if not genus:  # genus doesn't exist already
                        genus = Genus(id=genus_id, name=genus_name)

                    session.merge(genus) #technically unneeded (organism also inserts genus)
                    organism = Organism(**organism_data, organism_genus=genus)
                    article = Article(authors=authors, **annotation_data['Article'], organism=organism)

                    for condition in annotation_data['Condition']:

                        stress = self.check_entry_exists(Stress, Stress.name, condition['name'])
                        if not stress: #stress condition doesn't exist yet
                            stress = Stress(id=stress_id, name=condition['name'], gene_collection=genes)

                        textmatch = self.check_entry_exists(Textmatch, Textmatch.sentence, condition['sentence'])
                        if not textmatch: #text match not found before (somewhat unlikely)
                            textmatch = Textmatch(id=match_id, score=condition['score'], sentence=condition['sentence'],
                                                  article=article)

                        session.merge(textmatch)
                        session.merge(stress)

                    #session.merge(article)
                    session.commit()

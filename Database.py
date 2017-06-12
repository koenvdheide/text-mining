import mysql.connector
DB = 'project'
cnx = mysql.connector.connect(host="127.0.0.1", user="root", password="usbw", db = DB, port=3307)
cursor = cnx.cursor()


class Database:

    def __init__(self):
        self.add_organism = ("INSERT INTO organism (taxonomy_id, name, common_name, organism_genus) VALUES (%s, %s, %s, %s)")
        self.add_genus =  ("INSERT INTO organism_genus (id, name) VALUES (%d, %s)")


    def insert_annotation(self, anno_data):
        self.insert_table_data("article",anno_data)


    def insert_table_data(self,start_table, table_dict):
        constrains = self.get_references(start_table)
        if constrains:
            for constraint in constrains:
                table = constraint[3]
                self.insert_table_data(table,table_dict)
        else:
            self.insert_data(start_table,table_dict)


    def insert_data(self,table,table_dict):
        print('now insert in:' + str(table))



    def get_references(self, table):
        query = """SELECT 
              TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME
            FROM
              INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
              REFERENCED_TABLE_SCHEMA = 'project'
              """
        cursor.execute(query)
        refs = [ref for ref in cursor if ref[0] == table]
        if refs:
            print(refs)
            return refs
        else:
            return None


def main():
    anno = {'article': {'pubmed_id': '28586465', 'title': 'ROS Induces Anthocyanin Production Via Late Biosynthetic Genes and Anthocyanin Deficiency Confers the Hypersensitivity to ROS-generating Stresses in Arabidopsis.', 'authors': ['Xu Z', 'Mahmood K', 'Rothstein SJ']}, 'gene': [{'gene_id': '32980818', 'name': 'pap1', 'aliasses': 'CAGL0L07546g', 'description': 'hypothetical protein', 'location': 'L', 'Orthologs': [{'TaxName': 'Saccharomyces cerevisiae', 'TaxId': 4932, 'Symbol': 'CAD1', 'Title': 'CAD1', 'GeneID': 852033}, {'TaxName': 'Kluyveromyces lactis', 'TaxId': 28985, 'Symbol': 'KLLA0A01760g', 'Title': 'KLLA0A01760g', 'GeneID': 2896569}], 'Organism': {'taxonomy_id': None, 'name': '[Candida] glabrata', 'common_name': '', 'genus': '[Candida]'}}], 'organism': [{'taxonomy_id': '3702', 'name': 'Arabidopsis thaliana', 'common_name': 'thale cress', 'genus': 'Arabidopsis'}], 'condition': [{'name': 'different stress', 'sentence': 'However, the mechanism of ROS-induced anthocyanin accumulation and the role of anthocyanins in the response of Arabidopsis (Arabidopsis thaliana) to different stresses are largely unknown.', 'score': 0.5701219512195121}, {'name': 'ROS-generating stress', 'sentence': 'Ten Arabidopsis mutants covering the main anthocyanin regulatory and biosynthetic genes are systematically analyzed under ROS-generating stresses.', 'score': 0.49186991869918695}, {'name': 'ROS-generating stress', 'sentence': 'The anthocyanin-deficient mutants have more endogenous ROS and are more sensitive to ROS-generating stresses while having decreased antioxidant capacity.', 'score': 0.4857723577235772}, {'name': 'high-light stress', 'sentence': 'Gene expression analysis reveals that photosynthetic capacity is more impaired in anthocyanin-deficient mutants under high-light stress.', 'score': 0.5416666666666666}, {'name': 'ROS-generating stress', 'sentence': 'We conclude that ROS is an important source signal to induce anthocyanin accumulation by up-regulating late biosynthetic and the corresponding regulatory genes and, as a feed-back regulation, anthocyanins modulate the ROS level and the sensitivity to ROS-generating stresses in maintaining photosynthetic capacity.', 'score': 0.6300813008130081}]}
    db = Database()
    db.insert_annotation(anno)

main()
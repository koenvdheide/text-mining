from collections import defaultdict
import json


class JSONBuilder:
    """
    This class can be used to build a JSON file from a string in which every 
    leaf is separated by a specific delimiter. 
    This code was edited from: https://stackoverflow.com/questions/43757965/convert-csv-to-json-tree-structure
    """

    @staticmethod
    def __ctree():
        """ 
        This function makes a dynamic tree structure
        """
        return defaultdict(JSONBuilder.__ctree)

    @staticmethod
    def __build_leaf(name, leaf, depth=0):
        """
        This recursive function build the custom tree
        :param name: The name of the leaf that should be added.
        :param leaf: The leaf item that should be added.
        :param depth: the current leaf depth.
        :return: The current tree.
        """
        res = {"name": name}
        depth += 1

        # add children node if the leaf actually has any children
        if len(leaf.keys()) > 0:
            lst = [JSONBuilder.__build_leaf(k, v, depth) for k, v in leaf.items()]
            if depth >= 1:
                size = len([d for d in lst])
                for d in lst:
                    if size == 1:
                        d['size'] = 150 + 50 #scale for one value
                    if size == 2:
                        d['size'] = 150 + 40 # scale for two values
                    else:
                        d['size'] = 150  #>2 scale the same
            res["children"] = lst
        return res

    @staticmethod
    def convert_to_JSON(delimited_data, delimiter=";"):
        """
        This function builds a JSON tree based on string provided. 
        :param delimited_data: A string in which every leaf is separated by a specific delimiter.
        :param delimiter: The delimiter that separates the leafs.
        :return: A JSON tree. 
        """
        tree = JSONBuilder.__ctree()
        rows = [row.strip().split(delimiter) for row in delimited_data.split("\n")]
        for row in rows:
            if row:
                leaf = tree[row[0]]
                for cid in range(1, len(row)):
                    leaf = leaf[row[cid]]

        # building a custom tree structure
        res = []
        for name, leaf in tree.items():
            res.append(JSONBuilder.__build_leaf(name, leaf))

        return json.dumps(res)

def main():
    text = ""
    with open('output.txt') as f:
        for line in f:
            if "Homo" not in line and "Mus" not in line and "Saccharomyces" not in line and "Drosophila" not in line:
                spl_line = line.split(";")
                if len(spl_line) < 4 and len(spl_line[1]) <=20:
                    text += line
    json = JSONBuilder.convert_to_JSON(text)
    print(json)
main()
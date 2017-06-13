import collections


class StringConverter:
    """
    This Class can function as bridge between Entrez strings and regular strings.
    However python will interpret them both as Class: __str__ the Entrez strings 
    are fundamentally different and can therefore cause errors while inserting in a database.
    This code was rewritten for python 3 based and for str instead of unicode: https://stacko
    verflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
    """

    @staticmethod
    def convert(data):
        """
        This function converts a Class __str__ to a python Class __str__.
        The data input can be either a single string, a dictionary, a list
        or a nested structure of these. 
        :param data: A __str__ like data object.
        :return: A __str__ python object. 
        """
        if isinstance(data, str):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(StringConverter.convert, data.items()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(StringConverter.convert, data))
        else:
            return data

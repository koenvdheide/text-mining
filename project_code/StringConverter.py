import collections


class StringConverter:

    @staticmethod
    def convert(data):
        if isinstance(data, str):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(StringConverter.convert, data.items()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(StringConverter.convert, data))
        else:
            return data

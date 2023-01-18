class Commander(object):
    def __init__(self):
        self.__items = dict()

    # Add object to commander
    def add_object(self, object_code: str, object_item: any):
        self.__items[object_code] = object_item

    # Append text to object
    def append_text(self, object_code: str, text: str):
        self.__items[object_code].clear()
        self.__items[object_code].append(text)

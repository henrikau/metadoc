class MetaElement:
    """
    MetaElement - an individual element in the MetaDoc tree.

    This is a semi-abstract class (semi since we don' have the notion of
    abstract classes in python).
    """
    def __init__(self, name):
        self.attribs = None
        self.element = None
        self.name    = name

    def getName(self):
        """
        getName - return the name of the element
        """
        return self.name

    def getElement(self):
        """
        element is an xml.etree.Element with the values. It can be a hierarchy
        """
        if self.element:
            return self.element

    def addEntry(self):
        """
        addEntry: add an entry to the element, this is typically a sub-entry.

        At the MetaElement level, this will raise an error, so classes
        inheriting from MetaElement must override this method.
        """
        raise Exception("%s has not implemented addEntry, and function cannot be used!" % self.name)


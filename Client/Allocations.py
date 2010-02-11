from MetaElement import MetaElement
import xml.etree.ElementTree

class Allocations(MetaElement):
    """
    Allocations - the granted resources for a project.
    """
    def __init__(self):
        """
        init()
        """
        MetaElement.__init__(self, "allocations")
        self.element = xml.etree.ElementTree.Element(self.getName())
        self.legalClass = ["pri", "nonpri"]

    def addEntry(self, account_nmb, hours, all_class, period):
        """
        add an allocation-entry to the list of allocations.
        """
        if not all_class in self.legalClass:
            print "Illegal class \"%s\" for Allocations (%s). Use one of %s." % (all_class, account_nmb, self.legalClass)
            return
        entry = xml.etree.ElementTree.Element("all_entry",
                                              account_nmb=account_nmb,
                                              hours=hours,
                                              all_class=all_class,
                                              period=period)
        self.element.append(entry)



from abstract import MetaInput

class UpdateAllocations(MetaInput):
    """ Class that processes recieved allocations from server. """
    def process(self):
        """ Processes allocation data recieved from server.

        Customize this function.

        """
        for item in self.items:
            print item.attributes
            for a in item.sub_elements:
                print a.attributes

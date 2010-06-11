from abstract import MetaOutput
from software.entries import SoftwareEntry
#### Testing Purposes ####
import random
#### Testing Purposes end ####

class SiteSoftware(MetaOutput):
    def populate(self):
        """ Function to populate self.items with SoftwareEntry.

        Customize this function to fit to your site.

        """
        for i in xrange(5):
            self.items.append(SoftwareEntry('GCC', '%d.%d.%d' % (random.randint(0,10), random.randint(0,10), random.randint(0,10)), "GPLv2", "http://gcc.no"))

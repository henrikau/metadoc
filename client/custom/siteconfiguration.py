from abstract import MetaOutput
from configuration.entries import ConfigEntry
#### Testing Purposes ####
import random
#### Testing Purposes end ####

class SiteConfiguration(MetaOutput):
    def populate(self):
        """ Function to populate self.items with ConfigEntry.

        Customize this function to fit to your site.

        """
        a = [
                ('cores', 'count'), 
                ('nodes', 'count'),
                ('totalDisk', 'TB'),
                ('usedDisk', 'TB'),
                ('totalSwap', 'GB'),
                ('usedSwap', 'GB'),
                ('totalMemory', 'MB'),
                ('usedMemory', 'MB')
            ]
        for i in xrange(5):
            t = random.randint(0,len(a)-1)
            self.items.append(ConfigEntry(a[t][0], a[t][1], random.randint(0,1000)))

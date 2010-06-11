from datetime import datetime, timedelta

from abstract import MetaOutput
from events.entries import ResourceUpEntry, ResourceDownEntry
#### Testing Purposes ####
import random
#### Testing Purposes end ####

class SiteEvents(MetaOutput):
    def populate(self):
        """
        Function to populate self.items with ConfigItem
        """
        for i in xrange(5):
            t = random.randint(0,1)
            if t == 0:
                self.items.append(ResourceDownEntry('Testing purposes', datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), (datetime.now()+timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S"), 95.5))
            else:
                self.items.append(ResourceUpEntry(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), 'We are BACK!', 'We were down'))

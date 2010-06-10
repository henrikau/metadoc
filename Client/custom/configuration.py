"""
Custom
"""

from Abstract import MetaOutput
#### Testing Purposes ####
import random
#### Testing Purposes end ####

class ConfigItem:
    """
    Help class that defines a ConfigItem
    """
    def __init__(self, element, metric, volume):
        self.element = element
        self.metric = metric
        self.volume = volume
    def __str__(self):
        return "ConfigItem: %s (%d %s)" % (self.element, self.volume, self.metric)
    def todict(self):
        return {
            'element': self.element,
            'metric': self.metric,
            'volume': self.volume,
        }

class SiteConfiguration(MetaOutput):
    def populate(self):
        """
        Function to populate self.items with ConfigItem
        """
        for i in xrange(5):
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
            t = random.randint(0,len(a)-1)
            self.items.append(ConfigItem(a[t][0], a[t][1], random.randint(0,1000)))

import metaelement
import re
from custom.siteposts import SitePosts
from utils import UniqueID()

class PostEntry(metaelement.MetaElement):
    xml_tag_name = "post_entry"

    def __init__(self, title, author):
        unique_id = UniqueID()
        attributes = {
            'title': title,
            'author': author,
            'id': unique_id.get_id(),
        }
        super(PostEntry, self).__init__(PostEntry.xml_tag_name, attributes)
    def set_content(self, content):
        """ Sets the content of the post. """
        self.text = content
    def clean_author(self, author):
        """ Makes sure the author's name is in lower case. """
        return author.lower()

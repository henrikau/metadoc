import metaelement
from custom.siteposts import SitePosts
from posts.entries import PostEntry

class Posts(metaelement.MetaElement):
    xml_tag_name = "posts"
    site_handler = SitePosts
    url = "posts"

    def __init__(self):
        super(Posts, self).__init__(Posts.xml_tag_name)
        self.legal_element_types = (PostEntry,)

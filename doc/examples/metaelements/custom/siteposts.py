from custom.abstract import MetaOutput
from posts.entries import PostEntry

class SitePosts(MetaOutput):
    def populate(self):
        """ Adds a couple of posts that should be sent. """
        post_one = PostEntry(title="We're making progress!", author="bjornarg")
        post_one.set_content("""This text will be in post_entry MetaElement 
instance's self.text!""")
        self.items.append(post_one)
        post_two = PostEntry(title="Cleaning attributes" author="ProperAuthor")
        post_two = "We've made sure that author is sent in lower case."
        self.items.append(post_two)

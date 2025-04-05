class BlogPostVerificationError(Exception):
    """Custom exception for blog post verification errors."""
    pass

class BlogPost:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.verify_blog_post()
    

    def to_dictionary(self):
        return {
            'id': self.id,
            'title': self.title,
        }
    
    def verify_blog_post(self):
        if not isinstance(self.id, int):
            raise BlogPostVerificationError("BlogPost `id` must be an integer.")
        if not isinstance(self.title, str) or not self.title.strip():
            raise BlogPostVerificationError("BlogPost `title` must be a non-empty string.")

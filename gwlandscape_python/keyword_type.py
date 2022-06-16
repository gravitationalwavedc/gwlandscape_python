class Keyword:
    def __init__(self, keyword_data):
        self.tag = keyword_data['tag']
        self.id = keyword_data['id']

    def __repr__(self):
        return f"Keyword '{self.tag}'"

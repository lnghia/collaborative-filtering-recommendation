class Post:
    def __init__(self, id, title, thumbnail, rating, content, createdAt, updatedAt, author, angry, like, yummy):
        self.id = id
        self.title = title
        self.thumbnail = thumbnail
        self.rating = rating
        self.content = content
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.author = author
        self.angry = angry
        self.like = like
        self.yummy = yummy

    def __str__(self):
        return self.id
    
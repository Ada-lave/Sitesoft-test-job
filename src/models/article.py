class ArticleInfo:
    def __init__(
        self,
        heading: str,
        publish_date: str,
        link: str,
        author_name: str,
        link_to_author: str,
    ) -> None:
        self.heading = heading
        self.publish_date = publish_date
        self.link = link
        self.author_name = author_name
        self.link_to_author = link_to_author

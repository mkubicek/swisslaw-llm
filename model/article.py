from dataclasses import dataclass

@dataclass
class Article:
    article_number: str

    def __str__(self):
        return f"{self.article_number}"

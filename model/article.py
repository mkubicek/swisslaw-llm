from dataclasses import dataclass

@dataclass
class Article:
    article_number: str
    paragraphs: list
    context: list
    
    def __str__(self):
        return f"{self.article_number}"

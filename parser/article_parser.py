import re
from model.article import Article
import xml.etree.ElementTree as ET

def _get_paragraphs(article):
    paragraphs = []
    for paragraph in article.findall('.//akn:paragraph', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}):
        # Check for regular paragraph content
        p_content = paragraph.find('.//akn:content/akn:p', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'})
        if p_content is not None:
            paragraphs.append(''.join(p_content.itertext()).strip().replace('\xa0', ' '))
        # Check for blockList content
        block_list = paragraph.find('.//akn:content/akn:blockList', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'})
        if block_list is not None:
            block_paragraph = []
            for item in block_list.findall('.//akn:item', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}):
                item_text = ''.join(item.itertext()).strip().replace('\xa0', ' ')
                block_paragraph.append(item_text)
            paragraphs.append(' '.join(block_paragraph))
    # If no paragraphs are found, add the authorialNote since the article has been annulled
    if not paragraphs:
        note = article.find('.//akn:authorialNote', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'})
        if note is not None:
            note_content = ''.join(note.itertext()).strip().replace('\xa0', ' ')
            paragraphs.append(note_content)
    return paragraphs

def parse_articles(xml_content):
    root = ET.fromstring(xml_content)
    ET.register_namespace('akn', 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0')
    articles = []

    body = root.find('.//akn:body', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'})
    if body is not None:
        for article in body.findall('.//akn:article', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}):
            article_num_raw = ''.join(article.find('.//akn:num', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}).itertext()).strip().replace('\xa0', ' ')
            article_num = re.search(r'\d+[a-z]*', article_num_raw).group()
            if article_num:
                articles.append(Article(article_number=article_num, paragraphs=_get_paragraphs(article)))
                        
    return articles


if __name__ == '__main__':
    with open('raw/fedlex-data-admin-ch-eli-cc-1999-404-20240101-de-xml-14.xml', 'r') as file:
        xml_data = file.read()
    articles = parse_articles(xml_data)
    
    print(len(articles))
    #for article in articles:
    #    print(article)

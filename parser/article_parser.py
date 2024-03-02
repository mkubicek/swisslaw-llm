import re
import xml.etree.ElementTree as ET
from model.article import Article

NS = {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}

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
            block_paragraph = [' '.join(item.itertext()).strip() for item in block_list.findall('.//akn:item', NS)]
            paragraphs.append(' '.join(block_paragraph))
    # If no paragraphs are found, add the authorialNote since the article has been annulled
    if not paragraphs:
        note = article.find('.//akn:authorialNote', NS)
        if note is not None:
            paragraphs.append(' '.join(note.itertext()).strip())

    return paragraphs

def _get_context(article, parent_map):
    context = []
    current = parent_map.get(article)
    while current is not None and current.tag != 'akn:body' and current.tag is not ET.Comment:
        num = current.find('.//akn:num', NS)
        heading = current.find('.//akn:heading', NS)
        if num is not None:
            context.append(' '.join(num.itertext()).strip())
        elif heading is not None:
            context.append(' '.join(heading.itertext()).strip())
        current = parent_map.get(current)

    return context[::-1]

def parse_articles(xml_content):
    root = ET.fromstring(xml_content)
    ET.register_namespace('akn', NS['akn'])
    articles = []

    # Create the parent map only once
    parent_map = {child: parent for parent in root.iter() for child in parent}

    for article in root.findall('.//akn:body//akn:article', NS):
        article_num_raw = ' '.join(article.find('.//akn:num', NS).itertext()).strip()
        article_num = re.search(r'\d+[a-z]*', article_num_raw).group()
        if article_num:
            articles.append(Article(article_number=article_num, paragraphs=_get_paragraphs(article), context=_get_context(article, parent_map)))

    return articles

if __name__ == '__main__':
    with open('your_xml_file_path.xml', 'r') as file:
        xml_data = file.read()
    articles = parse_articles(xml_data)
    
    print(len(articles))
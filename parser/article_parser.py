from model.article import Article
import xml.etree.ElementTree as ET

def parse_articles(xml_content):
    root = ET.fromstring(xml_content)
    ET.register_namespace('akn', 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0')
    articles = []

    body = root.find('.//akn:body', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'})
    if body is not None:
        for article in body.findall('.//akn:article', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}):
            article_num = ''.join(article.find('.//akn:num', {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}).itertext()).strip()
            if article_num:
                articles.append(Article(article_number=article_num))
    return articles

if __name__ == '__main__':
    with open('raw/fedlex-data-admin-ch-eli-cc-1999-404-20240101-de-xml-14.xml', 'r') as file:
        xml_data = file.read()
    articles = parse_articles(xml_data)
    
    print(len(articles))
    #for article in articles:
    #    print(article)

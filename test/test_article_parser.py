import unittest
from law_repo.law_repo import LawRepo
from parser.article_parser import parse_articles

class TestArticleParser(unittest.TestCase):
    def test_or_article_count(self):
        xml_data = LawRepo.get_xml("OR")
        articles = parse_articles(xml_data)
        self.assertEqual(len(articles), 1600, "The number of articles in OR should be 1600.")
        
    def test_zgb_article_count(self):
        xml_data = LawRepo.get_xml("ZGB")
        articles = parse_articles(xml_data)
        self.assertEqual(len(articles), 472, "The number of articles in ZGB should be 472.")

    def test_bv_article_count(self):
        xml_data = LawRepo.get_xml("BV")
        articles = parse_articles(xml_data)
        self.assertEqual(len(articles), 232, "The number of articles in BV should be 232.")
        
if __name__ == '__main__':
    unittest.main()
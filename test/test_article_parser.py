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
        
    def test_article_num_contains_only_digits_and_optional_letter(self):
        for law in LawRepo.laws:
            xml_data = LawRepo.get_xml(law)
            articles = parse_articles(xml_data)
            for article in articles:
                self.assertRegex(article.article_number, r'^\d+[a-z]*$', f"Article number {article.article_number} in {law} does not match the expected pattern.")
    
    def test_article_contains_paragraphs(self):
        for law in LawRepo.laws:
            xml_data = LawRepo.get_xml(law)
            articles = parse_articles(xml_data)
            for article in articles:
                self.assertTrue(len(article.paragraphs) > 0, f"Article {article.article_number} in {law} does not contain any paragraphs.")
        
if __name__ == '__main__':
    unittest.main()
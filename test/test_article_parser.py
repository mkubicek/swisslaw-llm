import unittest
from law_repo.law_repo import LawRepo
from parser.article_parser import parse_articles
import re

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
                
    def test_or_parse_article_1_paragraphs(self):
        # read assets/OR_Art1.xml and parse it
        with open('test/assets/OR_Art1.xml', 'r') as file:
            xml_data = file.read()
        articles = parse_articles(xml_data)
        self.assertTrue(len(articles[0].paragraphs) == 2, "Article 1 in OR should contain 2 paragraph.")
        self.assertTrue(len(articles[0].article_number) == 1, "Article 1 in OR should have the number 1.")
        
        article_1_paragraphs = ['Zum Abschlusse eines Vertrages ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich.', 'Sie kann eine ausdrückliche oder stillschweigende sein.']
        self.assertEqual(articles[0].paragraphs, article_1_paragraphs, "Article 1 in OR does not contain the expected paragraphs.")

    def test_or_parse_article_1_context(self):
        # read assets/OR_Art1.xml and parse it
        with open('test/assets/OR_Art1.xml', 'r') as file:
            xml_data = file.read()
        articles = parse_articles(xml_data)
        
        article_1_context = ['Erste Abteilung: Allgemeine Bestimmungen', 
                             'Erster Titel: Die Entstehung der Obligationen',
                             'Erster Abschnitt: Die Entstehung durch Vertrag',
                             'A. Abschluss des Vertrages',
                             'I. Übereinstimmende Willensäusserung',
                             '1. Im Allgemeinen']
        self.assertEqual(articles[0].context, article_1_context, "Article 1 in OR does not contain the expected context.")

if __name__ == '__main__':
    unittest.main()
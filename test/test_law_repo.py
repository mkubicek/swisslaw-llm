import unittest
from unittest.mock import patch, mock_open
from law_repo.law_repo import LawRepo

class TestLawRepo(unittest.TestCase):
    def test_get_or(self):
        xml_content = LawRepo.get_xml("OR")


if __name__ == '__main__':
    unittest.main()
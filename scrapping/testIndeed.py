import os
import unittest
from bs4 import BeautifulSoup

from scrapping_indeed import Indeed

class Test(unittest.TestCase):

    def test__init__(self):

        testClass = Indeed()      
        
        
        #self.assertTrue(isinstance(testClass.results, bs4.element.Tag))
        self.assertTrue(testClass.results != '')
        self.assertTrue(len(testClass.a_links)> 1)
        
        #self.assertTrue(os.path.exists('./stop_areas_maria.json'))

    """ continuer avec les test
    """

if __name__  == '__main__':
    unittest.main(verbosity =2)

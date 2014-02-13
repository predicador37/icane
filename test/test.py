# -*- coding: utf-8 -*-
import sys
sys.path.append('../icane')
import unittest
import metadata
import logging
import urllib2


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestIcaneMetadata(unittest.TestCase):


   def setUp(self):
        pass
        
   def test_category(self):
       
        self.assertRaises(ValueError, metadata.Category,'not a json object')
        self.assertTrue(metadata.Category(metadata.request('category/historical-data')).title=='Datos históricos')
   
   def test_get_category(self):
       
       self.assertRaises(urllib2.HTTPError, metadata.Category.get,'regioal-data')
       self.assertTrue(metadata.Category.get('regional-data').title=='Datos regionales')       
       
       self.assertRaises(urllib2.HTTPError, metadata.Category.get,89)
       self.assertTrue(metadata.Category.get(1).title=='Datos regionales')
     
   def test_get_categories(self):
       
       categories = metadata.Category.find_all()
       self.assertTrue(len(categories) == 4)
       self.assertTrue(categories.index(metadata.Category.get('municipal-data')))
       
   def test_section(self):
       
        self.assertRaises(ValueError, metadata.Section,'not a json object')
        self.assertTrue(metadata.Section(metadata.request('section/society')).title=='Sociedad')
   
   def test_get_section(self):
       
       self.assertRaises(urllib2.HTTPError, metadata.Section.get,'economia')
       self.assertTrue(metadata.Section.get('economy').title=='Economía')       
       
       self.assertRaises(urllib2.HTTPError, metadata.Section.get,89)
       self.assertTrue(metadata.Section.get(4).title=='Territorio y Medio ambiente')
     
   def test_get_sections(self):
       
       sections = metadata.Section.find_all()
       self.assertTrue(len(sections) == 5)
       self.assertTrue(sections.index(metadata.Section.get('synthesis'))) 
       
if __name__ == '__main__':
    unittest.main()


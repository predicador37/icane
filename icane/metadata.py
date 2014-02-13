# -*- coding: utf-8 -*-
import urllib2
import json
import logging
import httplib
import inspect 

BASE_URL = 'http://www.icane.es/metadata/api/'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def request(path):
            '''Utility function that calls urllib2 with BASE_URL + path and accepting json format'''
            request = urllib2.Request(BASE_URL + path, headers={"Accept" : "application/json"})
            f=None
            try: 
                f = urllib2.urlopen(request)
            except urllib2.HTTPError, e:
                logger.error((inspect.stack()[0][3]) + ': HTTPError = ' + str(e.code) + ' ' + str(e.reason) + ' ' + str(e.geturl()))
                raise
            except urllib2.URLError, e:
                logger.error('URLError = ' + str(e.reason)+ ' ' + str(e.geturl()))
                raise
            except httplib.HTTPException, e:
                logger.error('HTTPException')
                raise
            except Exception:
                import traceback
                logger.error('Generic exception: ' + traceback.format_exc())
                raise
            else:
                response = json.loads(f.read())
                f.close()
                return response                 

class JSONDecoder(dict):
    '''Utility function that decodes JSON into a python object'''
    def __init__(self, dict_):
        super(JSONDecoder, self).__init__(dict_)
        for key in self:
            item = self[key]
            if isinstance(item, list):
                for id, it in enumerate(item):
                    if isinstance(it, dict):
                        item[id] = self.__class__(it)
            elif isinstance(item, dict):
                self[key] = self.__class__(item)

    def __getattr__(self, key):
        return self[key]

class Category(JSONDecoder):
    
    label_='category'
        
    def __init__(self, dict_):
        
        super(self.__class__, self).__init__(dict_)
   
    '''

      Retrieve a category by its uriTag.
      @param uriTag the uriTag of the Category
      @return
     
    '''
    
    @classmethod 
    def get(cls,uriTag):
        return Category(request(cls.label_ + '/' + str(uriTag)))
    
    '''
    
      Retrieves all available categories
      @return a list of categories
    
    '''
       
    @classmethod    
    def find_all(cls):
        categories=[]
       
        for category in request('categories'):
                categories.append(JSONDecoder(category))    
        return categories
       
class Section(JSONDecoder):
    
    label_='section'
        
    def __init__(self, dict_):
        
        super(self.__class__, self).__init__(dict_)
   
    '''

      Retrieve a Section by its uriTag.
      @param uriTag the uriTag of the Section
      @return
     
    '''
    
    @classmethod 
    def get(cls,uriTag):
        return Section(request(cls.label_ + '/' + str(uriTag)))
    
    '''
    
      Retrieves all available categories
      @return a list of categories
    
    '''
       
    @classmethod    
    def find_all(cls):
        sections=[]
       
        for section in request('sections'):
                sections.append(JSONDecoder(section))    
        return sections




class Time_series(object):
    
    def __init__(self):
        pass
    
    def find_all_by_category(self, category_uri_tag):
        time_series_list = []
        time_series_array = self.request(category_uri_tag + '/time-series-list')
        for time_series in time_series_array:
            time_series_list.append(JSONDecoder(time_series))
        return time_series_list
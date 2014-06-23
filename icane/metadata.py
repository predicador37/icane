# -*- coding: utf-8 -*-
import urllib2
import json
import logging
import httplib
import inspect
import datetime
import pandas as pd

BASE_URL = 'http://www.icane.es/metadata/api/'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def request(path):

   """Sends a request to a given URL accepting JSON, and returns a JSON object.
      If no "http://" protocol is specified, BASE_URL is used in the request.

   Args:
     path (str): The URI to be requested.

   Returns:
     response: Deserialized JSON object.

   Raises:
     HTTPError: the HTTP error returned by the requested server.
     URLError: the handlers of urllib2 this exception (or derived exceptions).
     when they run into a problem.
     HTTPException: generic http exception.
     Exception: generic exception.

   """
   if (path.startswith("http://")):
       request = urllib2.Request(path,
                             headers={"Accept": "application/json"})
   else:
       request = urllib2.Request(BASE_URL + path,
                             headers={"Accept": "application/json"})
   f = None
   try:
       f = urllib2.urlopen(request)
   except urllib2.HTTPError, e:
       logger.error((inspect.stack()[0][3]) +
                    ': HTTPError = ' + str(e.code) +
                    ' ' + str(e.reason) +
                    ' ' + str(e.geturl()))
       raise
   except urllib2.URLError, e:
       logger.error('URLError = ' + str(e.reason) +
                    ' ' + str(e.geturl()))
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

def flatten(data, record=None):

    """Flattens a nested dict generated from a deserialized JSON object .

    Args:
      data (dict): a dictionary generated by ''request()'' function.
      record (list , optional): Defaults to None.
      
    Yields:
      row: A list representing a row in a flattened matrix.
      
    #TODO: 
    Examples:
      Examples should be written in doctest format, and should illustrate how
      to use the function.

      >>> print [i for i in example_generator(4)]
      [0, 1, 2, 3]

    """
    
    if data.get('data'):#first level
        record = []
        row = []
        for j in sorted(list(flatten(data['data'], record))):
            yield j
    else: #other levels
        for idx, k in enumerate(sorted(list(data))):
            if isinstance(data[k],dict):      
                record.append(k)
                try:
                
                    for i in sorted(list(flatten(data[k], record))):
                        if len(record) == 1:
                            record.pop()
                        yield i
                except:
                    pass
            else: #last level
               row = list(record)
               row.append(k)
               row.append(data[k])
               yield row
        if record:
            record.pop()

def add_query_string_params(nodeType = None, inactive = None):
        arguments = locals()
        query_string =''
        for argument, value in arguments.iteritems():
            if value is not None:           
                query_string = query_string + '?' + str(argument) + '=' +\
                               str(value)     
        return query_string

def add_path_params(section_uri_tag = None, subsection_uri_tag = None,
                    data_set_uri_tag = None):
        # arguments order must be preserved, I can't find a better way of 
        # doing this, since it is not an OrderedDict.
        arguments = locals()
        values = []
        ordered_arg_names = ['section_uri_tag', 'subsection_uri_tag', 
                     'data_set_uri_tag']
       
        for name in ordered_arg_names:
            values.append(arguments[name])
        path=''
        for value in values:
            if value is not None:
                path = path + '/' + str(value)
        return path

class RawObject(dict):

    """Class to convert deserialized JSON into a Python object
      
    """

    label_ = None
    plabel_ = None

    def __init__(self, dict_):
        
        """Decodes JSON to a Python object
           by http://peedlecode.com/posts/python-json/

        Args:
          dict_ (dict): dictionary that results from deserialized JSON object.

        """
        
        super(RawObject, self).__init__(dict_)
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
        
    def to_json(self):
        return json.dumps(self)


class BaseEntity(RawObject):
    
    def __init__(self, dict_):

        super(BaseEntity, self).__init__(dict_)
    '''
     Retrieve an entity by its uriTag.
     @param uriTag the uriTag of the entity
     @return

    '''

    @classmethod
    def get(cls, uriTag):
        return cls(request(cls.label_ + '/' + str(uriTag)))

    '''

      Retrieves all available entities
      @return a list of entities

    '''

    @classmethod
    def find_all(cls):
        entities = []
        for entity in request(cls.plabel_):
                entities.append(cls(entity))
        return entities

class DataEntity(RawObject):
    
    def __init__(self, dict_):

        super(self.__class__, self).__init__(dict_)
     
    @classmethod
    def get_last_updated(cls):    
        return datetime.datetime.fromtimestamp(
               int(str((request( str(cls.label_)
               + '/' + 'last-updated')))[0:-3])).strftime('%d/%m/%Y')
                
    @classmethod
    def get_last_updated_millis(cls):
        return int(str((request( str(cls.label_)
                + '/' + 'last-updated'))))

class Category(BaseEntity):
        
    label_ = 'category'
    plabel_ = 'categories'


class Class(BaseEntity):

    label_ = 'class'
    plabel_ = 'classes'
    
        
    '''

     Retrieve an entity by its uriTag.
     @param uriTag the uriTag of the entity
     @return

    '''

    @classmethod
    def get(cls, class_name, lang):
        return cls(request(cls.label_ +
                           '/' + str(class_name) +
                           '/' + 'description' + '/' + lang))
   
    '''

      Retrieves all available entities
      @return a list of entities

    '''

    @classmethod
    def find_all(cls,lang):
        entities = []
        response = request(cls.plabel_ + '/' + 'description' + '/' + lang)
        for entity in response[cls.plabel_]:
                entities.append(cls(entity))
        return entities

class Data(DataEntity):
    
     label_ = 'data'
     

class DataProvider(BaseEntity):

    label_ = 'data-provider'
    plabel_ = 'data-providers'


class DataSet(BaseEntity):

    label_ = 'data-set'
    plabel_ = 'data-sets'


class Link(BaseEntity):

    label_ = 'link'
    plabel_ = 'links'


class LinkType(BaseEntity):

    label_ = 'link-type'
    plabel_ = 'link-types'


class Measure(BaseEntity):

    label_ = 'measure'
    plabel_ = 'measures'


class Metadata(DataEntity):
    
     label_ = 'metadata'


class NodeType(BaseEntity):

    label_ = 'node-type'
    plabel_ = 'node-types'


class Periodicity(BaseEntity):

    label_ = 'periodicity'
    plabel_ = 'periodicities'


class ReferenceArea(BaseEntity):

    label_ = 'reference-area'
    plabel_ = 'reference-areas'


class Section(BaseEntity):

    label_ = 'section'
    plabel_ = 'sections'

    @classmethod
    def get_subsections(cls, uriTag):
        subsections = []
        subsection_array = request(cls.label_ +
                            '/' + str(uriTag) +
                            '/' + 'subsections')
        for subsection in subsection_array:
            subsections.append(Subsection(subsection))
        return subsections 
    
    @classmethod
    def get_subsection_by_section_and_uri_tag(cls, section_uri_tag, 
                                              subsection_uri_tag):
        return cls(request('section' +
                     '/'+ section_uri_tag +
                     '/' + subsection_uri_tag))

class Source(BaseEntity):

    label_ = 'source'
    plabel_ = 'sources'


class Subsection(BaseEntity):

    label_ = 'subsection'
    plabel_ = 'subsections'

class TimePeriod(BaseEntity):

    label_ = 'time-period'
    plabel_ = 'time-periods'


class TimeSeries(BaseEntity):

    label_ = 'time-series'
    plabel_ = 'time-series-list'

    @classmethod
    def get(cls, uriTag, inactive=None):
        return cls(request(cls.label_ + '/' + str(uriTag) + 
                    add_query_string_params(inactive = inactive)))

    def to_dataframe(self):
        resource = request(self.apiUris[3].uri) #third element is icane json
        df = pd.DataFrame(list(flatten(resource)))
        headers = list(resource['headers'])
        headers.append(unicode('Valor'))
        df.columns = headers
        if (self.category.id == 3):
            ts = df.set_index([unicode(headers[0])]) #TODO: check indexes pos
        else:
            ts = df.set_index([unicode(headers[len(headers)-2])])
        return ts

    #def get_data(self):
    #    return request(self.apiUris[3].uri)

    '''

    Retrieve an entity by its uriTag.
    @param uriTag the uriTag of the entity
    @return

    '''

    @classmethod
    def get_parent(cls, uriTag):
        return cls(request(cls.label_ + '/' + str(uriTag) + '/' + 'parent'))
        
    @classmethod
    def get_parents(cls, uriTag):
        parents = []
        parents_array = request(cls.label_ +
                            '/' + str(uriTag) +
                            '/' + 'parents')
        for ancestor in parents_array:
            parents.append(TimeSeries(ancestor))
        return parents
    
    '''

    Retrieve possible subsections associated to TimeSeries uriTag.
    @param uriTag the uriTag of the TimeSeries entity
    @return List of Subsection entities

    '''
    
    @classmethod
    def get_possible_subsections(cls, uriTag):
        subsections = []
        subsections_array = request(cls.label_ +
                                    '/' + str(uriTag) +
                                    '/' + 'subsections')
        for subsection in subsections_array:
            subsections.append(Subsection(subsection))
        return subsections
    
    '''

    Retrieve possible time-series associated to TimeSeries uriTag.
    @param uriTag the uriTag of the TimeSeries entity
    @return List of TimeSeries entities

    '''
    
    @classmethod
    def get_possible_time_series(cls, uriTag):
        time_series_list = []
        time_series_array = request(cls.plabel_ +
                                    '/' + str(uriTag))
        for time_series in time_series_array:
            time_series_list.append(TimeSeries(time_series))
        return time_series_list

    @classmethod
    def find_all_datasets(cls,
                          category_uri_tag,
                          section_uri_tag,
                          subsection_uri_tag):
        time_series_list = []
        time_series_array = request(category_uri_tag + '/' +
                                    section_uri_tag + '/' +
                                    subsection_uri_tag + '/' +
                                    'data-sets')
        for time_series in time_series_array:
            time_series_list.append(TimeSeries(time_series))
        return time_series_list
        
    @classmethod
    def find_all_by_last_updated(cls,
                          dataUpdated=None,
                          metadataUpdated=None):
        time_series_list = []
        if (dataUpdated):
            time_series_array = request(cls.plabel_ + '?dataUpdated=' +
                                        dataUpdated)
        elif (metadataUpdated):
            time_series_array = request(cls.plabel_ + '?dataUpdated=' +
                                        metadataUpdated)    
        for time_series in time_series_array:
            time_series_list.append(TimeSeries(time_series))
        return time_series_list

    @classmethod
    def find_all(cls, category_uri_tag,
                      section_uri_tag = None,
                      subsection_uri_tag = None,
                      data_set_uri_tag = None,
                      node_type_uri_tag = None,
                      inactive = None):
        
        time_series_list = []
        http_request =  category_uri_tag + add_path_params(
                        section_uri_tag, subsection_uri_tag, data_set_uri_tag)\
                        + '/time-series-list' +\
                        add_query_string_params(node_type_uri_tag, inactive)
        time_series_array = request(http_request)
        for time_series in time_series_array:
            time_series_list.append(TimeSeries(time_series))
        return time_series_list

class UnitOfMeasure(BaseEntity):

    label_ = 'unit-of-measure'
    plabel_ = 'units-of-measure'

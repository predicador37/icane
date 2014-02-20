# -*- coding: utf-8 -*-
import urllib2
import json
import logging
import httplib
import inspect
import datetime

BASE_URL = 'http://www.icane.es/metadata/api/'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def request(path):
            '''Utility function that calls urllib2 with BASE_URL
            + path and accepting json format'''
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


class JSONDecoder(dict):
    '''Utility function that decodes JSON into a python object'''

    label_ = None
    plabel_ = None

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


class BaseEntity(JSONDecoder):
    
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

class DataEntity(JSONDecoder):
    
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
        for entity in request(cls.plabel_ + '/' + 'description' + '/' + lang):
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
            parents.append(BaseEntity(ancestor))
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
                      node_type_uri_tag = None):
        
        time_series_list = []
        
        if (section_uri_tag and
            subsection_uri_tag and
            data_set_uri_tag):
            time_series_array = request(category_uri_tag + '/' +
                                        section_uri_tag + '/' +
                                        subsection_uri_tag + '/' +
                                        data_set_uri_tag + '/' +
                                        cls.plabel_)
        elif (section_uri_tag and
              subsection_uri_tag):
              time_series_array = request(category_uri_tag + '/' +
                                          section_uri_tag + '/' +
                                          subsection_uri_tag + '/' +
                                          cls.plabel_)
        elif (section_uri_tag and
              node_type_uri_tag):
              time_series_array = request(category_uri_tag + '/' +
                                        section_uri_tag + '/' +
                                        cls.plabel_ + '?nodeType=' +
                                        node_type_uri_tag)
        elif (section_uri_tag):
            time_series_array = request(category_uri_tag + '/' +
                                        section_uri_tag + '/' +
                                        cls.plabel_)
        else:
            time_series_array = request(category_uri_tag + '/' +
                                         cls.plabel_)     
        for time_series in time_series_array:
            time_series_list.append(TimeSeries(time_series))
        return time_series_list


class UnitOfMeasure(BaseEntity):

    label_ = 'unit-of-measure'
    plabel_ = 'units-of-measure'

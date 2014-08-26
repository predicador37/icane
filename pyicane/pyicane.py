# -*- coding: utf-8 -*-
"""pyicane-metadata is a Python wrapper for the Statistical Office of \
Cantabria's (ICANE) metadata restful API. This module parses ICANE's json \
data and metadata into Python objects and common data structures such as \
Pandas dataframes [1]_. All ICANE's API classes and methods are covered; \ 
also, time-series data can be downloaded into a Python Pandas dataframe \
structure. 

pyicane-metadata is written and maintained by `Miguel Expósito Martín \
<https://twitter.com/predicador37>`_ and is distributed under the Apache 2.0 \
License (see LICENSE file).

.. [1] http://pandas.pydata.org for Python Data Analysis Library information  
"""

import requests
import logging
import inspect
import datetime
import pandas as pd
import abc

BASE_URL = 'http://www.icane.es/metadata/api/'
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def request(path):
    """Send a request to a given URL accepting JSON format and return a JSON \ 
       converted Python object. If no "http://" protocol is specified, \
       BASE_URL is used in the request.

    Args:
      path (str): The URI to be requested.

    Returns:
      response: Deserialized JSON Python object.

    Raises:
      HTTPError: the HTTP error returned by the requested server.
      URLError: the handlers of urllib2 this exception (or derived exceptions).
      when they run into a problem.
      HTTPException: generic http exception.
      Exception: generic exception.

    """
    headers = {'Accept': 'application/json'}
    try:
        if (path.startswith("http://")):
            requested_object = requests.get(path, headers=headers)
        else:
            requested_object = requests.get(BASE_URL + path, headers=headers)
        requested_object.raise_for_status()
    except requests.exceptions.HTTPError, exception:
        LOGGER.error((inspect.stack()[0][3]) +
                               ': HTTPError = ' +
                               str(exception.response.status_code) +
                               ' ' + str(exception.response.reason) +
                               ' ' + str(path))
        raise
    except requests.exceptions.InvalidURL, exception:
        LOGGER.error('URLError = ' + str(exception.reason) +
                              ' ' + str(path))
        raise
    except Exception:
        import traceback
        LOGGER.error('Generic exception: ' + traceback.format_exc())
        raise
    else:
        response = requested_object.json()
        return response

def node_digest_model(node):
    """Extracts plain relevant metadata fields only.

    Args:
      node(dict): a dictionary generated by the ''request()'' function \
                  containing nested TimeSeries objects.
    Returns:
      List of relevant time-series metadata fields with the intention of \
      using them to populate a CSV row. 

    """

    if node.dataUpdate is None:
        data_update = '0000'
    else:
        data_update = node.dataUpdate
    if node.dataSet is None:
        dataset_title = ''
    else:
        dataset_title = node.dataSet.title
    if node.periodicity is None:
        periodicity_title = ''
    else:
        periodicity_title = node.periodicity.title
    if node.referenceArea is None:
        reference_area_title = ''
    else:
        reference_area_title = node.referenceArea.title
    if len(node.sources) == 0:
        sources_label = ''
    else:
        sources_label = node.sources[0].label
    
    return [node.id, node.title, node.active, node.uri, 
                   node.metadataUri, node.resourceUri, 
                   node.documentation, node.methodology, 
                   node.mapScope, node.referenceResources, 
                   node.description, node.theme, node.language, 
                   node.publisher, node.license, node.topics, 
                   node.automatizedTopics, node.uriTag, node.uriTagEs,
                   node.initialPeriodDescription, 
                   node.finalPeriodDescription, 
                   datetime.datetime.fromtimestamp(
                   int(str(data_update)[0:-3])).strftime('%d/%m/%Y'),
                   datetime.datetime.fromtimestamp(
                   int(str(node.dateCreated)[0:-3])).strftime('%d/%m/%Y'),
                   datetime.datetime.fromtimestamp(
                   int(str(node.lastUpdated)[0:-3])).strftime('%d/%m/%Y'),
                   node.subsection.title,
                   node.subsection.section.title,
                   node.category.title, dataset_title,
                   periodicity_title, node.nodeType.title,
                   reference_area_title, sources_label,
                   str(', '.join([': '.join((x.title, x.unit)) for x in 
                   node.measures])), 
                   str([', '.join((x.uri,'')) for x in node.apiUris])]

def flatten_metadata(data):
    """Flatten a nested dict or list of nested dicts generated from a \
       deserialized JSON object provided by ICANE's Restful metadata API.

    Args:
      data (dict): a dictionary or list of dictionaries containing nested \
                   TimeSeries objects.
    Yields:
      Python List of node_digest_model elements: A list with the most \
                                                 relevant metadata for a \
                                                 given node or list of nodes \
                                                 and their children in a \
                                                 flattened format.
    """
    if isinstance(data, list):
        for node in data:    
            if node.nodeType.uriTag in ['time-series',
                                        'non-olap-native',
                                        'document']: #leaf node
                yield node_digest_model(node)

            else:
                yield node_digest_model(node)
                for child in flatten_metadata(node.children):
                    yield child 
    elif isinstance(data, dict):
        if data.nodeType.uriTag in ['time-series', \
                                    'non-olap-native',
                                    'document']: #leaf node
            yield node_digest_model(data)

        else:
            yield node_digest_model(data)
            for child in flatten_metadata(data.children):
                yield child 

def flatten_data(data, record=None):
    """Flatten a nested dict generated from a deserialized JSON object /
       provided by ICANE's Restful data API. 

    Args:
      data (dict): a dictionary generated by the ''request()'' function with \
                   ICANE's API time-series data.
      record (list, optional): list of values representing a row. \
                                It's used within the recursive calls to the \
                                method. Defaults to None.

    Yields:
      row (list): A list representing a row in a flattened matrix.

    """
    
    if data.get('data'):#first level
        record = []
        row = []
        for j in sorted(list(flatten_data(data['data'], record))):
            yield j
    else: #other levels
        for k in sorted(list(data)):
            if isinstance(data[k], dict):      
                record.append(k)
                #try:
                
                for i in sorted(list(flatten_data(data[k], record))):
                    if len(record) == 1:
                        record.pop()
                    yield i
                #except Exception:
                #    pass
            else: #last level
                row = list(record)
                row.append(k)
                row.append(data[k])
                yield row
        if record:
            record.pop()

def add_query_string_params(node_type = None, inactive = None):
    """Add query string params to a string representing part of a URI.

    Args:
      node_type(string, optional): specifies the node type to return. Accepted \ 
                                  values: 'time-series', 'data-set', \
                                  'folder','theme', etc. See node_type class \
                                  for more info. Defaults to None.
      inactive(boolean, optional): if True, inactive nodes are also returned. \
                                   Defaults to None.

    Returns:
      query_string(string): conveniently concatenated query string params to \
                            conform the URI to be requested.

    """

    arguments = locals()
    query_string = ''
    operator = '?'
    for i, (argument, value) in enumerate(arguments.iteritems()):
        if (i == 0) and value is not None:
            argument = argument.replace('node_type','nodeType')
            query_string = query_string + operator + str(argument) + '=' +\
                               str(value)
            operator = '&'
        elif (i==0) and value is None:
            operator = '?'
        elif (value is not None):
            query_string = query_string + operator + str(argument) + '=' +\
                               str(value)
            operator = '?'
    return query_string

def add_path_params(section_uri_tag = None, subsection_uri_tag = None,
                    data_set_uri_tag = None):
    """Concatenate path params to a string representing part of a URI.

    Args:
      section_uri_tag(string, optional): uri_tag (ie, label) of the section \
                                         to be added as path parameter to the \
                                         URI to be requested. Defaults to None.
      subsection_uri_tag(string, optional): uri_tag (ie, label) of the \
                                            subsection to be added as path \
                                            parameter to the URI to be \
                                            requested. Must follow a section \
                                            uri_tag or an exception will be \
                                            thrown by the restful API. \
                                            Defaults to None.
      dataset_uri_tag(string, optional): uri_tag (ie, label) of the dataset \
                                            to be added as path parameter to \
                                            the URI to be requested. Must \
                                            follow a subsection uri_tag or an \
                                            exception will be thrown by the \
                                            restful API. Defaults to None.

    Returns:
      path(string): conveniently concatenated path params to conform the URI \
                    to be requested.

    """

    # argument order must be preserved, I can't find a better way of 
    # doing this, since it is not an OrderedDict.
    arguments = locals()
    values = []
    ordered_arg_names = ['section_uri_tag', 'subsection_uri_tag', 
                 'data_set_uri_tag']
   
    for name in ordered_arg_names:
        values.append(arguments[name])
    path = ''
    for value in values:
        if value is not None:
            path = path + '/' + str(value)
    return path


class BaseEntity(dict):
    """Class to convert deserialized JSON into a Python object. Basic \
       skeleton for almost all the module classes.
    
    Attributes:
      label_ (str): singular label of the converted entity. Ex: "category"
      plabel_ (str): plural label of the converted entity. Ex: "categories"
      
    """

    __metaclass__ = abc.ABCMeta 
    @abc.abstractmethod
    def __init__(self, dict_): 
        """Decode JSON to a Python object.
           See http://peedlecode.com/posts/python-json/

        Args:
          dict_ (dict): dictionary that results from deserialized JSON object.

        """
        
        super(BaseEntity, self).__init__(dict_)
        for key in self:
            items = self[key]
            if isinstance(items, list):
                for idx, item in enumerate(items):
                    if isinstance(item, dict):
                        items[idx] = self.__class__(item)
            elif isinstance(items, dict):
                self[key] = self.__class__(items)
                
    @abc.abstractmethod
    def __getattr__(self, key):
        """Get dictionary key as attribute. Overriden method.

        Args:
          key (string): key of the dictionary.

        Returns:
          self[key](string): key associated value.

        """

        return self[key]

class BaseMixin(dict):
    __metaclass__ = abc.ABCMeta
     
    label_ = None
    plabel_ = None
    
    @classmethod
    @abc.abstractmethod
    def get(cls, uri_tag):
        """Retrieve an entity by its uri_tag.
        Args:
         uri_tag (string): the uri_tag (ie. label) of the entity.

        Returns:
         Python object from the entity class represented by the uri_tag \
         parameter.

        """

        return cls(request(cls.label_ + '/' + str(uri_tag)))

    @classmethod
    @abc.abstractmethod
    def find_all(cls):
        """Retrieve all available entities of the class.
        Args:
         None

        Returns:
         List of Python objects from the entity class represented by the \
         uri_tag parameter.

        """

        entities = []
        for entity in request(cls.plabel_):
            entities.append(cls(entity))
        return entities

class DataMixin(dict):
    """Class to convert deserialized JSON into a Python object. Basic \
       skeleton for data and metadata subclasses.
    
    Attributes:
      label_ (str): singular label of the converted entity. Ex: "category"
      plabel_ (str): plural label of the converted entity. Ex: "categories"
      
    """
    __metaclass__ = abc.ABCMeta 
    
    label_ = None

    @classmethod
    @abc.abstractmethod
    def get_last_updated(cls):
        """Retrieve last updated date in dd/mm/YY format.
        Args:
         None.

        Returns:
         datetime.datetime object in dd/mm/YY format.

        """

        return datetime.datetime.fromtimestamp(
               int(str((request( str(cls.label_)
               + '/' + 'last-updated')))[0:-3])).strftime('%d/%m/%Y')
                
    @classmethod
    @abc.abstractmethod
    def get_last_updated_millis(cls):
        """Retrieve last updated date in milliseconds.
        Args:
         None.

        Returns:
         int with milliseconds. 

        """

        return int(str((request( str(cls.label_)
                + '/' + 'last-updated'))))

class Category(BaseEntity, BaseMixin):
    """ Class mapping icane.es 'Category' entity. A Category classifies \
        data based on their temporal or geographical area."""
    
    label_ = 'category'
    plabel_ = 'categories'


class Class(BaseEntity):
    """ Class mapping icane.es 'Class' entity."""
    
    label_ = 'class'
    plabel_ = 'classes'
    
    @classmethod
    def get(cls, class_name, lang):
        """Retrieve the description of a class or entity by its name.
            Args:
             class_name (string): name of the class to get the description of.
             lang (string): language; possible values: 'es', 'en'

            Returns:
             Python object from 'Class' class.

        """

        return cls(request(cls.label_ +
                           '/' + str(class_name) +
                           '/' + 'description' + '/' + lang))

    @classmethod
    def find_all(cls, lang):
        """Retrieve the description of all classes or entitiese.
            Args:
             lang (string): language; possible values: 'es', 'en'

            Returns:
             Python list of objects from 'Class' class.

        """

        entities = []
        response = request(cls.plabel_ + '/' + 'description' + '/' + lang)
        for entity in response[cls.plabel_]:
            entities.append(cls(entity))
        return entities

class Data(BaseEntity, DataMixin):
    """Class mapping icane.es 'Data' entity."""

    label_ = 'data'
     

class DataProvider(BaseEntity, BaseMixin):
    """Class mapping icane.es 'DataProvider' entity.  A DataProvider \
       represents an organisation which produces data or metadata."""

    label_ = 'data-provider'
    plabel_ = 'data-providers'


class DataSet(BaseEntity, BaseMixin):
    """Class mapping icane.es 'DataSet' entity. A DataSet represents any \
       organised collection of data."""

    label_ = 'data-set'
    plabel_ = 'data-sets'


class Link(BaseEntity, BaseMixin):
    """Class mapping icane.es 'Link' entity. A Link or hyperlink represents \
       a reference to data that can be followed."""

    label_ = 'link'
    plabel_ = 'links'


class LinkType(BaseEntity, BaseMixin):
    """Class mapping icane.es 'LinkType' entity. A LinkType is used to \
       distinguish among vocabulary specifications."""

    label_ = 'link-type'
    plabel_ = 'link-types'


class Measure(BaseEntity, BaseMixin):
    """Class mapping icane.es 'Measure' entity. A Measure represents a \
       phenomenon or phenomena to be measured in a data set."""

    label_ = 'measure'
    plabel_ = 'measures'


class Metadata(BaseEntity, DataMixin):
    """Class mapping icane.es 'Metadata' entity."""

    label_ = 'metadata'


class NodeType(BaseEntity, BaseMixin):
    """Class mapping icane.es 'node_type' entity. A node_type is used to \
       distinguish among typologies of levels in a hierarchical \
       representation of metadata."""

    label_ = 'node-type'
    plabel_ = 'node-types'


class Periodicity(BaseEntity, BaseMixin):
    """Class mapping icane.es 'Periodicity' entity. A Periodicity instance \
       represents the frequency of compilation of the data."""

    label_ = 'periodicity'
    plabel_ = 'periodicities'


class ReferenceArea(BaseEntity, BaseMixin):
    """Class mapping icane.es 'ReferenceArea' entity.  A ReferenceArea \
       represents the geographic area to which the measured statistical \
       phenomenon relates."""

    label_ = 'reference-area'
    plabel_ = 'reference-areas'


class Section(BaseEntity, BaseMixin):
    """Class mapping icane.es 'Section' entity. A Section represents \
       the first level of classification within a category."""

    label_ = 'section'
    plabel_ = 'sections'

    def get_subsections(self):
        """Retrieve all subsections belonging to a given section.
            Args:
             uri_tag (string): Section uri tag (ie, label).

            Returns:
             Python list of objects of'Subsection' class.

        """
        subsections = []
        subsection_array = request(self.label_ +
                            '/' + str(self.uriTag) +
                            '/' + 'subsections')
        for subsection in subsection_array:
            subsections.append(Subsection(subsection))
        return subsections 
    
    def get_subsection(self, subsection_uri_tag):
        """Retrieve a subsection instance for a given section.
            Args:
             section_uri_tag (string): Section uri tag (ie, label) of the \
                                       Subsection parent.
             subsection_uri_tag (string): The subsection uri tag to be \
                                          retrieved.
            Returns:
             Python objects of 'Subsection' class.

        """
        return Subsection(request('section' +
                     '/'+ self.uriTag +
                     '/' + subsection_uri_tag))

class Source(BaseEntity, BaseMixin):
    """Class mapping icane.es 'Source' entity. A Source represents a specific \
       data set, metadata set, database or metadata repository from where \
       data or metadata are available"""

    label_ = 'source'
    plabel_ = 'sources'


class Subsection(BaseEntity, BaseMixin):
    """Class mapping icane.es 'Subsection' entity. A Subsection \
       represents the second level of classification within a category, \
       i.e. the next level in a section."""

    label_ = 'subsection'
    plabel_ = 'subsections'

class TimePeriod(BaseEntity, BaseMixin):
    """Class mapping icane.es 'TimePeriod' entity. A TimePeriod \
       represents the period of time or point in time to which the measured \
       observation refers"""

    label_ = 'time-period'
    plabel_ = 'time-periods'


class TimeSeries(BaseEntity):
    """Class mapping icane.es 'TimeSeries' entity.  A TimeSeries \
       represents a set of ordered observations on a quantitative \
       characteristic of an individual or collective phenomenon taken at \
       different points of time. Lists of elements of this class are returned \
       adequately classified and nested in a structure with groups, themes \
       and statistics without semantic value."""

    label_ = 'time-series'
    plabel_ = 'time-series-list'
    
    @classmethod
    def get(cls, uri_tag, inactive=None):
        return cls(request(cls.label_ + '/' + str(uri_tag) +
        add_query_string_params(inactive = inactive)))

    def data_to_dataframe(self):
        """Convert TimeSeries data into pandas.DataFrame object.

            Returns:
            Python Pandas Dataframe.
        """
        resource = request(self.apiUris[3].uri) #third element is icane json
        data = pd.DataFrame(list(flatten_data(resource)))
        headers = list(resource['headers'])
        headers.append(unicode('Valor'))
        data.columns = headers
        if (self.category.id == 3):
            time_series = data.set_index([unicode(headers[0])]) 
            #TODO: check indexes pos
        else:
            time_series = data.set_index([unicode(headers[len(headers)-2])])
        return time_series
    
    def metadata_to_dataframe(self):
        """Convert TimeSeries metadata digest into pandas.DataFrame object.

            Returns:
            Python Pandas Dataframe.
        """
        table = []
        
        
        for node in flatten_metadata(self):
            table.append(node)
        metadata = pd.DataFrame(table, columns = ['id', 'title', 'active', 
                   'uri', 'metadataUri', 'resourceUri', 'documentation',
                   'methodology', 'mapScope', 'referenceResources', 
                   'description', 'theme', 'language', 'publisher', 'license', 
                   'topics', 'automatizedTopics', 'uriTag', 'uriTagEs', 
                   'initialPeriodDescription', 'finalPeriodDescription', 
                   'dataUpdate', 'dateCreated', 'lastUpdated', 'subsection', 
                   'section', 'category', 'dataset', 'periodicty', 'nodeType', 
                   'referenceArea', 'sources', 'measures', 'apiUris'])
        return metadata

    @classmethod
    def get_parent(cls, uri_tag):
        """Retrieve the parent node of the node or TimeSeries given by its \
           uri_tag.
            Args:
             uri_tag (string): uri_tag (ie, label) of the node or TimeSeries.

            Returns:
             Python TimeSeries object representing the parent node of the \
             given one.

        """
        return cls(request(cls.label_ + '/' + str(uri_tag) + '/' + 'parent'))
        
    @classmethod
    def get_parents(cls, uri_tag):
        """Retrieve all ancestors of the node or TimeSeries given by its \
           uri_tag.
            Args:
             uri_tag (string): uri_tag (ie, label) of the node or TimeSeries.

            Returns:
             Python list of TimeSeries objects representing the ancestors of \
             the given node.

        """
        parents = []
        parents_array = request(cls.label_ +
                            '/' + str(uri_tag) +
                            '/' + 'parents')
        for ancestor in parents_array:
            parents.append(TimeSeries(ancestor))
        return parents
    
    @classmethod
    def get_possible_subsections(cls, uri_tag):
        """Retrieve all possible subsections associated to a node or \
           TimeSeries uri_tag.
            Args:
             uri_tag (string): uri_tag (ie, label) of the node or TimeSeries.

            Returns:
             Python list of Subsection objects representing the subsections \
             associated to the given node.

        """
        subsections = []
        subsections_array = request(cls.label_ +
                                    '/' + str(uri_tag) +
                                    '/' + 'subsections')
        for subsection in subsections_array:
            subsections.append(Subsection(subsection))
        return subsections
    
    @classmethod
    def get_possible_time_series(cls, uri_tag):
        """Retrieve all possible nodes or time series associated to a node or \
           TimeSeries uri_tag.
            Args:
             uri_tag (string): uri_tag (ie, label) of the node or TimeSeries.

            Returns:
             Python list of TimeSeries objects representing the nodes or time \
             series associated to a given uri_tag.

        """
        time_series_list = []
        time_series_array = request(cls.plabel_ +
                                    '/' + str(uri_tag))
        for time_series in time_series_array:
            time_series_list.append(TimeSeries(time_series))
        return time_series_list

    @classmethod
    def find_all_datasets(cls,
                          category_uri_tag,
                          section_uri_tag,
                          subsection_uri_tag):
        """Retrieve all nodes of type dataset given its category, section \
            and subsection.
            Args:
             category_uri_tag (string): uri_tag (ie, label) of the category.
             section_uri_tag (string): uri_tag (ie, label) of the section.
             subsection_uri_tag (string): uri_tag (ie, label) of the subsection.

            Returns:
             Python list of TimeSeries objects with node_type='data-set' for \
             a given category, section and subsection.
             

        """
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
                          data_updated=None,
                          metadata_updated=None):
        """Retrieve all time series for a given data or metadata update date.
            
            Args:
             data_updated (string, optional): last data update date. Both \
                                             arguments are mutually exclusive.
             metadata_updated (string, optional): last metadata update date.
                                                 Both arguments are mutually \
                                                 exclusive.

            Returns:
             Python list of TimeSeries objects whose data or metadata have \
             been updated in the specified dates. 

        """
        time_series_list = []
        if (data_updated):
            time_series_array = request(cls.plabel_ + '?data_updated=' +
                                        data_updated)
        elif (metadata_updated):
            time_series_array = request(cls.plabel_ + '?data_updated=' +
                                        metadata_updated)    
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
        """Retrieve all nodes of type dataset given its category, section \
            and subsection.
            Args:
             category_uri_tag (string): uri_tag (ie, label) of the category.
             section_uri_tag (string, optional): uri_tag (ie, label) of the \
                 section. If present, it must follow a category uri-tag or an \
                 exception will be thrown by the restful API.
             subsection_uri_tag (string, optional): uri_tag (ie, label) of \
                 the subsection. If present, it must follow a section uri-tag \
                 or an exception will be thrown by the restful API.
             data_set_uri_tag (string, optional): uri_tag (ie, label) of the \
                 data-set. If present, it must follow a subsection uri-tag or \
                 an exception will be thrown by the restful API.
             node_type(string, optional): specifies the node type to return. \
                 Accepted values: 'time-series', 'data-set', 'folder','theme',\
                 etc. See node_type class for more info. Defaults to None.
             inactive(boolean, optional): if True, inactive nodes are also \
                 returned. Defaults to None.

            Returns:
             Python list of TimeSeries objects representing the nodes or time \
             series associated to a given category, section, subsection or \
             dataset uri_tag, filtered by node_type and inactive status.

        """
        time_series_list = []
        http_request =  category_uri_tag + add_path_params(
                        section_uri_tag, subsection_uri_tag, data_set_uri_tag)\
                        + '/' + cls.plabel_ +\
                        add_query_string_params(node_type_uri_tag, inactive)
        time_series_array = request(http_request)
        for time_series in time_series_array:
            time_series_list.append(TimeSeries(time_series))
        return time_series_list

class UnitOfMeasure(BaseEntity, BaseMixin):
    """Class mapping icane.es 'UnitOfMeasure' entity. A UnitOfMeasure \
       represents a quantity or increment by which something is counted or \
       described."""

    label_ = 'unit-of-measure'
    plabel_ = 'units-of-measure'

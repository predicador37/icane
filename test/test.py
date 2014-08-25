# -*- coding: utf-8 -*-
"""Testing class for icane package.

"""
import sys
sys.path.append('../icane')
import unittest
import metadata
import logging
import requests
import datetime

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
REQUESTS_LOG = logging.getLogger("requests")
REQUESTS_LOG.setLevel(logging.WARNING)

class TestGenericMethods(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata module methods """
    def setUp(self):
        self.node_digest_fields = 34

    def test_request(self):
        """ Test metadata.request() """
        section_instance = metadata.Section(metadata.request(
                                            'section/economy'))
        self.assertTrue(section_instance.title == 'Economía')
        self.assertRaises(requests.exceptions.HTTPError,
                          metadata.request, 'section/economic')
    
    def test_plain_metadata_model(self):
        """ Test metadata.plain_metadata_model() """
        node_instance = metadata.TimeSeries.get('quarterly-accounting-'
                                          'cantabria-base-2008-current-prices')
        node_digest = metadata.node_digest_model(node_instance)
        self.assertTrue(len(node_digest) == self.node_digest_fields)
        self.assertTrue(node_digest[22] == '31/10/2012')
              
    def test_flatten_metadata(self):
        """ Test metadata.flatten_metadata() """
        node_list = metadata.TimeSeries.find_all('regional-data',
                                                 'economy',
                                                 'labour-market')
        first_record_name = 'Estadísticas de empleo y paro'
        second_record_uri_tag = 'active-population-survey-bases'
        records = metadata.flatten_metadata(node_list)
        self.assertTrue(first_record_name == next(records)[1])
        self.assertTrue(second_record_uri_tag == next(records)[17])
    
    def test_add_query_string_params(self):
        """ Test metadata.add_query_string_params() """
        self.assertTrue(metadata.add_query_string_params('non-olap-native') == 
                        '?nodeType=non-olap-native')
       
        self.assertTrue(metadata.add_query_string_params('non-olap-native',
                                                         'True') == 
                        '?nodeType=non-olap-native&inactive=True')
    def test_add_path_params(self):
        """ Test metadata.add_path_params() """
        self.assertTrue(metadata.add_path_params('economy') == 
                        '/economy')
        self.assertTrue(metadata.add_path_params('economy', 'labour-market') == 
                        '/economy/labour-market')
       
        self.assertTrue(metadata.add_path_params('economy', 'labour-market',
                        'active-population-survey-bases') == 
                        '/economy/labour-market/active-population-survey-'
                        'bases') 
 
class TestCategory(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Category class """
    def setUp(self):
        pass
    
    def test_category(self):
        """ Test metadata.Category class"""
        self.assertRaises(ValueError, metadata.Category, 'not a json object')
        self.assertTrue(metadata.Category(
                        metadata.request('category/historical-data')).title
                        == 'Datos históricos')

    def test_get(self):
        """ Test metadata.Category get()"""
        self.assertRaises(requests.exceptions.HTTPError,
                          metadata.Category.get, 'regioal-data')
        self.assertEqual(metadata.Category.get('regional-data').title,
                         'Datos regionales')
        self.assertEqual(metadata.Category.get(3).uriTag, 'municipal-data')

        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.Category.get, 89)
        self.assertEqual(metadata.Category.get(1).title, 'Datos regionales')

    def test_find_all(self):
        """ Test metadata.Category find_all()"""
        categories = metadata.Category.find_all()
        self.assertEqual(len(categories), 4)
        self.assertTrue(metadata.Category.get('municipal-data') in categories)

class TestClass(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Class class """
    def setUp(self):
        pass
    
    def test_get(self):
        """ Test metadata.Class.get()"""
        self.assertEqual(metadata.Class.get('time-series','es').fields[0].name,
                         'active')
        self.assertEqual(metadata.Class.get('time-series','en').fields[1].name,
                         'apiUris')

    def test_find_all(self):
        """ Test metadata.Class.find_all()"""
        self.assertEqual(metadata.Class.find_all('en')[1].name, 'DataSet')
        self.assertEqual(metadata.Class.find_all('en')[2].name, 'TimeSeries')
                     
class TestData(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Data class """
    def setUp(self):
        pass
                        
    def test_get_last_updated(self):
        """ Test metadata.Data.get_last_updated()"""
        self.assertTrue(datetime.datetime.strptime(
                        metadata.Data.get_last_updated(), '%d/%m/%Y'))

    def test_get_last_updated_millis(self):
        """ Test metadata.Data.get_last_updated_millis()"""
        self.assertTrue(datetime.datetime.strptime(
                        datetime.datetime.fromtimestamp(
                        int(str(metadata.Data.get_last_updated_millis()
                        )[0:-3])).strftime('%d/%m/%Y'), '%d/%m/%Y'))
 
class TestDataProvider(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.DataProvider class """
    def setUp(self):
        pass

    def test_data_provider(self):
        """ Test metadata.DataProvider class"""
        self.assertRaises(ValueError,
                          metadata.DataProvider,
                          'not a json object')
        self.assertEqual(metadata.DataProvider(
                        metadata.request('data-provider/1')).title
                        , 'Instituto Nacional de Estadística')

    def test_get(self):
        """ Test metadata.DataProvider.get()"""
        self.assertRaises(requests.exceptions.HTTPError,
                          metadata.DataProvider.get,'E0012120')
        self.assertEqual(metadata.DataProvider.get('E00121204').acronym, 'INE')

        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.DataProvider.get, 999)
        self.assertEqual(metadata.DataProvider.get(3).title,
                         'Gobierno de España')

    def test_find_all(self):
        """ Test metadata.DataProvider.find_all()"""
        data_providers = metadata.DataProvider.find_all()
        self.assertTrue(len(data_providers) > 100)
        self.assertTrue(metadata.DataProvider.get('20') in data_providers)

class TestDataSet(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.DataSet class """
    def setUp(self):
        pass

    def test_data_set(self):
        """ Test metadata.DataSet class"""
        self.assertRaises(ValueError, metadata.DataSet, 'not a json object')
        self.assertEqual(metadata.DataSet(
                         metadata.request('data-set/87')).title,
                         'Empleo de las personas con discapacidad')

    def test_get(self):
        """ Test metadata.DataSet.get()"""
        self.assertRaises(requests.exceptions.HTTPError,
                          metadata.DataProvider.get, 'elections-autonomix')
        self.assertEqual(metadata.DataSet.get('elections-autonomic').acronym,
                         'EAUTO')

        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.DataSet.get, 999)
        self.assertEqual(metadata.DataSet.get(4).title, 'Aperturas de centros')

    def test_find_all(self):
        """ Test metadata.DataSet.find_all()"""
        data_sets = metadata.DataSet.find_all()
        self.assertTrue(len(data_sets) > 100)
        self.assertTrue(metadata.DataSet.get('regional-accounts-1995')
                        in data_sets)
 
class TestLink(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Link class """
    def setUp(self):
        pass
                       
    def test_link(self):
        """ Test metadata.Link class"""
        self.assertRaises(ValueError, metadata.Link, 'not a json object')
        self.assertEqual(metadata.Link(
                        metadata.request('link/472')).title, 'DBpedia')

    def test_get(self):
        """ Test metadata.Link.get()"""
        self.assertRaises(requests.exceptions.HTTPError, metadata.Link.get, 89)
        self.assertEqual(metadata.Link.get(478).title, 'LEM')

    def test_find_all(self):
        """ Test metadata.Link.find_all()"""
        links = metadata.Link.find_all()
        self.assertTrue(len(links) > 200)
        self.assertTrue(metadata.Link.get('873') in links)

class TestLinkType(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.LinkType class """
    def setUp(self):
        pass

    def test_link_type(self):
        """ Test metadata.LinkType class"""
        self.assertRaises(ValueError, metadata.LinkType, 'not a json object')
        self.assertEqual(metadata.LinkType(
                        metadata.request('link-type/1')).title, 'HTTP')

    def test_get(self):
        """ Test metadata.LinkType.get()"""
        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.LinkType.get, 99)
        self.assertEqual(metadata.LinkType.get(6).title, 'RDFS seeAlso')

    def test_find_all(self):
        """ Test metadata.LinkType.find_all()"""
        link_types = metadata.LinkType.find_all()
        self.assertTrue(len(link_types) == 8)
        self.assertTrue(metadata.LinkType.get('4') in link_types)

class TestMeasure(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Measure class """
    def setUp(self):
        pass

    def test_measure(self):
        """ Test metadata.Measure class"""
        self.assertRaises(ValueError, metadata.Measure, 'not a json object')
        self.assertEqual(metadata.Measure(
                        metadata.request('measure/1')).title, 'Parados')

    def test_get(self):
        """ Test metadata.Measure.get()"""
        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.Measure.get, 9999)
        self.assertEqual(metadata.Measure.get(5742).code, 'CMestancia')

    def test_find_all(self):
        """ Test metadata.Measure.find_all()"""
        measures = metadata.Measure.find_all()
        self.assertTrue(len(measures) > 3000)
        self.assertTrue(metadata.Measure.get('1503') in measures)

class TestMetadata(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Metadata class """
    def setUp(self):
        pass
        
    def test_get_last_updated(self):
        """ Test metadata.Metadata.get_last_updated()"""
        self.assertTrue(datetime.datetime.strptime(
                        metadata.Metadata.get_last_updated(), '%d/%m/%Y'))
                        
    def test_get_last_updated_millis(self):
        """ Test metadata.Metadata.get_last_updated_millis()"""
        self.assertTrue(datetime.datetime.strptime(
                        datetime.datetime.fromtimestamp(
                        int(str(metadata.Metadata.get_last_updated_millis()
                        )[0:-3])).strftime('%d/%m/%Y'), '%d/%m/%Y'))
 
class TestNodeType(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.NodeType class """
    def setUp(self):
        pass

    def test_node_type(self):
        """ Test metadata.NodeType class"""
        self.assertRaises(ValueError, metadata.NodeType, 'not a json object')
        self.assertEqual(metadata.NodeType(
                        metadata.request('node-type/1')).title, 'Sección')

    def test_get(self):
        """ Test metadata.NodeType.get()"""
        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.NodeType.get, 'documen')
        self.assertEqual(metadata.NodeType.get('document').title, 'Documento')

        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.NodeType.get, 99)
        self.assertEqual(metadata.NodeType.get(8).title, 'Categoría')

    def test_find_all(self):
        """ Test metadata.NodeType.find_all()"""
        node_types = metadata.NodeType.find_all()
        self.assertTrue(len(node_types) >= 10)
        self.assertTrue(metadata.NodeType.get('4') in node_types)

class TestPeriodicity(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Periodicity class """
    def setUp(self):
        pass

    def test_periodicity(self):
        """ Test metadata.Periodicity class"""
        self.assertRaises(ValueError, metadata.Periodicity,
                          'not a json object')
        self.assertEqual(metadata.Periodicity(
                        metadata.request('periodicity/annual')).title, 'Anual')

    def test_get(self):
        """ Test metadata.Periodicity.get()"""
        self.assertRaises(requests.exceptions.HTTPError,
                          metadata.Periodicity.get, 'montly')
        self.assertEqual(metadata.Periodicity.get('monthly').title, 'Mensual')

        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.Periodicity.get, 89)
        self.assertEqual(metadata.Periodicity.get(3).title, 'Trimestral')

    def test_find_all(self):
        """ Test metadata.Periodicity.find_all()"""
        periodicities = metadata.Periodicity.find_all()
        self.assertTrue(len(periodicities) == 12)
        self.assertTrue(metadata.Periodicity.get('irregular') in periodicities)

class TestReferenceArea(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.ReferenceArea class """
    def setUp(self):
        pass

    def test_reference_area(self):
        """ Test metadata.ReferenceArea class"""
        self.assertRaises(ValueError, metadata.ReferenceArea,
                          'not a json object')
        self.assertEqual(metadata.ReferenceArea(
                        metadata.request('reference-area/local')).title,
                        'Inframunicipal')

    def test_get(self):
        """ Test metadata.ReferenceArea.get()"""
        self.assertRaises(requests.exceptions.HTTPError,
                          metadata.ReferenceArea.get, 'regioal')
        self.assertEqual(metadata.ReferenceArea.get('regional').title, 
                         'Regional')

        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.ReferenceArea.get, 89)
        self.assertEqual(metadata.ReferenceArea.get(3).title, 'Nacional')

    def test_find_all(self):
        """ Test metadata.ReferenceArea.find_all()"""
        reference_areas = metadata.ReferenceArea.find_all()
        self.assertTrue(len(reference_areas) >= 6)
        self.assertTrue(metadata.ReferenceArea.get('municipal')
                        in reference_areas)

class TestSection(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Section class"""
    def setUp(self):
        pass

    def test_section(self):
        """ Test metadata.Section class"""
        self.assertRaises(ValueError, metadata.Section, 'not a json object')
        self.assertEqual(metadata.Section(
                        metadata.request('section/society')).title, 'Sociedad')

    def test_get(self):
        """ Test metadata.Section.get()"""
        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.Section.get, 'economia')
        self.assertEqual(metadata.Section.get('economy').title, 'Economía')

        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.Section.get, 89)
        self.assertEqual(metadata.Section.get(4).title, 
                         'Territorio y Medio ambiente')

    def test_find_all(self):
        """ Test metadata.Section.find_all()"""
        sections = metadata.Section.find_all()
        self.assertTrue(len(sections) == 5)
        self.assertTrue(metadata.Section.get('synthesis') in sections)
        
    def test_get_subsections(self):
        """ Test metadata.Section.get_subsections()"""
        self.assertTrue(metadata.Subsection.get(7) in
                        metadata.Section.get(2).get_subsections())
    
    def test_get_subsection(self):
        """ Test metadata.Section.get_subsection()"""
        with self.assertRaises(requests.exceptions.HTTPError):
            metadata.Section.get('economy').get_subsection('lavour-market')
        self.assertEqual(metadata.Section.get('economy').get_subsection(
                        'labour-market').title, 'Mercado de Trabajo')

class TestSource(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Source class"""
    def setUp(self):
        pass

    def test_source(self):
        """ Test metadata.Source class"""
        self.assertRaises(ValueError, metadata.Source,
                          'not a json object')
        self.assertEqual(metadata.Source(
                        metadata.request('source/45')).label,
                        'Censo agrario. ' +
                        'Instituto Nacional de Estadística (INE)')

    def test_get(self):
        """ Test metadata.Source.get()"""
        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.Source.get, 8999)
        self.assertEqual(metadata.Source.get(546).uri, 'http://www.ine.es')

    def test_find_all(self):
        """ Test metadata.Source.find_all()"""
        sources = metadata.Source.find_all()
        self.assertTrue(len(sources) > 500)
        self.assertTrue(metadata.Source.get('457') in sources)

class TestSubsection(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.Subsection class"""
    def setUp(self):
        pass

    def test_subsection(self):
        """ Test metadata.Subsection class"""
        self.assertRaises(ValueError, metadata.Subsection,
                          'not a json object')
        self.assertEqual(metadata.Subsection(
                        metadata.request('subsection/1')).title,
                        'Cifras de población')

    def test_get(self):
        """ Test metadata.Subsection.get()"""
        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.Subsection.get, 99)
        self.assertEqual(metadata.Subsection.get(13).title, 'Servicios')

    def test_find_all(self):
        """ Test metadata.Subsection.find_all()"""
        subsections = metadata.Subsection.find_all()
        self.assertTrue(len(subsections) > 20)
        self.assertTrue(metadata.Subsection.get('6') in subsections)

class TestTimePeriod(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.TimePeriod class"""
    def setUp(self):
        pass
    
    def test_time_period(self):
        """ Test metadata.TimePeriod class"""
        self.assertRaises(ValueError, metadata.TimePeriod,
                          'not a json object')
        self.assertEqual(metadata.TimePeriod(
                        metadata.request('time-period/593')).timeFormat, 'na')
    
    def test_get(self):
        """ Test metadata.TimePeriod.get()"""
        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.TimePeriod.get, 9999)
        self.assertEqual(metadata.TimePeriod.get(340).startYear, 1976)
    
    def test_find_all(self):
        """ Test metadata.TimePeriod.find_all()"""
        time_periods = metadata.TimePeriod.find_all()
        self.assertTrue(len(time_periods) > 300)
        self.assertTrue(metadata.TimePeriod.get('426') in time_periods)

class TestTimeSeries(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.TimeSeries class"""
    def setUp(self):
        pass
   
    def test_time_series(self):
        """ Test metadata.TimeSeries class"""
        self.assertRaises(ValueError, metadata.TimeSeries,
                          'not a json object')
        self.assertEqual(metadata.TimeSeries(
                         metadata.request('time-series/232')).title,
                         'Afiliados medios mensuales en alta laboral')
    
    def test_get(self):
        """ Test metadata.TimeSeries.get()"""
        self.assertRaises(requests.exceptions.HTTPError,
                          metadata.TimeSeries.get, 'quarterly-account')
        self.assertEqual(metadata.TimeSeries.get('quarterly-accounting-' +
        'cantabria-base-2008-current-prices').title, 'Precios corrientes')

        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.TimeSeries.get, 9999)
        self.assertEqual(metadata.TimeSeries.get(5036).title,
                         'Nomenclátor Cantabria')
        
        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.TimeSeries.get, 32)
        self.assertEqual(metadata.TimeSeries.get_inactive(32).uriTag,
                         'childbirths')    
    def test_data_to_dataframe(self):
        """ Test metadata.TimeSeries.data_to_dataframe()"""
        time_series = metadata.TimeSeries.get('quarterly-accounting-' +
                  'cantabria-base-2008-current-prices')
        data_frame = time_series.data_to_dataframe()
        self.assertTrue(len(data_frame) >= 2349)

    def test_metadata_to_dataframe(self):
        """ Test metadata.TimeSeries.metadata_to_dataframe()"""
        time_series = metadata.TimeSeries.get('quarterly-accounting-' +
                  'cantabria-base-2008-current-prices')
        node_list = metadata.TimeSeries.find_all('regional-data',
                                                 'economy',
                                                 'labour-market')
        dataframe = time_series.metadata_to_dataframe()
        metadata_array = []
        for node in node_list:
            metadata_array.append(node.metadata_to_dataframe())
        metadata_df = metadata_array[0].append(metadata_array[1:])
        self.assertTrue(len(metadata_df) >= 200)
        self.assertEqual('Precios corrientes', dataframe.iloc[0]['title'])
        self.assertEqual('ajuste,trimestre,sector', 
                         dataframe.iloc[0]['automatizedTopics'])
    
    def test_get_parent(self):
        """ Test metadata.TimeSeries.get_parent()"""
        self.assertEqual(metadata.TimeSeries.get_parent('terrain-series'),
                         metadata.TimeSeries.get('terrain'))
        self.assertEqual(metadata.TimeSeries.get_parent(4876),
                         metadata.TimeSeries.get(4106))

    def test_get_parents(self):
        """ Test metadata.TimeSeries.get_parents()"""
        self.assertTrue(metadata.TimeSeries.get('terrain')
                        in metadata.TimeSeries.get_parents('terrain-series'))
        self.assertTrue(metadata.TimeSeries.get(4106)
                        in metadata.TimeSeries.get_parents(4876))
    
    def test_get_possible_subsections(self):
        """ Test metadata.TimeSeries.get_possible_subsections()"""
        subsections = metadata.TimeSeries.get_possible_subsections(
                      'active-population-economic-sector-nace09')
        self.assertEqual(len(subsections), 1)
        self.assertTrue(metadata.Subsection.get(7) in subsections)
    
    def test_get_by_category(self):
        """ Test metadata.TimeSeries.get_by_category()"""
        time_series_list = metadata.TimeSeries.find_all('historical-data')
        self.assertTrue(len(time_series_list) > 50)
        self.assertTrue(metadata.TimeSeries.get('unemployment-employment')
                        in time_series_list)
    
    def test_get_by_category_and_section(self):
        """ Test metadata.TimeSeries.get_by_category_and_section()"""
        data_set_list = metadata.TimeSeries.find_all('municipal-data',
                                                     'society',
                                                     node_type_uri_tag =
                                                     'data-set')
        time_series_list = metadata.TimeSeries\
                                   .find_all('municipal-data',
                                             'territory-environment',
                                             node_type_uri_tag =
                                             'time-series')
        self.assertTrue(len(data_set_list) > 7)
        self.assertTrue(len(time_series_list) > 40)
        self.assertTrue(metadata.TimeSeries.get('terrain-series')
                        in time_series_list)                        
        self.assertTrue(metadata.TimeSeries.get('elections-municipal')
                        in data_set_list)
    
    def test_get_by_category_and_section_and_subsection(self):
        """ Test metadata.TimeSeries.get_by_category_and_section_and_
        subsection()"""
        node_list = metadata.TimeSeries.find_all('regional-data',
                                                 'economy',
                                                 'labour-market')
        node_list_all = metadata.TimeSeries.find_all('regional-data',
                                                 'economy',
                                                 'labour-market',
                                                 inactive = True)
        time_series_list = metadata.TimeSeries.find_all('regional-data',
                                                 'economy',
                                                 'labour-market',
                                                 node_type_uri_tag=
                                                 'time-series')
        time_series_list_all = metadata.TimeSeries.find_all('regional-data',
                                                 'economy',
                                                 'labour-market',
                                                 node_type_uri_tag=
                                                 'time-series',
                                                 inactive=True)
        data_set_list = metadata.TimeSeries.find_all('regional-data',
                                                     'society',
                                                     'living-standards',
                                                     node_type_uri_tag =
                                                     'data-set')
                                                     
        self.assertTrue(len(time_series_list_all) >= len(time_series_list))
        self.assertTrue(len(node_list) >= 2)
        self.assertEqual(len(node_list), len(node_list_all))
        self.assertTrue(len(data_set_list) >= 3)
        self.assertTrue(len(time_series_list) >= 60)
        self.assertTrue(metadata.TimeSeries.get('unemployment-benefits')
                        in data_set_list)
        self.assertTrue(metadata.TimeSeries.get('active-population-aged-16-'
                         'more-gender-age-group-activity-base-2011')
                         in time_series_list)
        self.assertTrue(metadata.TimeSeries.get('employment-unemployment-'
                        'statistics')
                         in node_list)

    def test_get_by_category_and_section_and_subsection_and_dataset(self):
        """ Test metadata.TimeSeries.get_by_category_and_section_and_
        subsection_and_dataset()"""        
        node_list = metadata.TimeSeries.find_all('regional-data',
                                                 'society',
                                                 'living-standards',
                                                 'unemployment-benefits')
        self.assertTrue(len(node_list) >= 2)       
        self.assertTrue(metadata.TimeSeries.get('unemployment-benefits-'
                        'requests-beneficiaries-expenditures')
                         in node_list)

    def test_get_datasets(self):
        """ Test metadata.TimeSeries.get_datasets()"""    
        data_set_list = metadata.TimeSeries.find_all_datasets(
                           'regional-data', 'economy', 'labour-market')
        data_set_filtered_list = metadata.TimeSeries.find_all(
                                 'regional-data', 'economy', 'labour-market',
                                 node_type_uri_tag='data-set')
        self.assertTrue(len(data_set_list) <= len(data_set_filtered_list))
        self.assertTrue(len(data_set_list) >= 3)
        self.assertTrue(metadata.TimeSeries.get('labour-societies')
                        in data_set_list)
                        
        
    def test_get_possible_time_series(self):
        """ Test metadata.TimeSeries.get_possible_time_series()"""
        time_series_list = metadata.TimeSeries.get_possible_time_series(
                           'active-population-economic-sector-nace09')
        self.assertEqual(len(time_series_list), 1)
        self.assertTrue(metadata.TimeSeries.get(5642) in time_series_list)
                       
class TestUnifOfMeasure(unittest.TestCase):
    # pylint: disable=R0904
    """ Test Case for metadata.UnitOfMeasure class"""
    def setUp(self):
        pass  

    def test_unif_of_measure(self):
        """ Test metadata.UnitOfMeasure class"""
        self.assertRaises(ValueError, metadata.UnitOfMeasure,
                          'not a json object')
        self.assertEqual(metadata.UnitOfMeasure(
                        metadata.request('unit-of-measure/1')).title, 'Años')

    def test_get(self):
        """ Test metadata.UnitOfMeasure.get()"""
        self.assertRaises(requests.exceptions.HTTPError, 
                          metadata.UnitOfMeasure.get, 9999)
        self.assertEqual(metadata.UnitOfMeasure.get(320).title,
                        'Número de bibliotecas y '
                        'Número de equipos de reproducción')

    def test_find_all(self):
        """ Test metadata.UnitOfMeasure.find_all()"""
        units_of_measure = metadata.UnitOfMeasure.find_all()
        self.assertTrue(len(units_of_measure) > 300)
        self.assertTrue(metadata.UnitOfMeasure.get('45') in units_of_measure)

if __name__ == '__main__':
    unittest.main()

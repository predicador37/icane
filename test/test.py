# -*- coding: utf-8 -*-
import sys
sys.path.append('../icane')
import unittest
import metadata
import logging
import urllib2
import time
import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestCategory(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_category(self):

        self.assertRaises(ValueError, metadata.Category, 'not a json object')
        self.assertTrue(metadata.Category(
                        metadata.request('category/historical-data')).title
                        == 'Datos históricos')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.Category.get, 'regioal-data')
        self.assertTrue(metadata.Category.get(
                        'regional-data').title
                        == 'Datos regionales')

        self.assertRaises(urllib2.HTTPError, metadata.Category.get, 89)
        self.assertTrue(metadata.Category.get(1).title == 'Datos regionales')

    def test_find_all(self):

        categories = metadata.Category.find_all()
        self.assertTrue(len(categories) == 4)
        self.assertTrue(metadata.Category.get('municipal-data') in categories)

class TestClass(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_get(self):
        self.assertTrue(metadata.Class.get('time-series','es').fields[0].name
                        == 'active')

    def test_find_all(self):
        self.assertTrue(metadata.Class.find_all('en')[1].name
                        == 'DataSet')
                        
class TestData(unittest.TestCase):

    def setUp(self):
        pass
                        
    def test_get_last_updated(self):
        self.assertTrue(datetime.datetime.strptime(
                        metadata.Data.get_last_updated(), '%d/%m/%Y'))

    def test_get_last_updated_millis(self):
          self.assertTrue(datetime.datetime.strptime(
                          datetime.datetime.fromtimestamp(
                          int(str(metadata.Data.get_last_updated_millis()
                          )[0:-3])).strftime('%d/%m/%Y'), '%d/%m/%Y'))

class TestDataProvider(unittest.TestCase):

    def setUp(self):
        pass

    def test_data_provider(self):

        self.assertRaises(ValueError,
                          metadata.DataProvider,
                          'not a json object')
        self.assertTrue(metadata.DataProvider(
                        metadata.request('data-provider/1')).title
                        == 'Instituto Nacional de Estadística')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.DataProvider.get,'E0012120')
        self.assertTrue(metadata.DataProvider.get('E00121204').acronym=='INE')

        self.assertRaises(urllib2.HTTPError, metadata.DataProvider.get, 999)
        self.assertTrue(metadata.DataProvider.get(3).title
                        == 'Gobierno de España')

    def test_find_all(self):

        data_providers = metadata.DataProvider.find_all()
        self.assertTrue(len(data_providers) > 100)
        self.assertTrue(metadata.DataProvider.get('20') in data_providers)

class TestDataSet(unittest.TestCase):

    def setUp(self):
        pass

    def test_data_set(self):

        self.assertRaises(ValueError, metadata.DataSet, 'not a json object')
        self.assertTrue(metadata.DataSet(metadata.request('data-set/87')).title
                        == 'Empleo de las personas con discapacidad')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.DataProvider.get, 'elections-autonomix')
        self.assertTrue(metadata.DataSet.get('elections-autonomic').acronym
                        == 'EAUTO')

        self.assertRaises(urllib2.HTTPError, metadata.DataSet.get, 999)
        self.assertTrue(metadata.DataSet.get(4).title
                        == 'Aperturas de centros')

    def test_find_all(self):

        data_sets = metadata.DataSet.find_all()
        self.assertTrue(len(data_sets) > 100)
        self.assertTrue(metadata.DataSet.get('regional-accounts-1995')
                        in data_sets)

class TestLink(unittest.TestCase):

    def setUp(self):
        pass
                       
    def test_link(self):

        self.assertRaises(ValueError, metadata.Link, 'not a json object')
        self.assertTrue(metadata.Link(
                        metadata.request('link/472')).title
                        == 'DBpedia')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError, metadata.Link.get, 89)
        self.assertTrue(metadata.Link.get(478).title == 'LEM')

    def test_find_all(self):

        links = metadata.Link.find_all()
        self.assertTrue(len(links) > 200)
        self.assertTrue(metadata.Link.get('873') in links)

class TestLinkType(unittest.TestCase):

    def setUp(self):
        pass

    def test_link_type(self):

        self.assertRaises(ValueError, metadata.LinkType, 'not a json object')
        self.assertTrue(metadata.LinkType(
                        metadata.request('link-type/1')).title == 'HTTP')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError, metadata.LinkType.get, 99)
        self.assertTrue(metadata.LinkType.get(6).title == 'RDFS seeAlso')

    def test_find_all(self):

        link_types = metadata.LinkType.find_all()
        self.assertTrue(len(link_types) == 8)
        self.assertTrue(metadata.LinkType.get('4') in link_types)

class TestMeasure(unittest.TestCase):

    def setUp(self):
        pass

    def test_measure(self):

        self.assertRaises(ValueError, metadata.Measure, 'not a json object')
        self.assertTrue(metadata.Measure(
                        metadata.request('measure/1')).title == 'Parados')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError, metadata.Measure.get, 9999)
        self.assertTrue(metadata.Measure.get(5742).code == 'CMestancia')

    def test_find_all(self):

        measures = metadata.Measure.find_all()
        self.assertTrue(len(measures) > 3000)
        self.assertTrue(metadata.Measure.get('1503') in measures)

class TestMetadata(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_get_last_updated(self):
         self.assertTrue(datetime.datetime.strptime(
                        metadata.Metadata.get_last_updated(), '%d/%m/%Y'))
                        
    def test_get_last_updated_millis(self):
          self.assertTrue(datetime.datetime.strptime(
                          datetime.datetime.fromtimestamp(
                          int(str(metadata.Metadata.get_last_updated_millis()
                          )[0:-3])).strftime('%d/%m/%Y'), '%d/%m/%Y'))

class TestNodeType(unittest.TestCase):

    def setUp(self):
        pass

    def test_node_type(self):

        self.assertRaises(ValueError, metadata.NodeType, 'not a json object')
        self.assertTrue(metadata.NodeType(
                        metadata.request('node-type/1')).title == 'Sección')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError, metadata.NodeType.get, 'documen')
        self.assertTrue(metadata.NodeType.get('document').title == 'Documento')

        self.assertRaises(urllib2.HTTPError, metadata.NodeType.get, 99)
        self.assertTrue(metadata.NodeType.get(8).title == 'Categoría')

    def test_find_all(self):

        node_types = metadata.NodeType.find_all()
        self.assertTrue(len(node_types) >= 10)
        self.assertTrue(metadata.NodeType.get('4') in node_types)

class TestPeriodicity(unittest.TestCase):

    def setUp(self):
        pass

    def test_periodicity(self):

        self.assertRaises(ValueError, metadata.Periodicity,
                          'not a json object')
        self.assertTrue(metadata.Periodicity(
                        metadata.request('periodicity/annual')).title
                        == 'Anual')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.Periodicity.get, 'montly')
        self.assertTrue(metadata.Periodicity.get('monthly').title == 'Mensual')

        self.assertRaises(urllib2.HTTPError, metadata.Periodicity.get, 89)
        self.assertTrue(metadata.Periodicity.get(3).title == 'Trimestral')

    def test_find_all(self):

        periodicities = metadata.Periodicity.find_all()
        self.assertTrue(len(periodicities) == 12)
        self.assertTrue(metadata.Periodicity.get('irregular') in periodicities)

class TestReferenceArea(unittest.TestCase):

    def setUp(self):
        pass

    def test_reference_area(self):

        self.assertRaises(ValueError, metadata.ReferenceArea,
                          'not a json object')
        self.assertTrue(metadata.ReferenceArea(
                        metadata.request('reference-area/local')).title
                        == 'Inframunicipal')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.ReferenceArea.get, 'regioal')
        self.assertTrue(metadata.ReferenceArea.get('regional').title
                        == 'Regional')

        self.assertRaises(urllib2.HTTPError, metadata.ReferenceArea.get, 89)
        self.assertTrue(metadata.ReferenceArea.get(3).title == 'Nacional')

    def test_find_all(self):

        reference_areas = metadata.ReferenceArea.find_all()
        self.assertTrue(len(reference_areas) >= 6)
        self.assertTrue(metadata.ReferenceArea.get('municipal')
                        in reference_areas)

class TestSection(unittest.TestCase):

    def setUp(self):
        pass

    def test_section(self):

        self.assertRaises(ValueError, metadata.Section, 'not a json object')
        self.assertTrue(metadata.Section(
                        metadata.request('section/society')).title
                        == 'Sociedad')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError, metadata.Section.get, 'economia')
        self.assertTrue(metadata.Section.get('economy').title == 'Economía')

        self.assertRaises(urllib2.HTTPError, metadata.Section.get, 89)
        self.assertTrue(metadata.Section.get(4).title
                        == 'Territorio y Medio ambiente')

    def test_find_all(self):

        sections = metadata.Section.find_all()
        self.assertTrue(len(sections) == 5)
        self.assertTrue(metadata.Section.get('synthesis') in sections)
        
    def test_get_subsections(self):
        
       self.assertTrue(metadata.Subsection.get(7) in
                       metadata.Section.get_subsections('economy'))
    
    def test_get_subsection_by_section_and_uri_tag(self):
        with self.assertRaises(urllib2.HTTPError):
            metadata.Section.get_subsection_by_section_and_uri_tag('economy',
                                                            'lavour-market')
        self.assertTrue(metadata.Section.get_subsection_by_section_and_uri_tag(
                        'economy','labour-market').title ==
                        'Mercado de Trabajo')

class TestSource(unittest.TestCase):

    def setUp(self):
        pass

    def test_source(self):

        self.assertRaises(ValueError, metadata.Source,
                          'not a json object')
        self.assertTrue(metadata.Source(
                        metadata.request('source/45')).label
                        == 'Censo agrario. ' +
                        'Instituto Nacional de Estadística (INE)')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError, metadata.Source.get, 8999)
        self.assertTrue(metadata.Source.get(546).uri == 'http://www.ine.es')

    def test_find_all(self):

        sources = metadata.Source.find_all()
        self.assertTrue(len(sources) > 500)
        self.assertTrue(metadata.Source.get('456') in sources)

class TestSubsection(unittest.TestCase):

    def setUp(self):
        pass

    def test_subsection(self):

        self.assertRaises(ValueError, metadata.Subsection,
                          'not a json object')
        self.assertTrue(metadata.Subsection(
                        metadata.request('subsection/1')).title
                        == 'Cifras de población')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError, metadata.Subsection.get, 99)
        self.assertTrue(metadata.Subsection.get(13).title == 'Servicios')

    def test_find_all(self):

        subsections = metadata.Subsection.find_all()
        self.assertTrue(len(subsections) > 20)
        self.assertTrue(metadata.Subsection.get('6') in subsections)

class TestTimePeriod(unittest.TestCase):

    def setUp(self):
        pass

    def test_time_period(self):

        self.assertRaises(ValueError, metadata.TimePeriod,
                          'not a json object')
        self.assertTrue(metadata.TimePeriod(
                        metadata.request('time-period/593')).timeFormat
                        == 'na')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError, metadata.TimePeriod.get, 9999)
        self.assertTrue(metadata.TimePeriod.get(340).startYear == 1976)

    def test_find_all(self):

        time_periods = metadata.TimePeriod.find_all()
        self.assertTrue(len(time_periods) > 300)
        self.assertTrue(metadata.TimePeriod.get('426') in time_periods)

class TestTimeSeries(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_time_series(self):

        self.assertRaises(ValueError, metadata.TimeSeries,
                          'not a json object')
        self.assertTrue(metadata.TimeSeries(
                        metadata.request('time-series/232')).title
                        == 'Afiliados medios mensuales en alta laboral')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.TimeSeries.get, 'quarterly-account')
        self.assertTrue(metadata.TimeSeries.get('quarterly-accounting-' +
        'cantabria-base-2008-current-prices').title == 'Precios corrientes')

        self.assertRaises(urllib2.HTTPError, metadata.TimeSeries.get, 9999)
        self.assertTrue(metadata.TimeSeries.get(5036).title
                        == 'Nomenclátor Cantabria')
        
        self.assertRaises(urllib2.HTTPError, metadata.TimeSeries.get, 32)
        self.assertTrue(metadata.TimeSeries.get(32, inactive='true').uriTag
                        == 'childbirths')
                        
    def test_to_dataframe(self):
        ts = metadata.TimeSeries.get('quarterly-accounting-' +
                  'cantabria-base-2008-current-prices')
        df = ts.to_dataframe()
        self.assertTrue(len(df) >= 2349)
        
    def test_get_parent(self):
        self.assertTrue(metadata.TimeSeries.get_parent('terrain-series')
                        == metadata.TimeSeries.get('terrain'))
        self.assertTrue(metadata.TimeSeries.get_parent(494)
                        == metadata.TimeSeries.get(493))
                        
    def test_get_parents(self):
        self.assertTrue(metadata.TimeSeries.get('terrain')
                        in metadata.TimeSeries.get_parents('terrain-series'))                        
        self.assertTrue(metadata.TimeSeries.get(493)
                        in metadata.TimeSeries.get_parents(494))
    
    def test_get_possible_subsections(self):
        subsections = metadata.TimeSeries.get_possible_subsections(
                      'active-population-economic-sector-nace09')
        self.assertTrue(len(subsections) == 2)
        self.assertTrue(metadata.Subsection.get(7) in subsections)
    
    def test_get_by_category(self):

        time_series_list = metadata.TimeSeries.find_all('historical-data')
        self.assertTrue(len(time_series_list) > 50)
        self.assertTrue(metadata.TimeSeries.get('unemployment-employment')
                        in time_series_list)

    def test_get_by_category_and_section(self):

        data_set_list = metadata.TimeSeries.find_all('municipal-data',
                                                     'society',
                                                     node_type_uri_tag =
                                                     'data-set')
        time_series_list = metadata.TimeSeries\
                                   .find_all('municipal-data',
                                             'territory-environment',
                                             node_type_uri_tag =
                                             'time-series')
        self.assertTrue(len(data_set_list) > 15)
        self.assertTrue(len(time_series_list) > 40)
        self.assertTrue(metadata.TimeSeries.get('terrain-series')
                        in time_series_list)                        
        self.assertTrue(metadata.TimeSeries.get('elections-municipal')
                        in data_set_list)

    def test_get_by_category_and_section_and_subsection(self):
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
                                                     'economy',
                                                     'labour-market',
                                                     node_type_uri_tag =
                                                     'data-set')
                                                     
        self.assertTrue(len(time_series_list_all) >= len(time_series_list))
        self.assertTrue(len(node_list) >= 3)
        self.assertTrue(len(node_list) == len(node_list_all))
        self.assertTrue(len(data_set_list) >= 20)
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
        node_list = metadata.TimeSeries.find_all('regional-data',
                                                 'economy',
                                                 'labour-market',
                                                 'unemployment-benefits')        
     
        self.assertTrue(len(node_list) >= 2)
       
        self.assertTrue(metadata.TimeSeries.get('unemployment-benefits-'
                        'requests-beneficiaries-expenditures')
                         in node_list)

    def test_get_datasets(self):

        data_set_list = metadata.TimeSeries.find_all_datasets(
                           'regional-data', 'economy', 'labour-market')
        data_set_filtered_list = metadata.TimeSeries.find_all(
                                 'regional-data', 'economy', 'labour-market',
                                 node_type_uri_tag='data-set')
        self.assertTrue(len(data_set_list) == len(data_set_filtered_list))
        self.assertTrue(len(data_set_list) >= 3)
        self.assertTrue(metadata.TimeSeries.get('labour-societies')
                        in data_set_list)
                        
        
    def test_get_possible_time_series(self):
        time_series_list = metadata.TimeSeries.get_possible_time_series(
                           'active-population-economic-sector-nace09')
        self.assertTrue(len(time_series_list) == 2)
        self.assertTrue(metadata.TimeSeries.get(5642) in time_series_list)
                        
class TestUnifOfMeasure(unittest.TestCase):

    def setUp(self):
        pass  

    def test_unif_of_measure(self):

        self.assertRaises(ValueError, metadata.UnitOfMeasure,
                          'not a json object')
        self.assertTrue(metadata.UnitOfMeasure(
                        metadata.request('unit-of-measure/1')).title
                        == 'Años')

    def test_get(self):

        self.assertRaises(urllib2.HTTPError, metadata.UnitOfMeasure.get, 9999)
        self.assertTrue(metadata.UnitOfMeasure.get(320).title
                        == 'Número de bibliotecas y ' +
                        'Número de equipos de reproducción')

    def test_find_all(self):

        units_of_measure = metadata.UnitOfMeasure.find_all()
        self.assertTrue(len(units_of_measure) > 300)
        self.assertTrue(metadata.UnitOfMeasure.get('45') in units_of_measure)

if __name__ == '__main__':
    unittest.main()

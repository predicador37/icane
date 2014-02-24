# -*- coding: utf-8 -*-
import sys
sys.path.append('../icane')
import unittest
import metadata
import logging
import urllib2
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestIcaneMetadata(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_category(self):

        self.assertRaises(ValueError, metadata.Category, 'not a json object')
        self.assertTrue(metadata.Category(
                        metadata.request('category/historical-data')).title
                        == 'Datos históricos')

    def test_get_category(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.Category.get, 'regioal-data')
        self.assertTrue(metadata.Category.get(
                        'regional-data').title
                        == 'Datos regionales')

        self.assertRaises(urllib2.HTTPError, metadata.Category.get, 89)
        self.assertTrue(metadata.Category.get(1).title == 'Datos regionales')

    def test_get_categories(self):

        categories = metadata.Category.find_all()
        self.assertTrue(len(categories) == 4)
        self.assertTrue(metadata.Category.get('municipal-data') in categories)
    
    def test_get_class(self):
        self.assertTrue(metadata.Class.get('time-series','es').fields[0].name
                        == 'active')
                        
    #Uncomment when proper content is returned in API  
    
    #def test_get_classes(self):
    #    self.assertTrue(metadata.Class.find_all('en').classes[1].name 
    #                    == 'DataSet')
        
    def test_data_provider(self):

        self.assertRaises(ValueError,
                          metadata.DataProvider,
                          'not a json object')
        self.assertTrue(metadata.DataProvider(
                        metadata.request('data-provider/1')).title
                        == 'Instituto Nacional de Estadística')

    def test_get_data_provider(self):

        #Uncomment when proper method is implemented in API
        #self.assertRaises(urllib2.HTTPError,
                           #metadata.DataProvider.get,'E0012120')
        #self.assertTrue(metadata.DataProvider.get('E00121204').acronym=='INE')

        self.assertRaises(urllib2.HTTPError, metadata.DataProvider.get, 999)
        self.assertTrue(metadata.DataProvider.get(3).title
                        == 'Gobierno de España')

    def test_get_data_providers(self):

        data_providers = metadata.DataProvider.find_all()
        self.assertTrue(len(data_providers) > 100)
        self.assertTrue(metadata.DataProvider.get('20') in data_providers)

    def test_data_set(self):

        self.assertRaises(ValueError, metadata.DataSet, 'not a json object')
        self.assertTrue(metadata.DataSet(metadata.request('data-set/87')).title
                        == 'Empleo de las personas con discapacidad')

    def test_get_data_set(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.DataProvider.get, 'elections-autonomix')
        self.assertTrue(metadata.DataSet.get('elections-autonomic').acronym
                        == 'EAUTO')

        self.assertRaises(urllib2.HTTPError, metadata.DataSet.get, 999)
        self.assertTrue(metadata.DataSet.get(4).title
                        == 'Aperturas de centros')

    def test_get_data_sets(self):

        data_sets = metadata.DataSet.find_all()
        self.assertTrue(len(data_sets) > 100)
        self.assertTrue(metadata.DataSet.get('regional-accounts-1995')
                        in data_sets)
    
    def test_get_last_updated_data(self):
        self.assertTrue(metadata.Data.get_last_updated() == '21/02/2014')
                       #time.strftime("%d/%m/%Y"))
        
    def test_get_last_updated_metadata(self):
       self.assertTrue(metadata.Metadata.get_last_updated() == '21/02/2014')
                       #time.strftime("%d/%m/%Y"))
                       
    def test_link(self):

        self.assertRaises(ValueError, metadata.Link, 'not a json object')
        self.assertTrue(metadata.Link(
                        metadata.request('link/472')).title
                        == 'DBpedia')

    def test_get_link(self):

        self.assertRaises(urllib2.HTTPError, metadata.Link.get, 89)
        self.assertTrue(metadata.Link.get(478).title == 'LEM')

    def test_get_links(self):

        links = metadata.Link.find_all()
        self.assertTrue(len(links) > 200)
        self.assertTrue(metadata.Link.get('873') in links)

    def test_link_type(self):

        self.assertRaises(ValueError, metadata.LinkType, 'not a json object')
        self.assertTrue(metadata.LinkType(
                        metadata.request('link-type/1')).title == 'HTTP')

    def test_get_link_type(self):

        self.assertRaises(urllib2.HTTPError, metadata.LinkType.get, 99)
        self.assertTrue(metadata.LinkType.get(6).title == 'RDFS seeAlso')

    def test_get_link_types(self):

        link_types = metadata.LinkType.find_all()
        self.assertTrue(len(link_types) == 8)
        self.assertTrue(metadata.LinkType.get('4') in link_types)

    def test_measure(self):

        self.assertRaises(ValueError, metadata.Measure, 'not a json object')
        self.assertTrue(metadata.Measure(
                        metadata.request('measure/1')).title == 'Parados')

    def test_get_measure(self):

        #self.assertRaises(urllib2.HTTPError, metadata.Link.get,'economia')
        #self.assertTrue(metadata.Link.get('economy').title=='Economía')

        self.assertRaises(urllib2.HTTPError, metadata.Measure.get, 9999)
        self.assertTrue(metadata.Measure.get(5742).code == 'CMestancia')

    def test_get_measures(self):

        measures = metadata.Measure.find_all()
        self.assertTrue(len(measures) > 3000)
        self.assertTrue(metadata.Measure.get('1503') in measures)

    def test_node_type(self):

        self.assertRaises(ValueError, metadata.NodeType, 'not a json object')
        self.assertTrue(metadata.NodeType(
                        metadata.request('node-type/1')).title == 'Sección')

    def test_get_node_type(self):

        self.assertRaises(urllib2.HTTPError, metadata.NodeType.get, 'documen')
        self.assertTrue(metadata.NodeType.get('document').title == 'Documento')

        self.assertRaises(urllib2.HTTPError, metadata.NodeType.get, 99)
        self.assertTrue(metadata.NodeType.get(8).title == 'Categoría')

    def test_get_node_types(self):

        node_types = metadata.NodeType.find_all()
        self.assertTrue(len(node_types) >= 10)
        self.assertTrue(metadata.NodeType.get('4') in node_types)

    def test_periodicity(self):

        self.assertRaises(ValueError, metadata.Periodicity,
                          'not a json object')
        self.assertTrue(metadata.Periodicity(
                        metadata.request('periodicity/annual')).title
                        == 'Anual')

    def test_get_periodicity(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.Periodicity.get, 'montly')
        self.assertTrue(metadata.Periodicity.get('monthly').title == 'Mensual')

        self.assertRaises(urllib2.HTTPError, metadata.Periodicity.get, 89)
        self.assertTrue(metadata.Periodicity.get(3).title == 'Trimestral')

    def test_get_periodicities(self):

        periodicities = metadata.Periodicity.find_all()
        self.assertTrue(len(periodicities) == 12)
        self.assertTrue(metadata.Periodicity.get('irregular') in periodicities)

    def test_reference_area(self):

        self.assertRaises(ValueError, metadata.ReferenceArea,
                          'not a json object')
        self.assertTrue(metadata.ReferenceArea(
                        metadata.request('reference-area/local')).title
                        == 'Inframunicipal')

    def test_get_reference_area(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.ReferenceArea.get, 'regioal')
        self.assertTrue(metadata.ReferenceArea.get('regional').title
                        == 'Regional')

        self.assertRaises(urllib2.HTTPError, metadata.ReferenceArea.get, 89)
        self.assertTrue(metadata.ReferenceArea.get(3).title == 'Nacional')

    def test_get_reference_areas(self):

        reference_areas = metadata.ReferenceArea.find_all()
        self.assertTrue(len(reference_areas) >= 6)
        self.assertTrue(metadata.ReferenceArea.get('municipal')
                        in reference_areas)

    def test_section(self):

        self.assertRaises(ValueError, metadata.Section, 'not a json object')
        self.assertTrue(metadata.Section(
                        metadata.request('section/society')).title
                        == 'Sociedad')

    def test_get_section(self):

        self.assertRaises(urllib2.HTTPError, metadata.Section.get, 'economia')
        self.assertTrue(metadata.Section.get('economy').title == 'Economía')

        self.assertRaises(urllib2.HTTPError, metadata.Section.get, 89)
        self.assertTrue(metadata.Section.get(4).title
                        == 'Territorio y Medio ambiente')

    def test_get_sections(self):

        sections = metadata.Section.find_all()
        self.assertTrue(len(sections) == 5)
        self.assertTrue(metadata.Section.get('synthesis') in sections)
        
    def test_get_subsections_from_section(self):
        
       self.assertTrue(metadata.Subsection.get(7) in
                       metadata.Section.get_subsections('economy'))

    def test_source(self):

        self.assertRaises(ValueError, metadata.Source,
                          'not a json object')
        self.assertTrue(metadata.Source(
                        metadata.request('source/45')).label
                        == 'Censo agrario. ' +
                        'Instituto Nacional de Estadística (INE)')

    def test_get_source(self):

        self.assertRaises(urllib2.HTTPError, metadata.Source.get, 8999)
        self.assertTrue(metadata.Source.get(546).uri == 'http://www.ine.es')

    def test_get_sources(self):

        sources = metadata.Source.find_all()
        self.assertTrue(len(sources) > 500)
        self.assertTrue(metadata.Source.get('456') in sources)

    def test_subsection(self):

        self.assertRaises(ValueError, metadata.Subsection,
                          'not a json object')
        self.assertTrue(metadata.Subsection(
                        metadata.request('subsection/1')).title
                        == 'Cifras de población')

    def test_get_subsection(self):

       # self.assertRaises(urllib2.HTTPError, 
       #                   metadata.Subsection.find_by_section_and_uri_tag,
       #                   ['economy','lavour-market'])
        with self.assertRaises(urllib2.HTTPError):
            metadata.Subsection.find_by_section_and_uri_tag('economy',
                                                            'lavour-market')
        self.assertTrue(metadata.Subsection.find_by_section_and_uri_tag(
                        'economy','labour-market').title ==
                        'Mercado de Trabajo')

        self.assertRaises(urllib2.HTTPError, metadata.Subsection.get, 99)
        self.assertTrue(metadata.Subsection.get(13).title == 'Servicios')

    def test_get_subsections(self):

        subsections = metadata.Subsection.find_all()
        self.assertTrue(len(subsections) > 20)
        self.assertTrue(metadata.Subsection.get('6') in subsections)

    def test_time_period(self):

        self.assertRaises(ValueError, metadata.TimePeriod,
                          'not a json object')
        self.assertTrue(metadata.TimePeriod(
                        metadata.request('time-period/593')).timeFormat
                        == 'na')

    def test_get_time_period(self):

        self.assertRaises(urllib2.HTTPError, metadata.TimePeriod.get, 9999)
        self.assertTrue(metadata.TimePeriod.get(340).startYear == 1976)

    def test_get_time_periods(self):

        time_periods = metadata.TimePeriod.find_all()
        self.assertTrue(len(time_periods) > 300)
        self.assertTrue(metadata.TimePeriod.get('426') in time_periods)
    
    def test_time_series(self):

        self.assertRaises(ValueError, metadata.TimeSeries,
                          'not a json object')
        self.assertTrue(metadata.TimeSeries(
                        metadata.request('time-series/232')).title
                        == 'Afiliados medios mensuales en alta laboral')

    def test_get_time_series(self):

        self.assertRaises(urllib2.HTTPError,
                          metadata.TimeSeries.get, 'quarterly-account')
        self.assertTrue(metadata.TimeSeries.get('quarterly-accounting-' +
        'cantabria-base-2008-current-prices').title == 'Precios corrientes')

        self.assertRaises(urllib2.HTTPError, metadata.TimeSeries.get, 9999)
        self.assertTrue(metadata.TimeSeries.get(5036).title
                        == 'Nomenclátor Cantabria')
                        
    def test_get_data(self):
        test_ts = metadata.TimeSeries.get('quarterly-accounting-' +
                  'cantabria-base-2008-current-prices')
        data = test_ts.get_data()
        self.assertTrue(len(data.rows) > 20)
        
    ''' 
    #Uncomment when methods are implemented in API
    def test_get_time_series_parent(self):
        self.assertTrue(metadata.TimeSeries.get_parent('terrain-series')
                        == metadata.TimeSeries.get('terrain'))
                        
    def test_get_time_series_parents(self):
        self.assertTrue(metadata.TimeSeries.get('terrain')
                        in metadata.TimeSeries.get_parents('terrain-series'))
    '''
    def test_get_time_series_list_by_category(self):

        time_series_list = metadata.TimeSeries.find_all('historical-data')
        self.assertTrue(len(time_series_list) > 50)
        self.assertTrue(metadata.TimeSeries.get('unemployment-employment')
                        in time_series_list)

    def test_get_time_series_list_by_category_and_section(self):

        data_set_list = metadata.TimeSeries.find_all('municipal-data',
                                                     'society')
        time_series_list = metadata.TimeSeries.find_all('municipal-data',
                                                        'territory-environment',
                                                        node_type_uri_tag =
                                                        'time-series')
        self.assertTrue(len(data_set_list) > 15)
        self.assertTrue(len(time_series_list) > 40)
        self.assertTrue(metadata.TimeSeries.get('terrain-series')
                        in time_series_list)                        
        self.assertTrue(metadata.TimeSeries.get('elections-municipal')
                        in data_set_list)
    #TODO: comprobar que el resultado de esta funcion es el mismo que con node-type=data-set
    def test_get_time_series_datasets(self):

        data_set_list = metadata.TimeSeries.find_all_datasets(
                           'regional-data', 'economy', 'labour-market')
        self.assertTrue(len(data_set_list) >= 3)
        self.assertTrue(metadata.TimeSeries.get('labour-societies')
                        in data_set_list)
                        
    def test_get_time_series_possible_subsections(self):
        subsections = metadata.TimeSeries.get_possible_subsections(
                      'active-population-economic-sector-nace09')
        self.assertTrue(len(subsections) == 2)
        self.assertTrue(metadata.Subsection.get(7) in subsections)
        
    def test_get_possible_time_series(self):
        time_series_list = metadata.TimeSeries.get_possible_time_series(
                           'active-population-economic-sector-nace09')
        self.assertTrue(len(time_series_list) == 2)
        self.assertTrue(metadata.TimeSeries.get(5642) in time_series_list)
                        
    def test_get_time_series_list_by_category_and_section_and_subsection(self):

        data_set_list = metadata.TimeSeries.find_all('regional-data',
                                                     'economy',
                                                     'labour-market')
        self.assertTrue(len(data_set_list) >= 3)
        self.assertTrue(metadata.TimeSeries.get('social-protection')
                        in data_set_list)

    def test_unif_of_measure(self):

        self.assertRaises(ValueError, metadata.UnitOfMeasure,
                          'not a json object')
        self.assertTrue(metadata.UnitOfMeasure(
                        metadata.request('unit-of-measure/1')).title
                        == 'Años')

    def test_unit_of_measure(self):

        self.assertRaises(urllib2.HTTPError, metadata.UnitOfMeasure.get, 9999)
        self.assertTrue(metadata.UnitOfMeasure.get(320).title
                        == 'Número de bibliotecas y ' +
                        'Número de equipos de reproducción')

    def test_units_of_measure(self):

        units_of_measure = metadata.UnitOfMeasure.find_all()
        self.assertTrue(len(units_of_measure) > 300)
        self.assertTrue(metadata.UnitOfMeasure.get('45') in units_of_measure)

if __name__ == '__main__':
    unittest.main()

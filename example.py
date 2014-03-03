# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/predicador/code/icane/icane/')
import metadata



series = metadata.TimeSeries.get('census-series-1900-2001')
#series = metadata.TimeSeries.get('affiliated-workers-activity-municipality-semester')
#series = metadata.TimeSeries.get('active-population-aged-16-more-gender-age-group-activity')
#series = metadata.TimeSeries.get('quarterly-accounting-cantabria-base-2008-current-prices')
df = series.get_dataframe()
noja=df[df.ix[:,1]==unicode(' 39047 - Noja')]
noja.plot(title='Population evolution in Noja', kind='bar')
print noja
print type(noja)
print len(noja)

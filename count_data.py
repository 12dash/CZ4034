import pysolr
import pandas as pd

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=100)
params = { 
  'facet': 'true',
  'facet.field': 'tweet',
  'rows': '20000',
  'facet.limit': '-1'
}


results = solr.search('*:*', **params)
fa = results.facets
r= fa['facet_fields']['tweet']
re = []
i = 0
lim = len(r)
for i in range(0,lim):
    if r[i] != int:
      re.append(r[i])


print(len(re))
print(re)
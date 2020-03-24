# If on Python 2.X
from __future__ import print_function
import pysolr

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)

# How you'd index data.

# Note that the add method has commit=True by default, so this is
# immediately committed to your index.

# You can index a parent/child document relationship by
# associating a list of child documents with the special key '_doc'. This
# is helpful for queries that join together conditions on children and parent
# documents.

# Later, searching is easy. In the simple case, just a plain Lucene-style
# query is fine.
results = solr.search('tweet:corona')

# The ``Results`` object stores total results found, by default the top
# ten most relevant results and any additional data like
# facets/highlighting/spelling/etc.
print("Saw {0} result(s).".format(len(results)))

# Just loop over it to access the results.
for result in results:
    print("The title is '{0}'.".format(result['tweet']))

# For a more advanced query, say involving highlighting, you can pass
# additional options to Solr.


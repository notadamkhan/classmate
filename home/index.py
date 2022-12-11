import algoliasearch_django as algoliasearch

from .models import Class

algoliasearch.register(Class)
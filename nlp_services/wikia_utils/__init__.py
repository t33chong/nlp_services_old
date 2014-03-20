"""
This module contains various Wikia utilities.
"""

import requests
from ..syntax import AllNounsService


def get_top_articles(wiki_id, n=50):
    """
    Get the top n articles for a given wiki ID.

    :type wiki_id: string
    :param wiki_id: The ID of the wiki in Solr

    :type n: int
    :param n: The number of articles to return

    :rtype: list
    :return: A list of article ID strings
    """
    articles = []
    hostname = requests.get(
        'http://www.wikia.com/api/v1/Wikis/Details',
        params={'ids': wiki_id}).json().get('items', {}).get(wiki_id,
                                                             {}).get('url')
    if hostname:
        items = requests.get(hostname +
                             'api/v1/Articles/List?limit=%d' % n).json()
        articles = ['%s_%i' % (wiki_id, item.get('id')) for item in
                    items.get('items', [])]
    return articles


def main_page_nps(wiki_id):
    response = requests.get(
        'http://search-s10:8983/solr/main/select',
        params=dict(q='wid:%s AND is_main_page:true' % wiki_id, fl='id',
                    wt='json'))

    docs = response.json().get('response', {}).get('docs', [{}])
    if not docs:
        return []
    doc_id = docs[0].get('id', None)

    return AllNounsService().get_value(doc_id)

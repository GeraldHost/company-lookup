import requests 
from lxml import html
from functools import reduce

GOV_URL = 'https://beta.companieshouse.gov.uk/company'

def combine_to_dict(key, values):
    key_values = list(zip(key, values))
    return [{"key": key.strip(), "value": value.strip()} for (key, value) in key_values]

def get_tree(url):
    page = requests.get(url)
    return html.fromstring(page.content)

def get_company_name(tree):
    co_name = tree.xpath('//*[@class="company-header"]/*[@class="heading-xlarge"]//text()')
    return co_name

def get_company_data(tree):
    co_keys = tree.xpath('//*[@id="content-container"]//dt//text()')
    co_values = tree.xpath('//*[@id="content-container"]//dd[@class="text data"]//text()')
    return combine_to_dict(co_keys, co_values)

def get_officers(tree):
    names = tree.xpath('//*[@class="appointments-list"]//div//span//a//text()')
    status = tree.xpath('//*[@class="appointments-list"]//div//div//span[contains(@class, "status-tag")]//text()')
    return combine_to_dict(names, status)

def lookup_company(n):
    co_url = "/".join([GOV_URL, n])
    tree = get_tree(co_url)

    co_name = get_company_name(tree)
    co_data = get_company_data(tree)

    return co_name, co_data

def lookup_officers(n):
    co_officers_url = "/".join([GOV_URL, n, 'officers'])
    tree = get_tree(co_officers_url)

    officers = get_officers(tree)

    return officers

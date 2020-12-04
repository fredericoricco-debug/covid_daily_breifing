from main import *

def test_config_fetcher():
    assert config_fetcher('covid_region') != None

def test_hhmm_to_seconds():
    assert hhmm_to_seconds('2020-12-03T15:21') == 55260

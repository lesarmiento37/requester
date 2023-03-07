import pytest
from converter import str_converter, name_provider

def test_converter_raw():
    raw_string = "message=This+is+a+test&to=Leonardo+Sarmiento&from=Rita+Asturia&timeToLifeSec=45"
    assert str_converter(raw_string) == {'message': 'This is a test','to': 'Leonardo Sarmiento','from': 'Rita Asturia','timeToLifeSec': '45'}

def test_retrieve_name():
    raw_name = {'message': 'This is a test','to': 'Leonardo Sarmiento','from': 'Rita Asturia','timeToLifeSec': '45'}
    assert name_provider(raw_name) == {"message":"Hello Leonardo Sarmiento, your message will be send"}

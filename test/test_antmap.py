import json
import sys

sys.path.append("./src")

import pytest

import AntMap


@pytest.fixture
def ant_map():
    return AntMap.AntMap()

@pytest.fixture
def map_json():
    return json.load(file("basic_map.json"))

def test_defaults(ant_map):
    assert ant_map.start_location == (0,0)
    assert ant_map.end_location == (0,0)
    assert ant_map.ant_location == (0,0, AntMap.EAST)
    assert ant_map.map == ()

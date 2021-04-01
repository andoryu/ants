import json
import sys

sys.path.append("./src")

import pytest

import AntMap


@pytest.fixture
def ant_map():
    return AntMap.AntMap()

@pytest.fixture
def ant_map_w_good_file():
    return AntMap.AntMap("test/basic_map.json")

def test_defaults(ant_map):
    assert ant_map.start_location == [0,0]
    assert ant_map.end_location == [0,0]
    assert ant_map.ant_location == (0, 0, AntMap.EAST)
    assert ant_map.map == []
    assert ant_map.style == AntMap.BOUNDED
    assert ant_map.loaded == False


def test_missing_def_file(ant_map):
    assert ant_map.load_definition("absent_test_file123.json") == False
    assert ant_map


def test_invalid_json_file(ant_map, tmp_path):
    json_file = tmp_path / "temp.json"
    json_file.write_text('{ "a": 1 "b": 2 }')

    assert ant_map.load_definition(json_file.as_posix()) == False
    assert ant_map

def test_incorrect_antmap_file(ant_map, tmp_path):
    json_file = tmp_path / "temp.json"
    json_file.write_text('{ "a": 1 }')

    assert ant_map.load_definition(json_file.as_posix()) == False
    assert ant_map


def test_style_conversion(ant_map):
    assert ant_map._convert_map_style("BOUNDED") == AntMap.BOUNDED
    assert ant_map._convert_map_style("UNBOUNDED") == AntMap.UNBOUNDED
    assert ant_map._convert_map_style("bounded") == AntMap.BOUNDED
    assert ant_map._convert_map_style("unbounded") == AntMap.UNBOUNDED
    with pytest.raises(ValueError):
        assert ant_map._convert_map_style("INFINITY")

def test_facing_conversion(ant_map):
    assert ant_map._convert_ant_facing("NORTH") == AntMap.NORTH
    assert ant_map._convert_ant_facing("EAST") == AntMap.EAST
    assert ant_map._convert_ant_facing("SOUTH") == AntMap.SOUTH
    assert ant_map._convert_ant_facing("WEST") == AntMap.WEST

    assert ant_map._convert_ant_facing("north") == AntMap.NORTH
    assert ant_map._convert_ant_facing("east") == AntMap.EAST
    assert ant_map._convert_ant_facing("south") == AntMap.SOUTH
    assert ant_map._convert_ant_facing("west") == AntMap.WEST

    with pytest.raises(ValueError):
        assert ant_map._convert_ant_facing("UP")

def test_map_load(ant_map_w_good_file):
    assert ant_map_w_good_file

    assert ant_map_w_good_file.name == "Basic Test Trail"
    assert ant_map_w_good_file.style == AntMap.BOUNDED
    assert ant_map_w_good_file.size  == (4,4)

    col = list(False for _ in range(4))
    map = list(col for _ in range(4))
    for x in range(4):
        map[x][2] = True
    assert ant_map_w_good_file.map  == map

    assert ant_map_w_good_file.start_location == [0,2]
    assert ant_map_w_good_file.end_location   == [3,2]

    assert ant_map_w_good_file.ant_facing == AntMap.EAST

def test_reset(ant_map_w_good_file):
    ant_map_w_good_file.reset()
    assert ant_map_w_good_file.ant_location == (0,2,AntMap.EAST)


def test__get_offset_pheremone(ant_map_w_good_file):
    ant_map = ant_map_w_good_file

    #facing NORTH ( (-1,-1), (0,-1), (1,-1) )
    assert ant_map._get_offset_pheremone( (0,2), (-1,-1)) == None
    assert ant_map._get_offset_pheremone( (0,2), (0, -1)) == False
    assert ant_map._get_offset_pheremone( (0,2), (1, -1)) == False

    #facing EAST ( (1,-1), (1,0), (1,1) )
    assert ant_map._get_offset_pheremone( (0,2), (1,-1)) == False
    assert ant_map._get_offset_pheremone( (0,2), (1, 0)) == True
    assert ant_map._get_offset_pheremone( (0,2), (1, 1)) == False

    #facing SOUTH ( (1,1), (0,1), (-1,1) )
    assert ant_map._get_offset_pheremone( (0,2), (1,1)) == False
    assert ant_map._get_offset_pheremone( (0,2), (0,1)) == False
    assert ant_map._get_offset_pheremone( (0,2), (-1,1)) == None

    #facing WEST ( (-1,1), (-1,0), (-1,-1) )
    assert ant_map._get_offset_pheremone( (0,2), (-1, 1)) == None
    assert ant_map._get_offset_pheremone( (0,2), (-1, 0)) == None
    assert ant_map._get_offset_pheremone( (0,2), (-1,-1)) == None

def test_get_ant_view_and_actions(ant_map_w_good_file):
    ant_map = ant_map_w_good_file
    ant_map.reset()

    assert ant_map.get_ant_view() == {
        "left":     False,
        "middle":   True,
        "right":    False,
    }

    assert ant_map.ant_advance() == {
        "loc": (1,2,AntMap.EAST),
        "view": {
            "left":     False,
            "middle":   True,
            "right":    False
        },
        "finished": False
    }

    assert ant_map.ant_rotate_ccw() == {
        "loc": (1,2,AntMap.NORTH),
        "view": {
            "left":     False,
            "middle":   False,
            "right":    False
        },
        "finished": False
    }

    assert ant_map.ant_advance() == {
        "loc": (1,1,AntMap.NORTH),
        "view": {
            "left":     False,
            "middle":   False,
            "right":    False
        },
        "finished": False
    }

    assert ant_map.ant_advance() == {
        "loc": (1,0,AntMap.NORTH),
        "view": {
            "left":     None,
            "middle":   None,
            "right":    None
        },
        "finished": False
    }

    assert ant_map.ant_rotate_cw() == {
        "loc": (1,0,AntMap.EAST),
        "view": {
            "left":     None,
            "middle":   False,
            "right":    False
        },
        "finished": False
    }


def test_get_ant_finished(ant_map_w_good_file):
    ant_map = ant_map_w_good_file
    ant_map.reset()

    ant_map.ant_advance()
    ant_map.ant_advance()

    assert ant_map.ant_advance() == {
        "loc": (3,2,AntMap.EAST),
        "view": {
            "left":     None,
            "middle":   None,
            "right":    None
        },
        "finished": True
    }

#def test_map_load(ant_map_w_bad_file):
#    assert ant_map_w_file

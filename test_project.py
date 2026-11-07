import json
from copy import deepcopy

import pytest

from project import (
    validate_time,
    calc_elapsed_time,
    get_travel_time,
    check_alibi,
    result,
    point_evaluation,
    analyse_case,
    generate_case,
)


@pytest.mark.parametrize("time", [
    "00:00", "09:30", "12:45", "23:59"
])
def test_validate_time_valid(time):
    assert validate_time(time) is True


@pytest.mark.parametrize("time", [
    "24:00", "12:60", "9:30", "hello", "12-30", ""
])
def test_validate_time_invalid(time):
    assert validate_time(time) is False


def test_calc_elapsed_time():
    assert calc_elapsed_time("10:00", "10:05") == 5
    assert calc_elapsed_time("09:30", "09:45") == 15
    assert calc_elapsed_time("11:50", "12:10") == 20
    assert calc_elapsed_time("12:00", "12:00") == 0


def test_calc_elapsed_time_invalid():
    with pytest.raises(ValueError):
        calc_elapsed_time("14:00", "13:55")

    with pytest.raises(ValueError):
        calc_elapsed_time("25:00", "26:00")


def test_check_alibi():
    assert check_alibi(10, 8) is True
    assert check_alibi(8, 8) is True
    assert check_alibi(5, 8) is False
    assert check_alibi(2, 4) is False


def test_get_travel_time():
    data = {
        "travel_times": [
            {"from": "Library", "to": "Gallery", "minutes": 4},
            {"from": "Archive", "to": "Reception", "minutes": 8}
        ]
    }

    assert get_travel_time(data, "Library", "Gallery") == 4
    assert get_travel_time(data, "Gallery", "Library") == 4
    assert get_travel_time(data, "Archive", "Reception") == 8


def test_get_travel_time_invalid():
    data = {
        "travel_times": [
            {"from": "Library", "to": "Gallery", "minutes": 4}
        ]
    }

    with pytest.raises(ValueError):
        get_travel_time(data, "Library", "Reception")


def test_result():
    assert result("guide", "guide") is True
    assert result("guide", "director") is False


def test_point_evaluation():
    assert point_evaluation(True) == 100
    assert point_evaluation(False) == 0


def make_sample_case():
    return {
        "travel_times": [
            {"from": "Library", "to": "Gallery", "minutes": 4},
            {"from": "Archive", "to": "Reception", "minutes": 8}
        ],
        "suspects": [
            {
                "name": "Director",
                "from": "Library",
                "to": "Gallery",
                "departure": "10:00",
                "arrival": "10:05"
            },
            {
                "name": "Guide",
                "from": "Archive",
                "to": "Reception",
                "departure": "11:20",
                "arrival": "11:25"
            }
        ]
    }


def test_analyse_case():
    case = make_sample_case()
    assert analyse_case(case) == "Guide"


def test_analyse_case_no_inconsistent():
    case = make_sample_case()
    case["suspects"][1]["arrival"] = "11:29"

    with pytest.raises(ValueError):
        analyse_case(case)


def test_analyse_case_multiple_inconsistent():
    case = make_sample_case()
    case["suspects"][0]["arrival"] = "10:02"

    with pytest.raises(ValueError):
        analyse_case(case)


def test_generate_case():
    with open("data/cases.json", "r") as file:
        data = json.load(file)

    original_data = deepcopy(data)
    names = {suspect["name"] for suspect in data["suspects"]}

    for _ in range(100):
        new_case = generate_case(data)

        assert isinstance(new_case, dict)
        assert len(new_case["suspects"]) == 4
        assert new_case["travel_times"] == data["travel_times"]

        new_names = {
            suspect["name"] for suspect in new_case["suspects"]
        }

        assert new_names == names
        assert analyse_case(new_case) in names

    assert data == original_data

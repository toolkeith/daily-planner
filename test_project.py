import pytest
from project import validate_time, sort_list, delete_task_by_id, validate_date
from datetime import datetime


def test_validate_time():
    assert validate_time("07:00") == "07:00"
    assert validate_time("00:00") == "00:00"
    assert validate_time("14:00") == "14:00"


def test_invalid_time():
    with pytest.raises(ValueError):
        validate_time("7:00")
    with pytest.raises(ValueError):
        validate_time("7am")
    with pytest.raises(ValueError):
        validate_time("7:00AM")
    with pytest.raises(ValueError):
        validate_time("12:60")
    with pytest.raises(ValueError):
        validate_time("5.30")


def test_sort_list():
    activity_lists = [
        ["07:00", "08:30", "Morning Exercise"],
        ["05:00", "05:30", "Pray & Meditate"],
        ["18:00", "19:30", "Dinner with the Family"],
    ]

    sorted_list = sort_list(activity_lists)

    assert sorted_list == [
        ["05:00", "05:30", "Pray & Meditate"],
        ["07:00", "08:30", "Morning Exercise"],
        ["18:00", "19:30", "Dinner with the Family"],
    ]


def test_delete_list_by_id():
    activity_lists = [
        ["05:00", "05:30", "Pray & Meditate"],
        ["07:00", "08:30", "Morning Exercise"],
        ["18:00", "19:30", "Dinner with the Family"],
    ]
    delete_task_by_id(activity_lists, 0)
    assert activity_lists == [
        ["07:00", "08:30", "Morning Exercise"],
        ["18:00", "19:30", "Dinner with the Family"],
    ]


def test_validate_date():
    date_format = "%Y-%m-%d"
    assert validate_date(date_format, "2030-12-25") == datetime(2030, 12, 25)
    assert validate_date(date_format, "2025-12-25") == datetime(2025, 12, 25)
    assert validate_date(date_format, "2050-12-25") == datetime(2050, 12, 25)


def test_invalid_date():
    date_format = "%Y-%m-%d"
    with pytest.raises(SystemExit):
        validate_date(date_format, "2023-25-08")
    with pytest.raises(SystemExit):
        validate_date(date_format, "August-01-2023")
    with pytest.raises(SystemExit):
        validate_date(date_format, "2023-08-01 12:00:00")
    with pytest.raises(SystemExit):
        validate_date(date_format, "2023-08-01")
    with pytest.raises(SystemExit):
        validate_date(date_format, "1900-01-01")

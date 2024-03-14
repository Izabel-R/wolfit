import pytest

from app.helpers import less_than_day, pretty_date
from freezegun import freeze_time
from datetime import datetime, timedelta

def test_just_now():
    assert less_than_day(5) == "just now"

def test_seconds_ago():
    assert less_than_day(30) == "30 seconds ago"

def test_a_minute_ago():
    assert less_than_day(70) == "a minute ago"

def test_minutes_ago():
    assert less_than_day(90) == "a minute ago"  
    assert less_than_day(120) == "2 minutes ago" 
    assert less_than_day(3599) == "59 minutes ago"


def test_an_hour_ago():
    assert less_than_day(3601) == "an hour ago"

def test_hours_ago():
    assert less_than_day(7201) == "2 hours ago"
    assert less_than_day(86399) == "23 hours ago"

@pytest.mark.parametrize("second_diff, expected", [
    (5, "just now"),
    (30, "30 seconds ago"),
    (70, "a minute ago"),
    (90, "a minute ago"),
    (3599, "59 minutes ago"),
    (3601, "an hour ago"),
    (7201, "2 hours ago"),
    (86399, "23 hours ago")
])
def test_various_times(second_diff, expected):
    assert less_than_day(second_diff) == expected

@freeze_time("2024-01-01")
def test_pretty_date_just_now():
    assert pretty_date() == "just now"

@freeze_time("2024-01-01")
def test_pretty_date_seconds():
    some_seconds_ago = datetime.utcnow() - timedelta(seconds=30)
    assert pretty_date(some_seconds_ago) == "30 seconds ago"

@freeze_time("2024-01-01")
def test_pretty_date_yesterday():
    yesterday = datetime.utcnow() - timedelta(days=1)
    assert pretty_date(yesterday) == "Yesterday"

@freeze_time("2024-01-01")
def test_pretty_date_days():
    few_days_ago = datetime.utcnow() - timedelta(days=3)
    assert pretty_date(few_days_ago) == "3 days ago"

@freeze_time("2024-01-01")
def test_pretty_date_weeks():
    few_weeks_ago = datetime.utcnow() - timedelta(days=14)
    assert pretty_date(few_weeks_ago) == "2 weeks ago"

@freeze_time("2024-01-01")
def test_pretty_date_months():
    few_months_ago = datetime.utcnow() - timedelta(days=60)
    assert pretty_date(few_months_ago) == "2 months ago"

@freeze_time("2024-01-01")
def test_pretty_date_years():
    few_years_ago = datetime.utcnow() - timedelta(days=365 * 2)
    assert pretty_date(few_years_ago) == "2 years ago"

@freeze_time("2024-01-01")
def test_pretty_date_future():
    future_date = datetime.utcnow() + timedelta(days=1)
    assert pretty_date(future_date) == "just about now"

@freeze_time("2024-01-01 12:00:00")
def test_pretty_date_with_int_timestamp():
    thirty_seconds_ago = datetime.utcnow() - timedelta(seconds=30)
    thirty_seconds_ago_timestamp = int(thirty_seconds_ago.timestamp())
    assert pretty_date(thirty_seconds_ago_timestamp) == "30 seconds ago"
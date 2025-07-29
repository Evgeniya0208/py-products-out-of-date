import datetime
from typing import Generator
from unittest import mock
from unittest.mock import patch

import pytest

from app.main import outdated_products


@pytest.fixture
def mock_today(request: pytest.FixtureRequest) -> (
        Generator)[mock.MagicMock, None, None]:
    real_date: datetime.date = request.param
    with patch("app.main.datetime.date") as mock_date:
        def date_side_effect(*args, **kwargs) -> datetime.date:
            if not args and not kwargs:
                return mock_date
            return datetime.date.__new__(datetime.date, *args, **kwargs)

        mock_date.today.return_value = real_date
        mock_date.side_effect = date_side_effect

        yield mock_date


products = [
    {
        "name": "salmon",
        "expiration_date": datetime.date(2022, 2, 10),
        "price": 600,
    },
    {
        "name": "chicken",
        "expiration_date": datetime.date(2022, 2, 2),
        "price": 120,
    },
    {
        "name": "duck",
        "expiration_date": datetime.date(2022, 2, 1),
        "price": 160,
    },
    {
        "name": "turkey",
        "expiration_date": datetime.date(2022, 1, 31),
        "price": 200,
    },
    {
        "name": "beef",
        "expiration_date": datetime.date(2022, 2, 5),
        "price": 300,
    },
]


@pytest.mark.parametrize(
    "mock_today,expected_products",
    [
        (datetime.date(2022, 2, 2), ["duck", "turkey"]),
        (datetime.date(2022, 2, 6), ["chicken", "duck", "turkey", "beef"]),
        (
            datetime.date(2022, 2, 11),
            ["salmon", "chicken", "duck", "turkey", "beef"],
        ),
        (datetime.date(2021, 2, 2), []),
    ],
    indirect=["mock_today"]
)
def test_outdated_products_one_expired(
    mock_today: mock.MagicMock,
    expected_products: list[str],
) -> None:
    assert outdated_products(products) == expected_products

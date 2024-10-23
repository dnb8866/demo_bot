import pytest

from utils.validators import validate_dates


@pytest.mark.parametrize(
    'args, expected_result',
    (
        (('1', 10, 2024), True),
        ((' 1,   2 , 3 ', 10, 2024), True),
        (('32', 11, 2024), False),
        (('0', 11, 2024), False),
        (('-1', 11, 2024), False),
        (('1, 4, 32', 10, 2024), False),
        (('', 10, 2024), False),
        ((1, 10, 2024), False),
        ((0, 10, 2024), False),
        ((-1, 10, 2024), False),
        (('3, qwe', 10, 2024), False)
    )
)
async def test_validate_dates(args, expected_result):
    assert await validate_dates(*args) == expected_result

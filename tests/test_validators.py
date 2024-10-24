import pytest

from utils.validators import validate_dates, validate_date


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


@pytest.mark.parametrize(
    'input_text, expected_result',
    (
        ('10.10.2024', True),
        ('1. 10. 2025', True),
        ('1 .  10  . 2020', True),
        ('10.1.2024', True),
        ('1. 12. 2025', True),
        ('1 .  02  . 2020', True),
        ('10.2024', False),
        ('10', False),
        ('32.10.2024', False),
        ('', False),
        ('10.10.2024, 11.10.2024', False),
        ('1, 10, 2025', False),
        ('10.11.2024.', False)
    )
)
async def test_validate_date(input_text, expected_result):
    assert await validate_date(input_text) == expected_result

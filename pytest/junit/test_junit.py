import pytest

from prime import is_prime

def sum(x, y) :
  return x + y

#def test_is_prime():
#    assert not is_prime(1)
#    assert is_prime(2)
#    assert is_prime(3)
#    assert not is_prime(4)
#    assert is_prime(5)
#    assert not is_prime(6)
#    assert is_prime(7)
#    assert not is_prime(8)
#    assert not is_prime(9)
#    assert not is_prime(10)

records = [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (6, False),
    (7, True),
    (8, False),
    (9, False),
    (10, False),
]

@pytest.mark.parametrize(
  ('number', 'expected'), records,
)

def test_is_prime(number, expected):
    assert is_prime(number) == expected

test_records = [
  (1, 1, 2),
  (2, 2, 4),
  (3, 4, 7),
]

@pytest.mark.parametrize( ('a', 'b', 'exp'), test_records)

def test_1(a, b, exp) :
  assert sum(a, b) == exp



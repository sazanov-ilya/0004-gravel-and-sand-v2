from unittest import TestCase

from app_first__gravel_and_sand.logic import operations


class LogicTastCase(TestCase):
    def test_plus(self):
        result = operations(6, 13, '+')
        self.assertEqual(19, result)

    def test_minus(self):
        result = operations(6, 13, '-')
        self.assertEqual(-7, result)

    def test_multiplay(self):
        result = operations(6, 13, '*')
        self.assertEqual(78, result)

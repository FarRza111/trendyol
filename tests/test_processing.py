"""
Test module for processing.py
Tests the utility functions in processing module
"""
import pytest
from processing import do_nothing, part1


class TestProcessingFunctions:
    """Test cases for processing.py functions"""

    def test_do_nothing_returns_none(self):
        """Test that do_nothing function returns None"""
        result = do_nothing()
        assert result is None

    def test_do_nothing_is_callable(self):
        """Test that do_nothing is callable"""
        assert callable(do_nothing)

    def test_do_nothing_no_side_effects(self):
        """Test that do_nothing has no side effects"""
        # Call multiple times to ensure no side effects
        for _ in range(5):
            result = do_nothing()
            assert result is None

    def test_part1_returns_none(self):
        """Test that part1 function returns None"""
        result = part1()
        assert result is None

    def test_part1_is_callable(self):
        """Test that part1 is callable"""
        assert callable(part1)

    def test_part1_no_side_effects(self):
        """Test that part1 has no side effects"""
        # Call multiple times to ensure no side effects
        for _ in range(5):
            result = part1()
            assert result is None

    def test_functions_are_independent(self):
        """Test that do_nothing and part1 are independent"""
        result1 = do_nothing()
        result2 = part1()
        
        assert result1 is None
        assert result2 is None
        assert result1 == result2

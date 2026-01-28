"""
Property-based tests for mathematical calculation accuracy.

This module contains property-based tests that validate the correctness
properties of the calculation functions, ensuring mathematical accuracy
across all possible input combinations.

**Property 4: Mathematical Calculation Accuracy**
**Validates: Requirements 4.2, 4.3**
"""

import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Union

import pytest
from hypothesis import given, strategies as st, assume, settings

# Add the src directory to the path to import the calculations module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mandi_setu.models.calculations import (
    calculate_total_amount,
    calculate_mandi_cess,
    calculate_final_amount,
    validate_calculation_consistency
)


# Custom strategies for generating test data
@st.composite
def positive_financial_values(draw, min_value=0.01, max_value=1000000.0):
    """Generate positive financial values suitable for trade calculations."""
    return draw(st.floats(
        min_value=min_value,
        max_value=max_value,
        allow_nan=False,
        allow_infinity=False,
        exclude_min=True  # Exclude exactly 0
    ))


@st.composite
def trade_calculation_inputs(draw):
    """Generate valid quantity and unit_price pairs for trade calculations."""
    quantity = draw(positive_financial_values(min_value=0.1, max_value=10000.0))
    unit_price = draw(positive_financial_values(min_value=0.1, max_value=10000.0))
    
    # Ensure the multiplication won't overflow or create precision issues
    # and that the result will be at least 0.01 after rounding
    product = quantity * unit_price
    assume(product >= 0.01)  # Ensure result won't round to 0
    assume(product <= 100000000.0)  # 100 million max to avoid overflow
    
    return quantity, unit_price


class TestCalculationAccuracyProperties:
    """Property-based tests for mathematical calculation accuracy."""
    
    @given(trade_calculation_inputs())
    @settings(max_examples=100, deadline=None)
    def test_total_amount_calculation_accuracy(self, inputs):
        """
        **Property 4: Mathematical Calculation Accuracy - Total Amount**
        **Validates: Requirements 4.2**
        
        For any valid quantity and unit_price combination, the system should
        calculate total amount correctly (quantity × unit_price) with proper
        rounding to 2 decimal places.
        """
        quantity, unit_price = inputs
        
        # Calculate total using the function
        result = calculate_total_amount(quantity, unit_price)
        
        # Calculate expected result using Decimal for precision
        expected = float(
            (Decimal(str(quantity)) * Decimal(str(unit_price)))
            .quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        )
        
        # Verify the calculation is accurate
        assert isinstance(result, float), "Result should be a float"
        assert result > 0, "Total amount should be positive"
        assert abs(result - expected) < 0.001, \
            f"Total amount {result} should equal {expected} (quantity {quantity} × unit_price {unit_price})"
        
        # Verify proper rounding (should have at most 2 decimal places)
        rounded_result = round(result, 2)
        assert abs(result - rounded_result) < 0.001, \
            f"Result {result} should be properly rounded to 2 decimal places"
    
    @given(positive_financial_values(min_value=0.1, max_value=1000000.0))
    @settings(max_examples=100, deadline=None)
    def test_mandi_cess_calculation_accuracy(self, total_amount):
        """
        **Property 4: Mathematical Calculation Accuracy - Mandi Cess**
        **Validates: Requirements 4.3**
        
        For any valid total amount, the system should calculate exactly 5%
        Mandi Cess with proper rounding to 2 decimal places.
        """
        # Calculate cess using the function
        result = calculate_mandi_cess(total_amount)
        
        # Calculate expected result using Decimal for precision
        expected = float(
            (Decimal(str(total_amount)) * Decimal('0.05'))
            .quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        )
        
        # Verify the calculation is accurate
        assert isinstance(result, float), "Result should be a float"
        assert result >= 0, "Mandi cess should be non-negative"
        assert abs(result - expected) < 0.001, \
            f"Mandi cess {result} should equal 5% of {total_amount} ({expected})"
        
        # The core property is that the function correctly applies the 5% rate and rounds properly
        # The actual percentage may vary due to rounding (e.g., 0.125 * 0.05 = 0.00625 -> 0.01 = 8%)
        # This is mathematically correct behavior given the 2-decimal-place constraint
        
        # Verify proper rounding (should have at most 2 decimal places)
        rounded_result = round(result, 2)
        assert abs(result - rounded_result) < 0.001, \
            f"Result {result} should be properly rounded to 2 decimal places"
    
    @given(trade_calculation_inputs())
    @settings(max_examples=100, deadline=None)
    def test_final_amount_calculation_consistency(self, inputs):
        """
        **Property 4: Mathematical Calculation Accuracy - Final Amount**
        **Validates: Requirements 4.2, 4.3**
        
        For any valid quantity and unit_price combination, the final amount
        calculation should be mathematically consistent across all components.
        """
        quantity, unit_price = inputs
        
        # Calculate using the combined function
        total_amount, mandi_cess, final_amount = calculate_final_amount(quantity, unit_price)
        
        # Verify individual calculations are correct
        expected_total = calculate_total_amount(quantity, unit_price)
        expected_cess = calculate_mandi_cess(total_amount)
        
        assert abs(total_amount - expected_total) < 0.001, \
            "Total amount should match individual calculation"
        assert abs(mandi_cess - expected_cess) < 0.001, \
            "Mandi cess should match individual calculation"
        
        # Verify final amount is sum of total and cess
        expected_final = total_amount + mandi_cess
        assert abs(final_amount - expected_final) < 0.001, \
            f"Final amount {final_amount} should equal total + cess ({expected_final})"
        
        # Verify all amounts are positive
        assert total_amount > 0, "Total amount should be positive"
        assert mandi_cess >= 0, "Mandi cess should be non-negative"
        assert final_amount >= total_amount, "Final amount should be greater than or equal to total amount"
    
    @given(trade_calculation_inputs())
    @settings(max_examples=100, deadline=None)
    def test_calculation_validation_consistency(self, inputs):
        """
        **Property 4: Mathematical Calculation Accuracy - Validation**
        **Validates: Requirements 4.2, 4.3**
        
        For any valid calculation inputs, the validation function should
        correctly identify mathematically consistent values.
        """
        quantity, unit_price = inputs
        
        # Calculate correct values
        total_amount = calculate_total_amount(quantity, unit_price)
        mandi_cess = calculate_mandi_cess(total_amount)
        
        # Validation should pass for correct values
        assert validate_calculation_consistency(quantity, unit_price, total_amount, mandi_cess), \
            "Validation should pass for correctly calculated values"
        
        # Validation should fail for incorrect total amount
        wrong_total = total_amount + 10.0  # Add significant error
        assert not validate_calculation_consistency(quantity, unit_price, wrong_total, mandi_cess), \
            "Validation should fail for incorrect total amount"
        
        # Validation should fail for incorrect cess
        wrong_cess = mandi_cess + 5.0  # Add significant error
        assert not validate_calculation_consistency(quantity, unit_price, total_amount, wrong_cess), \
            "Validation should fail for incorrect mandi cess"
    
    @given(st.floats(min_value=-1000.0, max_value=0.0))
    @settings(max_examples=50, deadline=None)
    def test_negative_quantity_rejection(self, negative_quantity):
        """
        **Property 4: Mathematical Calculation Accuracy - Input Validation**
        **Validates: Requirements 4.2**
        
        The calculation functions should reject negative or zero quantities
        with appropriate error messages.
        """
        unit_price = 10.0
        
        with pytest.raises(ValueError, match="Quantity must be positive"):
            calculate_total_amount(negative_quantity, unit_price)
    
    @given(st.floats(min_value=-1000.0, max_value=0.0))
    @settings(max_examples=50, deadline=None)
    def test_negative_unit_price_rejection(self, negative_price):
        """
        **Property 4: Mathematical Calculation Accuracy - Input Validation**
        **Validates: Requirements 4.2**
        
        The calculation functions should reject negative or zero unit prices
        with appropriate error messages.
        """
        quantity = 10.0
        
        with pytest.raises(ValueError, match="Unit price must be positive"):
            calculate_total_amount(quantity, negative_price)
    
    @given(st.floats(min_value=-1000.0, max_value=-0.01))
    @settings(max_examples=50, deadline=None)
    def test_negative_total_amount_rejection(self, negative_amount):
        """
        **Property 4: Mathematical Calculation Accuracy - Input Validation**
        **Validates: Requirements 4.3**
        
        The mandi cess calculation should reject negative total amounts
        with appropriate error messages.
        """
        with pytest.raises(ValueError, match="Total amount must be non-negative"):
            calculate_mandi_cess(negative_amount)
    
    @given(
        st.floats(min_value=0.01, max_value=1000.0, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0.01, max_value=1000.0, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_decimal_precision_consistency(self, quantity, unit_price):
        """
        **Property 4: Mathematical Calculation Accuracy - Decimal Precision**
        **Validates: Requirements 4.2, 4.3**
        
        Calculations should maintain consistent precision when using both
        float and Decimal inputs, ensuring no precision loss.
        """
        # Test with float inputs
        total_float = calculate_total_amount(quantity, unit_price)
        cess_float = calculate_mandi_cess(total_float)
        
        # Test with Decimal inputs
        total_decimal = calculate_total_amount(Decimal(str(quantity)), Decimal(str(unit_price)))
        cess_decimal = calculate_mandi_cess(Decimal(str(total_float)))
        
        # Results should be identical (within floating point tolerance)
        assert abs(total_float - total_decimal) < 0.001, \
            "Float and Decimal calculations should produce identical results for total amount"
        assert abs(cess_float - cess_decimal) < 0.001, \
            "Float and Decimal calculations should produce identical results for mandi cess"
    
    @given(trade_calculation_inputs())
    @settings(max_examples=100, deadline=None)
    def test_rounding_consistency(self, inputs):
        """
        **Property 4: Mathematical Calculation Accuracy - Rounding**
        **Validates: Requirements 4.2, 4.3**
        
        All calculations should use consistent rounding rules (ROUND_HALF_UP)
        and produce results with exactly 2 decimal places.
        """
        quantity, unit_price = inputs
        
        total_amount = calculate_total_amount(quantity, unit_price)
        mandi_cess = calculate_mandi_cess(total_amount)
        
        # Verify proper rounding (should have at most 2 decimal places)
        # Check by comparing with manually rounded values
        manually_rounded_total = round(total_amount, 2)
        manually_rounded_cess = round(mandi_cess, 2)
        
        assert abs(total_amount - manually_rounded_total) < 0.001, \
            f"Total amount {total_amount} should be properly rounded to 2 decimal places"
        assert abs(mandi_cess - manually_rounded_cess) < 0.001, \
            f"Mandi cess {mandi_cess} should be properly rounded to 2 decimal places"
        
        # Verify ROUND_HALF_UP behavior by comparing with manual calculation
        manual_total = float(
            (Decimal(str(quantity)) * Decimal(str(unit_price)))
            .quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        )
        manual_cess = float(
            (Decimal(str(total_amount)) * Decimal('0.05'))
            .quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        )
        
        assert abs(total_amount - manual_total) < 0.001, \
            "Total amount should use ROUND_HALF_UP rounding"
        assert abs(mandi_cess - manual_cess) < 0.001, \
            "Mandi cess should use ROUND_HALF_UP rounding"


class TestCalculationEdgeCases:
    """Edge case tests for calculation functions."""
    
    def test_minimum_values(self):
        """Test calculations with minimum valid values."""
        min_quantity = 0.01
        min_price = 0.01
        
        total = calculate_total_amount(min_quantity, min_price)
        cess = calculate_mandi_cess(total)
        
        assert total == 0.0, "Minimum values should produce 0.00 total"
        assert cess == 0.0, "Minimum total should produce 0.00 cess"
    
    def test_large_values(self):
        """Test calculations with large values."""
        large_quantity = 10000.0
        large_price = 10000.0
        
        total = calculate_total_amount(large_quantity, large_price)
        cess = calculate_mandi_cess(total)
        
        assert total == 100000000.0, "Large values should calculate correctly"
        assert cess == 5000000.0, "Large cess should calculate correctly"
    
    def test_zero_total_amount_cess(self):
        """Test mandi cess calculation with zero total amount."""
        cess = calculate_mandi_cess(0.0)
        assert cess == 0.0, "Zero total amount should produce zero cess"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
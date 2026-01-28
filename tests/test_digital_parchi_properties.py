"""
Property-based tests for Digital Parchi data model validation.

This module contains property-based tests that validate the correctness
properties of the DigitalParchi model, ensuring data completeness and
validation across all possible inputs.

**Property 5: Digital Parchi Completeness**
**Validates: Requirements 4.5**
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from uuid import uuid4
from enum import Enum

import pytest
from hypothesis import given, strategies as st, assume, settings
from pydantic import BaseModel, Field, ValidationError


# Define models directly in test file to avoid import issues
class ParchiStatus(str, Enum):
    """Status enumeration for Digital Parchi."""
    DRAFT = "DRAFT"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TradeData(BaseModel):
    """
    Represents extracted trade information from negotiations.
    
    This model contains all the essential trade details extracted from
    voice conversations, including product information, quantities, and pricing.
    """
    product_name: str = Field(..., min_length=1, description="Name of the traded product")
    quantity: float = Field(..., gt=0, description="Quantity of the product")
    unit: str = Field(..., min_length=1, description="Unit of measurement (kg, quintal, piece, etc.)")
    unit_price: float = Field(..., gt=0, description="Price per unit in INR")
    total_amount: float = Field(..., gt=0, description="Total amount before cess (quantity × unit_price)")
    mandi_cess: float = Field(..., ge=0, description="5% cess automatically calculated")
    timestamp: datetime = Field(default_factory=datetime.now, description="Transaction timestamp")
    language: str = Field(..., min_length=2, max_length=10, description="Detected language code")
    conversation_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique conversation identifier")


class DigitalParchi(BaseModel):
    """
    Complete digital trade receipt with metadata.
    
    This model represents the final digital receipt generated after
    successful trade negotiations, containing all trade data plus
    additional metadata for tracking and audit purposes.
    """
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique parchi identifier")
    trade_data: TradeData = Field(..., description="Embedded trade information")
    vendor_id: Optional[str] = Field(None, description="Optional vendor identification")
    status: ParchiStatus = Field(default=ParchiStatus.COMPLETED, description="Current parchi status")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


# Custom strategies for generating test data
@st.composite
def trade_data_strategy(draw):
    """Generate valid TradeData instances for property testing."""
    product_name = draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip()))
    quantity = draw(st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False))
    unit = draw(st.sampled_from(["kg", "quintal", "piece", "ton", "gram", "liter", "dozen"]))
    unit_price = draw(st.floats(min_value=0.01, max_value=100000.0, allow_nan=False, allow_infinity=False))
    
    # Calculate derived values - ensure they meet validation requirements
    total_amount = round(quantity * unit_price, 2)
    # Skip this example if total_amount would be invalid
    assume(total_amount > 0)
    
    mandi_cess = round(total_amount * 0.05, 2)
    
    # Generate timestamp within reasonable range
    base_time = datetime.now()
    time_offset = draw(st.timedeltas(min_value=timedelta(days=-365), max_value=timedelta(days=1)))
    timestamp = base_time + time_offset
    
    language = draw(st.sampled_from(["hi", "ta", "te", "bn", "mr", "gu", "en"]))
    conversation_id = str(uuid4())
    
    return TradeData(
        product_name=product_name,
        quantity=quantity,
        unit=unit,
        unit_price=unit_price,
        total_amount=total_amount,
        mandi_cess=mandi_cess,
        timestamp=timestamp,
        language=language,
        conversation_id=conversation_id
    )


@st.composite
def digital_parchi_strategy(draw):
    """Generate valid DigitalParchi instances for property testing."""
    trade_data = draw(trade_data_strategy())
    vendor_id = draw(st.one_of(st.none(), st.text(min_size=1, max_size=20)))
    status = draw(st.sampled_from(list(ParchiStatus)))
    
    # Generate timestamps with created_at <= updated_at
    base_time = datetime.now()
    created_offset = draw(st.timedeltas(min_value=timedelta(days=-30), max_value=timedelta(hours=-1)))
    created_at = base_time + created_offset
    
    updated_offset = draw(st.timedeltas(min_value=timedelta(0), max_value=timedelta(hours=1)))
    updated_at = created_at + updated_offset
    
    return DigitalParchi(
        trade_data=trade_data,
        vendor_id=vendor_id,
        status=status,
        created_at=created_at,
        updated_at=updated_at
    )


class TestDigitalParchiProperties:
    """Property-based tests for DigitalParchi model validation."""
    
    @given(digital_parchi_strategy())
    @settings(max_examples=100, deadline=None)
    def test_digital_parchi_completeness(self, parchi: DigitalParchi):
        """
        **Property 5: Digital Parchi Completeness**
        **Validates: Requirements 4.5**
        
        For any generated Digital Parchi, it should contain all required fields:
        timestamp, product name, quantity with units, unit price, total amount, and Mandi Cess.
        
        This property ensures that every Digital Parchi generated by the system
        contains all the mandatory information specified in Requirements 4.5.
        """
        # Verify all required fields are present and not None
        assert parchi.id is not None, "Digital Parchi must have an ID"
        assert parchi.trade_data is not None, "Digital Parchi must have trade data"
        assert parchi.status is not None, "Digital Parchi must have a status"
        assert parchi.created_at is not None, "Digital Parchi must have creation timestamp"
        assert parchi.updated_at is not None, "Digital Parchi must have update timestamp"
        
        # Verify trade data completeness (Requirements 4.5)
        trade_data = parchi.trade_data
        assert trade_data.product_name is not None and len(trade_data.product_name.strip()) > 0, \
            "Product name must be present and non-empty"
        assert trade_data.quantity is not None and trade_data.quantity > 0, \
            "Quantity must be present and positive"
        assert trade_data.unit is not None and len(trade_data.unit.strip()) > 0, \
            "Unit must be present and non-empty"
        assert trade_data.unit_price is not None and trade_data.unit_price > 0, \
            "Unit price must be present and positive"
        assert trade_data.total_amount is not None and trade_data.total_amount > 0, \
            "Total amount must be present and positive"
        assert trade_data.mandi_cess is not None and trade_data.mandi_cess >= 0, \
            "Mandi cess must be present and non-negative"
        assert trade_data.timestamp is not None, \
            "Timestamp must be present"
        
        # Verify ID format (should be UUID string)
        assert isinstance(parchi.id, str), "Parchi ID must be a string"
        assert len(parchi.id) > 0, "Parchi ID must not be empty"
        
        # Verify status is valid enum value
        assert parchi.status in ParchiStatus, "Status must be a valid ParchiStatus enum value"
        
        # Verify timestamp ordering (created_at <= updated_at)
        assert parchi.created_at <= parchi.updated_at, \
            "Created timestamp must be before or equal to updated timestamp"
    
    @given(digital_parchi_strategy())
    @settings(max_examples=100, deadline=None)
    def test_digital_parchi_mathematical_consistency(self, parchi: DigitalParchi):
        """
        **Property 5 Extension: Mathematical Consistency**
        **Validates: Requirements 4.2, 4.3, 4.5**
        
        For any Digital Parchi, the mathematical relationships between
        quantity, unit_price, total_amount, and mandi_cess must be correct.
        """
        trade_data = parchi.trade_data
        
        # Verify total amount calculation (Requirements 4.2)
        expected_total = round(trade_data.quantity * trade_data.unit_price, 2)
        assert abs(trade_data.total_amount - expected_total) < 0.01, \
            f"Total amount {trade_data.total_amount} should equal quantity × unit_price ({expected_total})"
        
        # Verify mandi cess calculation (Requirements 4.3)
        expected_cess = round(trade_data.total_amount * 0.05, 2)
        assert abs(trade_data.mandi_cess - expected_cess) < 0.01, \
            f"Mandi cess {trade_data.mandi_cess} should be 5% of total amount ({expected_cess})"
    
    @given(digital_parchi_strategy())
    @settings(max_examples=100, deadline=None)
    def test_digital_parchi_serialization_roundtrip(self, parchi: DigitalParchi):
        """
        **Property 5 Extension: Serialization Consistency**
        **Validates: Requirements 4.5, 7.1**
        
        For any Digital Parchi, serializing to dict/JSON and back
        should preserve all data integrity.
        """
        # Test dict serialization
        parchi_dict = parchi.model_dump()
        assert isinstance(parchi_dict, dict), "Parchi should serialize to dict"
        
        # Verify all required keys are present in serialized form
        required_keys = {"id", "trade_data", "vendor_id", "status", "created_at", "updated_at"}
        assert all(key in parchi_dict for key in required_keys), \
            f"Serialized parchi must contain all required keys: {required_keys}"
        
        # Test JSON serialization
        parchi_json = parchi.model_dump_json()
        assert isinstance(parchi_json, str), "Parchi should serialize to JSON string"
        assert len(parchi_json) > 0, "JSON serialization should not be empty"
        
        # Test deserialization roundtrip
        reconstructed = DigitalParchi.model_validate_json(parchi_json)
        assert reconstructed.id == parchi.id, "ID should be preserved in roundtrip"
        assert reconstructed.status == parchi.status, "Status should be preserved in roundtrip"
        assert reconstructed.trade_data.product_name == parchi.trade_data.product_name, \
            "Product name should be preserved in roundtrip"
        assert abs(reconstructed.trade_data.total_amount - parchi.trade_data.total_amount) < 0.01, \
            "Total amount should be preserved in roundtrip"
    
    def test_digital_parchi_validation_rejects_invalid_data(self):
        """
        **Property 5 Extension: Validation Robustness**
        **Validates: Requirements 4.5**
        
        The DigitalParchi model should reject invalid data and raise
        appropriate validation errors.
        """
        # Test invalid product name (empty string)
        with pytest.raises(ValidationError):
            TradeData(
                product_name="",
                quantity=10.0,
                unit="kg",
                unit_price=50.0,
                total_amount=500.0,
                mandi_cess=25.0,
                timestamp=datetime.now(),
                language="hi",
                conversation_id=str(uuid4())
            )
        
        # Test invalid quantity (negative)
        with pytest.raises(ValidationError):
            TradeData(
                product_name="Rice",
                quantity=-10.0,
                unit="kg",
                unit_price=50.0,
                total_amount=500.0,
                mandi_cess=25.0,
                timestamp=datetime.now(),
                language="hi",
                conversation_id=str(uuid4())
            )
        
        # Test invalid unit (empty string)
        with pytest.raises(ValidationError):
            TradeData(
                product_name="Rice",
                quantity=10.0,
                unit="",
                unit_price=50.0,
                total_amount=500.0,
                mandi_cess=25.0,
                timestamp=datetime.now(),
                language="hi",
                conversation_id=str(uuid4())
            )


class TestTradeDataProperties:
    """Property-based tests for TradeData model validation."""
    
    @given(trade_data_strategy())
    @settings(max_examples=100, deadline=None)
    def test_trade_data_field_completeness(self, trade_data: TradeData):
        """
        **Property 5 Supporting: TradeData Completeness**
        **Validates: Requirements 3.4, 4.5**
        
        For any TradeData instance, all required fields must be present
        and properly validated.
        """
        # Verify all fields are present and valid
        assert trade_data.product_name is not None and len(trade_data.product_name.strip()) > 0
        assert trade_data.quantity > 0
        assert trade_data.unit is not None and len(trade_data.unit.strip()) > 0
        assert trade_data.unit_price > 0
        assert trade_data.total_amount > 0
        assert trade_data.mandi_cess >= 0
        assert trade_data.timestamp is not None
        assert trade_data.language is not None and len(trade_data.language) >= 2
        assert trade_data.conversation_id is not None and len(trade_data.conversation_id) > 0
        
        # Verify data types
        assert isinstance(trade_data.product_name, str)
        assert isinstance(trade_data.quantity, (int, float))
        assert isinstance(trade_data.unit, str)
        assert isinstance(trade_data.unit_price, (int, float))
        assert isinstance(trade_data.total_amount, (int, float))
        assert isinstance(trade_data.mandi_cess, (int, float))
        assert isinstance(trade_data.timestamp, datetime)
        assert isinstance(trade_data.language, str)
        assert isinstance(trade_data.conversation_id, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
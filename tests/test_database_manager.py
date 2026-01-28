"""
Tests for DatabaseManager implementations.

This module contains unit tests for both SQLite and DynamoDB
database manager implementations.
"""

import pytest
import asyncio
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path

from src.mandi_setu.database import (
    SQLiteManager,
    DatabaseManager,
    DatabaseError,
    ValidationError,
    create_sqlite_manager,
    initialize_database
)
from src.mandi_setu.models.core import DigitalParchi, TradeData, ParchiStatus


class TestSQLiteManager:
    """Test cases for SQLite database manager."""
    
    @pytest.fixture
    async def temp_db_manager(self):
        """Create a temporary SQLite database manager for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "test_mandi_setu.db")
            manager = SQLiteManager(db_path=db_path)
            await manager.initialize()
            yield manager
            await manager.close()
    
    @pytest.fixture
    def sample_trade_data(self):
        """Create sample trade data for testing."""
        return TradeData(
            product_name="Wheat",
            quantity=100.0,
            unit="kg",
            unit_price=25.50,
            total_amount=2550.0,
            mandi_cess=127.50,
            language="hi",
            conversation_id="test-conv-123"
        )
    
    @pytest.fixture
    def sample_parchi(self, sample_trade_data):
        """Create sample Digital Parchi for testing."""
        return DigitalParchi(
            trade_data=sample_trade_data,
            vendor_id="vendor-123",
            status=ParchiStatus.COMPLETED
        )
    
    async def test_initialize_creates_database(self):
        """Test that initialization creates the database file and tables."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "test_init.db")
            manager = SQLiteManager(db_path=db_path)
            
            # Database file should not exist initially
            assert not Path(db_path).exists()
            
            # Initialize should create the database
            await manager.initialize()
            assert Path(db_path).exists()
            
            # Should be able to perform health check
            health = await manager.health_check()
            assert health['status'] == 'healthy'
            assert health['database_type'] == 'sqlite'
            
            await manager.close()
    
    async def test_save_and_retrieve_parchi(self, temp_db_manager, sample_parchi):
        """Test saving and retrieving a Digital Parchi."""
        # Save parchi
        saved_id = await temp_db_manager.save_parchi(sample_parchi)
        assert saved_id == sample_parchi.id
        
        # Retrieve parchi
        retrieved_parchi = await temp_db_manager.get_parchi(sample_parchi.id)
        assert retrieved_parchi is not None
        assert retrieved_parchi.id == sample_parchi.id
        assert retrieved_parchi.trade_data.product_name == sample_parchi.trade_data.product_name
        assert retrieved_parchi.trade_data.quantity == sample_parchi.trade_data.quantity
        assert retrieved_parchi.status == sample_parchi.status
    
    async def test_get_nonexistent_parchi(self, temp_db_manager):
        """Test retrieving a non-existent parchi returns None."""
        result = await temp_db_manager.get_parchi("nonexistent-id")
        assert result is None
    
    async def test_list_parchis(self, temp_db_manager, sample_trade_data):
        """Test listing parchis with pagination."""
        # Create multiple parchis
        parchis = []
        for i in range(5):
            trade_data = TradeData(
                product_name=f"Product-{i}",
                quantity=float(i + 1),
                unit="kg",
                unit_price=10.0,
                total_amount=float((i + 1) * 10),
                mandi_cess=float((i + 1) * 0.5),
                language="hi",
                conversation_id=f"conv-{i}"
            )
            parchi = DigitalParchi(trade_data=trade_data)
            parchis.append(parchi)
            await temp_db_manager.save_parchi(parchi)
        
        # List all parchis
        all_parchis = await temp_db_manager.list_parchis(limit=10)
        assert len(all_parchis) == 5
        
        # Test pagination
        first_page = await temp_db_manager.list_parchis(limit=2, offset=0)
        assert len(first_page) == 2
        
        second_page = await temp_db_manager.list_parchis(limit=2, offset=2)
        assert len(second_page) == 2
        
        # Verify ordering (most recent first)
        assert all_parchis[0].created_at >= all_parchis[1].created_at
    
    async def test_list_parchis_with_date_filter(self, temp_db_manager, sample_trade_data):
        """Test listing parchis with date filtering."""
        # Create parchi with specific date
        old_date = datetime.now() - timedelta(days=2)
        recent_date = datetime.now() - timedelta(hours=1)
        
        # Create old parchi
        old_parchi = DigitalParchi(trade_data=sample_trade_data)
        old_parchi.created_at = old_date
        await temp_db_manager.save_parchi(old_parchi)
        
        # Create recent parchi
        recent_parchi = DigitalParchi(trade_data=sample_trade_data)
        recent_parchi.created_at = recent_date
        await temp_db_manager.save_parchi(recent_parchi)
        
        # Filter by start date
        recent_parchis = await temp_db_manager.list_parchis(
            start_date=datetime.now() - timedelta(days=1)
        )
        assert len(recent_parchis) == 1
        assert recent_parchis[0].id == recent_parchi.id
    
    async def test_update_parchi(self, temp_db_manager, sample_parchi):
        """Test updating a parchi."""
        # Save original parchi
        await temp_db_manager.save_parchi(sample_parchi)
        
        # Update parchi
        updates = {
            'status': ParchiStatus.CANCELLED,
            'vendor_id': 'new-vendor-456'
        }
        
        success = await temp_db_manager.update_parchi(sample_parchi.id, updates)
        assert success is True
        
        # Verify updates
        updated_parchi = await temp_db_manager.get_parchi(sample_parchi.id)
        assert updated_parchi.status == ParchiStatus.CANCELLED
        assert updated_parchi.vendor_id == 'new-vendor-456'
        assert updated_parchi.updated_at > sample_parchi.updated_at
    
    async def test_update_nonexistent_parchi(self, temp_db_manager):
        """Test updating a non-existent parchi returns False."""
        success = await temp_db_manager.update_parchi("nonexistent-id", {'status': ParchiStatus.CANCELLED})
        assert success is False
    
    async def test_delete_parchi(self, temp_db_manager, sample_parchi):
        """Test deleting a parchi."""
        # Save parchi
        await temp_db_manager.save_parchi(sample_parchi)
        
        # Verify it exists
        retrieved = await temp_db_manager.get_parchi(sample_parchi.id)
        assert retrieved is not None
        
        # Delete parchi
        success = await temp_db_manager.delete_parchi(sample_parchi.id)
        assert success is True
        
        # Verify it's gone
        deleted = await temp_db_manager.get_parchi(sample_parchi.id)
        assert deleted is None
    
    async def test_delete_nonexistent_parchi(self, temp_db_manager):
        """Test deleting a non-existent parchi returns False."""
        success = await temp_db_manager.delete_parchi("nonexistent-id")
        assert success is False
    
    async def test_count_parchis(self, temp_db_manager, sample_trade_data):
        """Test counting parchis."""
        # Initially should be 0
        count = await temp_db_manager.count_parchis()
        assert count == 0
        
        # Add some parchis
        for i in range(3):
            trade_data = TradeData(
                product_name=f"Product-{i}",
                quantity=float(i + 1),
                unit="kg",
                unit_price=10.0,
                total_amount=float((i + 1) * 10),
                mandi_cess=float((i + 1) * 0.5),
                language="hi",
                conversation_id=f"conv-{i}"
            )
            parchi = DigitalParchi(trade_data=trade_data)
            await temp_db_manager.save_parchi(parchi)
        
        # Count should be 3
        count = await temp_db_manager.count_parchis()
        assert count == 3
    
    async def test_health_check(self, temp_db_manager):
        """Test database health check."""
        health = await temp_db_manager.health_check()
        
        assert health['status'] == 'healthy'
        assert health['database_type'] == 'sqlite'
        assert 'database_path' in health
        assert 'total_parchis' in health
        assert 'database_size_bytes' in health
        assert health['connection_active'] is True


class TestDatabaseFactory:
    """Test cases for database factory functions."""
    
    async def test_create_sqlite_manager(self):
        """Test creating SQLite manager through factory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "factory_test.db")
            manager = create_sqlite_manager(db_path)
            
            assert isinstance(manager, SQLiteManager)
            
            # Initialize and test
            await initialize_database(manager)
            health = await manager.health_check()
            assert health['status'] == 'healthy'
            
            await manager.close()


# Integration test to verify the complete flow
async def test_complete_database_workflow():
    """Test complete database workflow from creation to cleanup."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "workflow_test.db")
        
        # Create and initialize manager
        manager = SQLiteManager(db_path=db_path)
        await manager.initialize()
        
        try:
            # Create sample data
            trade_data = TradeData(
                product_name="Rice",
                quantity=50.0,
                unit="kg",
                unit_price=30.0,
                total_amount=1500.0,
                mandi_cess=75.0,
                language="hi",
                conversation_id="workflow-test"
            )
            
            parchi = DigitalParchi(
                trade_data=trade_data,
                vendor_id="workflow-vendor",
                status=ParchiStatus.COMPLETED
            )
            
            # Save parchi
            parchi_id = await manager.save_parchi(parchi)
            assert parchi_id == parchi.id
            
            # Retrieve and verify
            retrieved = await manager.get_parchi(parchi_id)
            assert retrieved is not None
            assert retrieved.trade_data.product_name == "Rice"
            
            # List parchis
            parchis_list = await manager.list_parchis()
            assert len(parchis_list) == 1
            
            # Count parchis
            count = await manager.count_parchis()
            assert count == 1
            
            # Update parchi
            await manager.update_parchi(parchi_id, {'status': ParchiStatus.CANCELLED})
            updated = await manager.get_parchi(parchi_id)
            assert updated.status == ParchiStatus.CANCELLED
            
            # Health check
            health = await manager.health_check()
            assert health['status'] == 'healthy'
            
        finally:
            await manager.close()


if __name__ == "__main__":
    # Run the integration test
    asyncio.run(test_complete_database_workflow())
    print("Database workflow test completed successfully!")
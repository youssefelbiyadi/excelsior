from typing import Optional, List
import uuid
from datetime import datetime
import logging

@dataclass
class Resource:
    id: uuid.UUID
    name: str
    creation_date: datetime
    update_date: Optional[datetime] = None
    deletion_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)

class ResourceManager(LoggingMixin):
    def __init__(self, logger: Optional[logging.Logger] = None):
        super().__init__(logger)
        self.resources = {}

    def create_resource(self, name: str, tags: Optional[List[str]] = None) -> Resource:
        resource_id = uuid.uuid4()
        resource = Resource(
            id=resource_id,
            name=name,
            creation_date=datetime.now(),
            tags=tags or []
        )
        self.resources[resource_id] = resource
        self._log_internal_action("Created new resource", resource_id)
        return resource

    def get_resource(self, resource_id: uuid.UUID) -> Resource:
        self._log_internal_action("Fetching resource", resource_id)
        if resource_id in self.resources:
            return self.resources[resource_id]
        raise KeyError(f"Resource with ID {resource_id} not found")

    def update_resource(self, resource_id: uuid.UUID, name: Optional[str] = None, tags: Optional[List[str]] = None) -> Resource:
        self._log_internal_action("Updating resource", resource_id)
        if resource_id in self.resources:
            resource = self.resources[resource_id]
            if name:
                resource.name = name
            if tags is not None:
                resource.tags = tags
            resource.update_date = datetime.now()
            return resource
        raise KeyError(f"Resource with ID {resource_id} not found")

    def delete_resource(self, resource_id: uuid.UUID) -> Resource:
        self._log_internal_action("Deleting resource", resource_id)
        if resource_id in self.resources:
            resource = self.resources[resource_id]
            resource.deletion_date = datetime.now()
            return resource
        raise KeyError(f"Resource with ID {resource_id} not found")

    @no_logging
    def cleanup_resources(self):
        """A method to clean up all resources marked as deleted. No logging should occur."""
        to_remove = [rid for rid, res in self.resources.items() if res.deletion_date is not None]
        for rid in to_remove:
            del self.resources[rid]

    def _log_internal_action(self, action: str, resource_id: uuid.UUID):
        """Private method that logs internal actions, but should not be logged itself."""
        print(f"Internal Log: {action} for Resource ID {resource_id}")



import pytest
import logging
import uuid
from unittest.mock import MagicMock, patch
from datetime import datetime
from your_module import ResourceManager, Resource

@pytest.fixture
def mock_logger():
    with patch.object(ResourceManager, 'get_logger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        yield mock_logger

@pytest.fixture
def resource_manager():
    return ResourceManager()

def test_create_resource_logged(mock_logger, resource_manager):
    resource = resource_manager.create_resource(name="TestResource", tags=["tag1", "tag2"])
    assert resource.name == "TestResource"
    assert resource.tags == ["tag1", "tag2"]
    assert isinstance(resource.id, uuid.UUID)
    mock_logger.info.assert_any_call("Calling method create_resource with args: ('TestResource',), kwargs: {'tags': ['tag1', 'tag2']}")
    mock_logger.info.assert_any_call(f"Method create_resource returned: {resource}")

def test_get_resource_logged(mock_logger, resource_manager):
    resource = resource_manager.create_resource(name="TestResource")
    retrieved_resource = resource_manager.get_resource(resource.id)
    assert retrieved_resource == resource
    mock_logger.info.assert_any_call(f"Calling method get_resource with args: ({resource.id},), kwargs: {{}}")
    mock_logger.info.assert_any_call(f"Method get_resource returned: {retrieved_resource}")

def test_update_resource_logged(mock_logger, resource_manager):
    resource = resource_manager.create_resource(name="TestResource")
    updated_resource = resource_manager.update_resource(resource.id, name="UpdatedResource")
    assert updated_resource.name == "UpdatedResource"
    assert updated_resource.update_date is not None
    mock_logger.info.assert_any_call(f"Calling method update_resource with args: ({resource.id},), kwargs: {{'name': 'UpdatedResource'}}")
    mock_logger.info.assert_any_call(f"Method update_resource returned: {updated_resource}")

def test_delete_resource_logged(mock_logger, resource_manager):
    resource = resource_manager.create_resource(name="TestResource")
    deleted_resource = resource_manager.delete_resource(resource.id)
    assert deleted_resource.deletion_date is not None
    mock_logger.info.assert_any_call(f"Calling method delete_resource with args: ({resource.id},), kwargs: {{}}")
    mock_logger.info.assert_any_call(f"Method delete_resource returned: {deleted_resource}")

def test_cleanup_resources_not_logged(mock_logger, resource_manager):
    resource_manager.create_resource(name="TestResource")
    resource_manager.cleanup_resources()
    mock_logger.info.assert_not_called()

def test_private_methods_not_logged(mock_logger, resource_manager):
    resource = resource_manager.create_resource(name="TestResource")
    resource_manager._log_internal_action("Testing private log", resource.id)
    mock_logger.info.assert_any_call("Calling method create_resource with args: ('TestResource',), kwargs: {'tags': None}")
    mock_logger.info.assert_any_call(f"Method create_resource returned: {resource}")
    mock_logger.info.assert_not_called_with("Internal Log: Testing private log")

def test_get_nonexistent_resource_raises_error(mock_logger, resource_manager):
    non_existent_id = uuid.uuid4()
    with pytest.raises(KeyError, match=f"Resource with ID {non_existent_id} not found"):
        resource_manager.get_resource(non_existent_id)
    mock_logger.info.assert_any_call(f"Calling method get_resource with args: ({non_existent_id},), kwargs: {{}}")
    mock_logger.error.assert_called_once()

def test_update_nonexistent_resource_raises_error(mock_logger, resource_manager):
    non_existent_id = uuid.uuid4()
    with pytest.raises(KeyError, match=f"Resource with ID {non_existent_id} not found"):
        resource_manager.update_resource(non_existent_id, name="NewName")
    mock_logger.info.assert_any_call(f"Calling method update_resource with args: ({non_existent_id},), kwargs: {{'name': 'NewName'}}")
    mock_logger.error.assert_called_once()

def test_delete_nonexistent_resource_raises_error(mock_logger, resource_manager):
    non_existent_id = uuid.uuid4()
    with pytest.raises(KeyError, match=f"Resource with ID {non_existent_id} not found"):
        resource_manager.delete_resource(non_existent_id)
    mock_logger.info.assert_any_call(f"Calling method delete_resource with args: ({non_existent_id},), kwargs: {{}}")
    mock_logger.error.assert_called_once()

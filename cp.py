from enum import Enum
from time import sleep


class OperationState(Enum):
    PENDING = "PENDING"
    SUCCESS =  "SUCCESS"
    FAILED = "FAILED"

class OperationStateManager:
    def __init__(self, model, service, state_attr):
        self.model = model
        self.service = service
        self.state_attr = state_attr

    def __enter__(self):
        print(f"Updating {self.model.__class__.__name__} attr {self.state_attr} to {OperationState.PENDING}")
        setattr(self.model, self.state_attr, OperationState.PENDING)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Updating {self.model.__class__.__name__} attr {self.state_attr} to {OperationState.FAILED}")
            setattr(self.model, self.state_attr, OperationState.FAILED)
            # * SHOULD I RAISE EXCEPTION HERE: I think no

        else:
            print(f"Updating {self.model.__class__.__name__} attr {self.state_attr} to {OperationState.SUCCESS}")
            setattr(self.model, self.state_attr, OperationState.SUCCESS)

# Example of SomeModel
class SomeModel:
    def __init__(self):
        self.state = None

# Example of SomeService
class SomeService:
    def perform_operation(self):
        print("Performing some operation...")
        raise Exception("MY Exception")
        return "Operation result"

# Example of usage
if __name__ == "__main__":
    model = SomeModel()
    service = SomeService()

    def perform_action():
        with OperationStateManager(model, service, "state") as state_manager:
            try:
                print(model.state)
                service.perform_operation()
            except Exception as e:
                print(model.state)
                raise Exception(f"An exception occurred: {e}")
            
            print(f"Not modifiying state: {model.state}")
        
        # Caution: Should have the right indentation
        print(f"Modifying state => Final state: {model.state}")
        return model

perform_action()

from abc import ABC 

class DatabaseRepository(ABC):
    def execute(self, query: str):
        """Execute a SQL query and return the result."""
        pass

    def get_schema(self):
        """Return the schema of the database."""
        pass 
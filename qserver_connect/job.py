from .data_types import AllData


class Job:
    """
    An object that holds job data. It's meant to be used with adapters
    """

    def __init__(self, data: AllData):
        """
        Store provided data.
        """

        self._data = data

    @property
    def data(self) -> AllData:
        """Getter for data."""
        return self._data

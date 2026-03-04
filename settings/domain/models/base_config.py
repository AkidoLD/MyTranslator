import uuid


class BaseConfig :
    def __init__(self, title : str, group_id : str = None, description : str | None = None):
        self.title = title
        self.description = description
        self.group_id = group_id
        self._id : str = str(uuid.uuid4())
        self._group_id : str = group_id

    @property
    def group_id(self):
        return self._group_id

    @group_id.setter
    def group_id(self, value : str):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"description may be none or string, got type {type(value).__name__}")
        #
        if isinstance(value, str) and not value.strip():
            raise ValueError("group_id can't be empty")
        #
        self._group_id = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value : str | None):
        if value is not None and not isinstance(value, str) :
            raise TypeError(f"description may be none or string, got type {type(value).__name__}")
        #
        if isinstance(value, str) and not value.strip() :
            raise ValueError("description can't be empty.")
        #
        self._description = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value : str):
        if not isinstance(value, str):
            raise TypeError(f"title must be string, got type {type(value).__name__}")
        #
        if not value.strip():
            raise ValueError("Configurable title can't be empty")
        #
        self._title = value
        
    @property
    def id(self):
        return self._id
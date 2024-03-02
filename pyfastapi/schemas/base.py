from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item: object) -> bool:
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass

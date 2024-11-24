from abc import ABC, abstractmethod
from typing import Generic, List, Set, TypeVar, Dict


class BaseNode(ABC):
    """Base class for all nodes"""

    # @abstractmethod
    # def is_root(self) -> bool:
    #     raise NotImplementedError


N = TypeVar("N", bound=BaseNode)


class BaseNodePool(ABC, Generic[N]):
    """Base class for all node pools"""

    def __init__(self):
        self._nodes: Dict[str, N] = {}

    def get_root_ids(self) -> Set[str]:
        raise NotImplementedError

NP = TypeVar("NP", bound=BaseNodePool)

from itertools import tee, zip_longest
from typing import Iterable, Iterator, Optional, Tuple, TypeVar

Element = TypeVar("Element")


def pairwise(
    iterable: Iterable[Element],
) -> Iterator[Tuple[Element, Optional[Element]]]:
    """Iterates through an iterable to return element and next
    ex: "[a,b,c]" -> (a,b), (b,c), (c,None)

    Note: in python 3.10 pairwise is included in itertools
    Args:
        iterable : the object to iterate through
    """
    a, b = tee(iterable)
    next(b, None)
    return zip_longest(a, b)

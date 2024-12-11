from typing import Generator, Generic, Optional, TypeVar


T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, data: T) -> None:
        self.data = data
        self.next: Optional[Node[T]] = None
        self.prev: Optional[Node[T]] = None


class LinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None

    def append(self, data: T) -> Node[T]:
        node = Node(data)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            assert self.tail is not None
            self.tail.next = node
            self.tail = node
        return node

    def remove(self, node: Node[T]) -> None:
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    def __iter__(self) -> Generator[Node[T], None, None]:
        node = self.head
        while node is not None:
            yield node
            node = node.next

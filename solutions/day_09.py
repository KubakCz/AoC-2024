from typing import Generator, Iterable, List, Tuple


def get_disk_blocks(input: str) -> Generator[int | None, None, None]:
    # Disk representation in blocks. Each block has file ID or None if empty
    for id2, block_count in enumerate(input):
        if id2 % 2 == 0:
            # File blocks
            id = id2 // 2
            for _ in range(int(block_count)):
                yield id
        else:
            # Empty blocks
            for _ in range(int(block_count)):
                yield None


def check_sum(disk: Iterable[int | None]) -> int:
    total = 0
    for i, file_id in enumerate(disk):
        if file_id is None:
            continue
        total += i * file_id
    return total


class DiskInfo:
    def __init__(self, input: str):
        # LinkedList of (start_idx, count) of empty blocks.
        self.empty_blocks: List[Tuple[int, int]] = []
        # List of (start_idx, count) of file blocks. File ID is the index.
        self.file_blocks: List[Tuple[int, int]] = []
        blocks_used = 0
        for id2, block_count_str in enumerate(input):
            block_count = int(block_count_str)
            if id2 % 2 == 0:
                # File blocks
                self.file_blocks.append((blocks_used, block_count))
            else:
                # Empty blocks
                self.empty_blocks.append((blocks_used, block_count))
            blocks_used += block_count

    def check_sum(self) -> int:
        total = 0
        for file_id, (start_idx, count) in enumerate(self.file_blocks):
            # file_id * Arithmetic sum (Arithmetic sum will always be even)
            total += file_id * count * (2 * start_idx + count - 1) // 2
        return total


def print_disk(disk: Iterable[int | None]) -> None:
    for block in disk:
        print(block if block is not None else ".", end="")
    print()


def solve_1(input: List[str]) -> str:
    disk = list(get_disk_blocks(input[0]))

    last_file_block_idx = len(disk) - 1
    first_empty_block_idx = 0

    while first_empty_block_idx < last_file_block_idx:
        # Find the first empty block
        while disk[first_empty_block_idx] is not None and first_empty_block_idx < last_file_block_idx:
            first_empty_block_idx += 1
        # Find the last file block
        while disk[last_file_block_idx] is None and first_empty_block_idx < last_file_block_idx:
            last_file_block_idx -= 1
        # Move the file block to the empty block
        disk[first_empty_block_idx] = disk[last_file_block_idx]
        disk[last_file_block_idx] = None

    return f"Checksum: {check_sum(disk)}"


def solve_2(input: List[str]) -> str:
    diskInfo = DiskInfo(input[0])
    for file_id in range(len(diskInfo.file_blocks) - 1, -1, -1):
        start_idx, count = diskInfo.file_blocks[file_id]
        for empty_block_idx, empty_block_node in enumerate(diskInfo.empty_blocks):
            (empty_start_idx, empty_count) = empty_block_node
            if empty_start_idx > start_idx:
                break  # No more empty blocks to the left of the file block
            if empty_count >= count:
                # Move the file blocks to the empty blocks
                diskInfo.file_blocks[file_id] = (empty_start_idx, count)
                if empty_count == count:
                    # Remove the empty block
                    diskInfo.empty_blocks.pop(empty_block_idx)
                else:
                    # Update the size of the empty block
                    diskInfo.empty_blocks[empty_block_idx] = (empty_start_idx + count, empty_count - count)
                break
    return f"Checksum: {diskInfo.check_sum()}"

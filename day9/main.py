from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from utils.helpers import expect


@dataclass
class Block:
    file_id: Optional[int]
    size: int
    is_free: bool

    @staticmethod
    def free(size: int) -> "Block":
        return Block(file_id=None, size=size, is_free=True)

    @staticmethod
    def file(file_id: int, size: int) -> "Block":
        return Block(file_id=file_id, size=size, is_free=False)

    def copy(self) -> "Block":
        return Block(self.file_id, self.size, self.is_free)


@dataclass
class Disk:
    blocks: list[Block]

    @staticmethod
    def from_disk_map(disk_map: str) -> "Disk":
        blocks = []
        for i, size in enumerate(int(c) for c in disk_map):
            if i % 2 == 0:
                blocks.append(Block.file(file_id=i // 2, size=size))
            else:
                blocks.append(Block.free(size))

        return Disk(blocks)

    def __str__(self) -> str:
        s = ""
        for block in self.blocks:
            char = "." if block.is_free else str(block.file_id)
            s += char * block.size

        return s

    def checksum(self) -> int:
        index = 0
        checksum = 0.0
        for block in self.blocks:
            if not block.is_free:
                checksum += (
                    ((index + index + block.size - 1) / 2)
                    * float(block.size)
                    * float(expect(block.file_id))
                )
            index += block.size

        return int(checksum)

    def compact(self) -> None:
        i = 0
        j = len(self.blocks) - 1
        while True:
            block = self.blocks[i]
            while not block.is_free:
                i += 1
                block = self.blocks[i]

            last_block = self.blocks[j]
            while last_block.is_free:
                j -= 1
                last_block = self.blocks[j]

            if i >= j:
                break

            if block.size == last_block.size:
                block.is_free = False
                block.file_id = last_block.file_id
                last_block.is_free = True
                i += 1
                continue

            if block.size > last_block.size:
                self.blocks.insert(i, last_block.copy())
                block.size -= last_block.size
                last_block.is_free = True
                continue

            if block.size < last_block.size:
                block.is_free = False
                block.file_id = last_block.file_id
                last_block.size -= block.size
                continue

    def compact2(self) -> None:
        j = len(self.blocks) - 1
        while j >= 0:
            last_block = self.blocks[j]
            while last_block.is_free:
                j -= 1
                last_block = self.blocks[j]

            i = 0
            block = self.blocks[i]
            while (not block.is_free) or block.size < last_block.size:
                if i >= len(self.blocks) - 1 or i >= j:
                    break
                i += 1
                block = self.blocks[i]

            if i >= len(self.blocks) - 1 or i >= j:
                j -= 1
                continue

            if block.size == last_block.size:
                block.is_free = False
                block.file_id = last_block.file_id
                last_block.is_free = True
                j -= 1
                continue

            if block.size > last_block.size:
                self.blocks.insert(i, last_block.copy())
                block.size -= last_block.size
                last_block.is_free = True
                j -= 1
                continue

            j -= 1


def main() -> None:
    disk_map = Path("input/input.txt").read_text("utf-8").strip()

    disk = Disk.from_disk_map(disk_map)
    disk.compact()
    print(disk.checksum())

    disk2 = Disk.from_disk_map(disk_map)
    disk2.compact2()
    print(disk2.checksum())


if __name__ == "__main__":
    main()

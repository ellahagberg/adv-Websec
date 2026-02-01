import hashlib
from M1P1 import byteToHex, hexToByte

def sha1_bytes(b: bytes) -> bytes:
    return hashlib.sha1(b).digest()

def merkle_root_from_leaf_and_path(leaf_hex: str, path_lines: list[str]) -> bytes:
    cur = hexToByte(leaf_hex)

    for line in path_lines:
        line = line.strip()
        side = line[0].upper()
        sib = hexToByte(line[1:])

        if side == "L":
            cur = sha1_bytes(sib + cur)
        elif side == "R":
            cur = sha1_bytes(cur + sib)
    return cur


def build_levels_sha1(leaves: list[bytes]) -> list[list[bytes]]:
    levels = [leaves[:]]
    while len(levels[-1]) > 1:
        level = levels[-1][:]
        if len(level) % 2 == 1:
            level.append(level[-1])

        nxt = []
        for i in range(0, len(level), 2):
            nxt.append(sha1_bytes(level[i] + level[i + 1]))

        levels.append(nxt)
    return levels

def merkle_path_for_index(levels: list[list[bytes]], i: int) -> list[str]:
    idx = i
    path = []
    for level in levels[:-1]:
        if len(level) % 2 == 1:
            effective = level + [level[-1]]
        else:
            effective = level

        sib = effective[idx ^ 1]
        side = "R" if (idx % 2 == 0) else "L"
        path.append(side + byteToHex(sib))
        idx //= 2
    return path

def path_node_at_depth(path: list[str], j: int) -> str:
    return path[len(path) - j]

def main():
    # leaves.txt (alla löv) ->vart är noden och vad är roten
    with open("leaves.txt", "r", encoding="utf-8") as f:
        lines = [ln.strip().lower() for ln in f if ln.strip()]

    i = int(lines[0])
    j = int(lines[1])
    leaves_hex = lines[2:]

    leaves = [hexToByte(hx) for hx in leaves_hex]
    levels = build_levels_sha1(leaves)
    root1 = levels[-1][0]

    path = merkle_path_for_index(levels, i)
    node_j = path_node_at_depth(path, j)

    print(node_j + byteToHex(root1))

    # leaf.txt så path och leaf->root
    with open("leaf.txt", "r", encoding="utf-8") as f:
        lines = [ln.strip().lower() for ln in f if ln.strip()]

    leaf_hex = lines[0]
    path_lines = lines[1:]

    root2 = merkle_root_from_leaf_and_path(leaf_hex, path_lines)
    print(byteToHex(root2))

if __name__ == "__main__":
    main()

from subprocess import check_output
from cypack.answer import zen_hash


def test_zen_hash():
    try:
        md5sum = check_output(["md5sum", "src/cypack/data/zen.txt"]).split(maxsplit=1)[0]
    except FileNotFoundError:
        # macOS
        md5sum = check_output(["md5", "src/cypack/data/zen.txt"]).split()[-1]
    assert md5sum == zen_hash().encode("ascii")

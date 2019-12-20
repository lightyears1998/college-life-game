import errno
import os

gb = "2345"


def change():
    global gb
    print(gb)
    gb = "ss"


def mkdirp(path: str) -> None:
    """
    若指定的目录不存在则将创建指定目录。
    :param path: 指定一个目录
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

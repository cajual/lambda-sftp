# filesystem served by pytest-sftpserver plugin
from os import environ
from sftpretty import CnOpts

# some default values for testing
USER = environ.get("USER", environ.get("USERNAME"))
PASS = "tEst@!357"


def conn(sftpsrv):
    """return a dictionary holding argument info for the sftpretty client"""
    cnopts = CnOpts(knownhosts="tests/resources/sftpserver.pub")
    return {
        "cnopts": cnopts,
        "default_path": "/home/test/pub",
        "host": sftpsrv.host,
        "port": sftpsrv.port,
        "private_key": "tests/resources/id_testkey",
        "private_key_pass": PASS,
        "username": USER,
    }


# filesystem served by pytest-sftpserver plugin
VFS = {
    "home": {
        "test": {
            "pub": {
                "foo1": {
                    "foo1.txt": "content of foo1.txt",
                    "image01.jpg": "data for image01.jpg",
                },
                "make.txt": "content of make.txt",
                "foo2": {
                    "bar1": {"bar1.txt": "contents bar1.txt"},
                    "foo2.txt": "content of foo2.txt",
                },
            },
            "read.me": "contents of read.me",
        }
    }
}

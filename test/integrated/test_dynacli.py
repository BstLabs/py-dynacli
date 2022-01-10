import os
import unittest
from os import environ, path
from subprocess import run
from typing import Union
from unittest import TestCase


def _get_expected(file_path: str) -> Union[tuple[str, None], tuple[str, str]]:
    with open(file_path, "r") as f:
        outputs = f.read().split("---")
    if len(outputs) < 2:
        return outputs[0], ""
    return outputs[0], outputs[1].lstrip()


class TestDynaCLI(TestCase):
    def setUp(self):
        cwd = path.dirname(__file__)
        environ["PATH"] = f'{environ["PATH"]}:{cwd}'

    def test_cli(self) -> None:
        dirname_ = os.path.dirname(__file__)
        self.maxDiff = None
        for test in os.listdir(f"{dirname_}/suite"):
            file_name, _ = os.path.splitext(test)
            cmd = file_name.split(" ")
            file_path = f"{dirname_}/suite/{test}"
            stdout, stderr = _get_expected(file_path)
            with self.subTest(cmd=file_name):
                print("Running ", cmd)
                result = run(cmd, capture_output=True, env=environ, text=True)
                self.assertEqual(stderr, result.stderr)
                self.assertEqual(stdout, result.stdout)


if __name__ == "__main__":
    unittest.main()

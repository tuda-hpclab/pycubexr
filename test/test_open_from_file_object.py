import io
import unittest
import zipfile
from pathlib import Path

from pycubexr import CubexParser


class TestOpenFromFileObject(unittest.TestCase):

    def setUp(self) -> None:
        self.cubex_file_path = Path("../data/blast.p64.r1/profile.cubex").resolve()
        with CubexParser(self.cubex_file_path) as cube_file:
            self.expected_metric_names = sorted(metric.name for metric in cube_file.all_metrics())

    def test_open_from_path(self):
        with CubexParser(self.cubex_file_path) as cube_file:
            metric_names = sorted(metric.name for metric in cube_file.all_metrics())
        self.assertEqual(self.expected_metric_names, metric_names)

    def test_open_from_file_object(self):
        with open(self.cubex_file_path, 'rb') as f:
            with CubexParser(f) as cube_file:
                metric_names = sorted(metric.name for metric in cube_file.all_metrics())
        self.assertEqual(self.expected_metric_names, metric_names)

    def test_open_from_bytes_io(self):
        with open(self.cubex_file_path, 'rb') as f:
            buf = io.BytesIO(f.read())
        with CubexParser(buf) as cube_file:
            metric_names = sorted(metric.name for metric in cube_file.all_metrics())
        self.assertEqual(self.expected_metric_names, metric_names)

    def test_open_from_zip_file(self):
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, 'w') as zf:
            zf.write(self.cubex_file_path, arcname='profile.cubex')
        zip_buf.seek(0)

        with zipfile.ZipFile(zip_buf) as zf:
            with zf.open('profile.cubex') as f:
                with CubexParser(f) as cube_file:
                    metric_names = sorted(metric.name for metric in cube_file.all_metrics())
        self.assertEqual(self.expected_metric_names, metric_names)


if __name__ == '__main__':
    unittest.main()
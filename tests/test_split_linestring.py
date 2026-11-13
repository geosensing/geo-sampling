"""Roads are cut into pieces whose recorded length follows the road."""

import unittest

import pyproj
from shapely.geometry import LineString

from geo_sampling.data.osm import OSMProvider

UTM_43N = "+proj=utm +zone=43 +north +datum=WGS84"


def from_utm(points):
    """A line in Delhi's UTM zone, given in meters, as longitude and latitude."""
    to_wgs84 = pyproj.Transformer.from_crs(UTM_43N, "EPSG:4326", always_xy=True)
    return LineString([to_wgs84.transform(x, y) for x, y in points])


class TestSplitLinestring(unittest.TestCase):
    def setUp(self):
        self.provider = OSMProvider.__new__(OSMProvider)
        self.origin = (715000.0, 3165000.0)

    def split(self, offsets, segment_length=500):
        x0, y0 = self.origin
        line = from_utm([(x0 + dx, y0 + dy) for dx, dy in offsets])
        return self.provider._split_linestring(line, segment_length)

    def test_lengths_follow_a_bend(self):
        """An L of 700 m then 500 m: the middle piece bends, so its chord is shorter."""
        pieces = self.split([(0, 0), (700, 0), (700, 500)])
        lengths = [length for _, length in pieces]
        self.assertEqual(len(pieces), 3)
        for got, expected in zip(lengths, [500, 500, 200]):
            self.assertAlmostEqual(got, expected, places=3)
        self.assertAlmostEqual(sum(lengths), 1200, places=3)

    def test_exact_multiple_leaves_no_sliver(self):
        pieces = self.split([(0, 0), (1000, 0)])
        self.assertEqual(len(pieces), 2)

    def test_short_and_empty_lines(self):
        pieces = self.split([(0, 0), (120, 0)])
        self.assertEqual(len(pieces), 1)
        self.assertAlmostEqual(pieces[0][1], 120, places=3)
        self.assertEqual(self.split([(0, 0), (0, 0)]), [])

    def test_pieces_stay_near_the_line(self):
        """Converting back from UTM must land in Delhi, not elsewhere."""
        pieces = self.split([(0, 0), (700, 0)])
        longitude, latitude = pieces[0][0].coords[0]
        self.assertAlmostEqual(latitude, 28.6, delta=0.1)
        self.assertAlmostEqual(longitude, 77.2, delta=0.1)


if __name__ == "__main__":
    unittest.main()

"""Type definitions for the geo_sampling package."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Union


def _optional(data: dict, key: str, convert):
    """Read a field that older files lack and that CSV stores as an empty string."""
    value = data.get(key)
    if value is None or value == "":
        return None
    return convert(value)


SEGMENT_COLUMNS = [
    "segment_id",
    "osm_id",
    "osm_name",
    "osm_type",
    "start_lat",
    "start_long",
    "end_lat",
    "end_long",
    "length_m",
    "stratum",
    "inclusion_prob",
]


@dataclass
class RoadSegment:
    """A road segment with start/end coordinates and metadata.

    Attributes:
        segment_id: Unique identifier for this segment
        osm_id: OpenStreetMap identifier
        osm_name: Name of the road from OSM
        osm_type: Type of road (primary, secondary, etc.)
        start_lat: Latitude of segment start point
        start_long: Longitude of segment start point
        end_lat: Latitude of segment end point
        end_long: Longitude of segment end point
        length_m: Length of the segment along the road, in meters
        stratum: Stratum the segment was sampled from, when the draw was stratified
        inclusion_prob: Probability that the draw included this segment
    """

    segment_id: int
    osm_id: str
    osm_name: str
    osm_type: str
    start_lat: float
    start_long: float
    end_lat: float
    end_long: float
    length_m: Optional[float] = None
    stratum: Optional[str] = None
    inclusion_prob: Optional[float] = None

    @classmethod
    def from_dict(cls, data: dict) -> RoadSegment:
        """Create RoadSegment from dictionary (e.g., CSV row)."""
        return cls(
            segment_id=int(data["segment_id"]),
            osm_id=str(data["osm_id"]),
            osm_name=str(data["osm_name"]),
            osm_type=str(data["osm_type"]),
            start_lat=float(data["start_lat"]),
            start_long=float(data["start_long"]),
            end_lat=float(data["end_lat"]),
            end_long=float(data["end_long"]),
            length_m=_optional(data, "length_m", float),
            stratum=_optional(data, "stratum", str),
            inclusion_prob=_optional(data, "inclusion_prob", float),
        )

    def to_dict(self) -> dict:
        """Convert RoadSegment to dictionary for CSV writing."""
        return {
            "segment_id": self.segment_id,
            "osm_id": self.osm_id,
            "osm_name": self.osm_name,
            "osm_type": self.osm_type,
            "start_lat": self.start_lat,
            "start_long": self.start_long,
            "end_lat": self.end_lat,
            "end_long": self.end_long,
            "length_m": self.length_m,
            "stratum": self.stratum,
            "inclusion_prob": self.inclusion_prob,
        }


@dataclass
class BoundingBox:
    """Geographic bounding box coordinates."""

    min_lat: float
    max_lat: float
    min_long: float
    max_long: float


RoadTypeFilter = Optional[Union[str, List[str]]]
"""Type alias for road type filtering - can be single type or list of types."""

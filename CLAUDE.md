# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python package for geographic road sampling that enables random sampling of street locations for data collection purposes. The core workflow involves downloading OpenStreetMap data, processing road segments, and generating sampling coordinates for field research.

## Key Architecture

- **geo_sampling/data/**: `gadm.py` downloads administrative boundaries; `osm.py` fetches OSM extracts from BBBike.org and splits roads into 500m segments, recording each segment's length.
- **geo_sampling/extractor.py**: `RoadExtractor` turns a region into a list of `RoadSegment`.
- **geo_sampling/sampler.py**: `RoadSampler` draws random, stratified, or length-targeted samples and records each sampled segment's inclusion probability and stratum.
- **geo_sampling/_types.py**: `RoadSegment` and the CSV column order.
- **geo_sampling/cli.py**, **convenience.py**, **visualization.py**: the `geo-sampling` command, one-call helpers, and plots.

## Development Commands

### Testing
```bash
uv run pytest             # Run all tests
```

### Linting and Code Quality
```bash
uv run ruff check .       # Linting (used in CI)
uv run ruff format .      # Code formatting
uv run ruff format --check .  # Check formatting (used in CI)
```

### Package Building
```bash
pip install -e .          # Install in development mode
python -m build           # Build distribution packages
pip install .             # Install package normally
```

### Documentation
```bash
cd docs && make html      # Build Sphinx documentation (uses uv run)
cd docs && make clean     # Clean documentation build
```

## CLI Commands

One command, `geo-sampling`, with subcommands; see `geo_sampling/cli.py`.

## Data Flow

1. Extract: GADM boundary → OSM data from BBBike → 500m segments → CSV
2. Sample: segments → filtered by road type → random or stratified draw → CSV with `inclusion_prob`, `stratum`, `length_m`
3. Optional plots of the sample by road type

## Implementation Notes

- BBBike.org extract URLs are dynamically generated via web scraping
- Road segments are split into 500m chunks for consistent sampling density
- Geographic transformations use UTM coordinate system for distance calculations
- CI runs on Python 3.11+ with ruff for code quality and formatting

## Dependencies

Core dependencies include pyshp (shapefile processing), matplotlib (plotting), pyproj/utm (coordinate transformations), Shapely (geometry operations), and beautifulsoup4/requests (web scraping BBBike extract URLs).

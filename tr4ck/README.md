# tr4ck - tracking tools
## dependencies
`pykml` - install via `pip install pykml` or `easy_install pykml`

`scapy` - install via `pip install scapy` or `easy_install scapy`

## checklist
- `tr4ckdb`
  - structure entries so that full timestamp & class are preserved (ie. maintain deseriability)
- `traffic`
  - database analysis
  - ~~database creation~~
- triangulation
  - `triangulate.triangulate`
  - `geometry`
    - `geometry.Circle.intersect`
    - ~~`geometry.Polygon.__contains__`~~
  - `triangulate._polygon_to_kml`
  - `triangulate.triangulate`

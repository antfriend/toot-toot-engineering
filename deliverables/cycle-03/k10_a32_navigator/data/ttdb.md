# Dice TTDB (K10)
Compact Dice TTDB sample for A32 LittleFS navigation.

```mmpdb
db_id: mmpdb:sample:dice:k10:v2
db_name: "Dice (K10 LittleFS)"
coord_increment:
  lat: 1
  lon: 1
collision_policy: southeast_step
timestamp_kind: unix_utc
umwelt:
  umwelt_id: umwelt:tte:agent:dice:v1
  role: dice_librarian
  perspective: "A lattice of dice geometry mapped onto a globe."
  scope: "Compact dice TTDB for K10 LittleFS navigation."
cursor_policy:
  max_preview_chars: 220
  max_nodes: 12
typed_edges:
  enabled: true
  syntax: "type>@TARGET_ID"
  note: "Typed edges connect matching latitudes and longitudes."
librarian:
  enabled: true
  primitive_queries:
    - "SELECT <record_id>"
    - "FIND <token>"
    - "EDGES <record_id>"
    - "STATUS"
  max_reply_chars: 220
  invocation_prefix: "@AI"
```

```cursor
selected:
  - @LAT35.264LON45.0
preview:
  @LAT35.264LON45.0: "Cube vertex at sea level (z=0)."
agent_note: "Dice TTDB compact set for K10 LittleFS."
```

---

@LAT35.264LON45.0 | created:1760000000 | updated:1760000000 | z:0 | relates:lat>@LAT35.264LON135.0,lat>@LAT35.264LON-135.0,lat>@LAT35.264LON-45.0,lon>@LAT-35.264LON45.0

## Cube Vertex NE
North hemisphere vertex at lon 45. Lat links to other north vertices; lon links to its south counterpart.

---

@LAT35.264LON135.0 | created:1760000001 | updated:1760000001 | z:0 | relates:lat>@LAT35.264LON45.0,lat>@LAT35.264LON-135.0,lat>@LAT35.264LON-45.0,lon>@LAT-35.264LON135.0

## Cube Vertex NW
North hemisphere vertex at lon 135.

---

@LAT35.264LON-135.0 | created:1760000002 | updated:1760000002 | z:0 | relates:lat>@LAT35.264LON45.0,lat>@LAT35.264LON135.0,lat>@LAT35.264LON-45.0,lon>@LAT-35.264LON-135.0

## Cube Vertex SW
North hemisphere vertex at lon -135.

---

@LAT35.264LON-45.0 | created:1760000003 | updated:1760000003 | z:0 | relates:lat>@LAT35.264LON45.0,lat>@LAT35.264LON135.0,lat>@LAT35.264LON-135.0,lon>@LAT-35.264LON-45.0

## Cube Vertex SE
North hemisphere vertex at lon -45.

---

@LAT-35.264LON45.0 | created:1760000004 | updated:1760000004 | z:0 | relates:lat>@LAT-35.264LON135.0,lat>@LAT-35.264LON-135.0,lat>@LAT-35.264LON-45.0,lon>@LAT35.264LON45.0

## Cube Vertex NE (South)
South hemisphere vertex at lon 45.

---

@LAT-35.264LON135.0 | created:1760000005 | updated:1760000005 | z:0 | relates:lat>@LAT-35.264LON45.0,lat>@LAT-35.264LON-135.0,lat>@LAT-35.264LON-45.0,lon>@LAT35.264LON135.0

## Cube Vertex NW (South)
South hemisphere vertex at lon 135.

---

@LAT-35.264LON-135.0 | created:1760000006 | updated:1760000006 | z:0 | relates:lat>@LAT-35.264LON45.0,lat>@LAT-35.264LON135.0,lat>@LAT-35.264LON-45.0,lon>@LAT35.264LON-135.0

## Cube Vertex SW (South)
South hemisphere vertex at lon -135.

---

@LAT-35.264LON-45.0 | created:1760000007 | updated:1760000007 | z:0 | relates:lat>@LAT-35.264LON45.0,lat>@LAT-35.264LON135.0,lat>@LAT-35.264LON-135.0,lon>@LAT35.264LON-45.0

## Cube Vertex SE (South)
South hemisphere vertex at lon -45.

---

@LAT0.0LON0.0 | created:1760000100 | updated:1760000100 | z:11

## Pip: Face 1 Center
Front face, single pip. The simplest expression of the cube's interior axis.

---

@LAT20.0LON130.0 | created:1760000101 | updated:1760000101 | z:22

## Pip: Face 2 Top-Left
Back face, upper-left pip.

---

@LAT-20.0LON170.0 | created:1760000102 | updated:1760000102 | z:22

## Pip: Face 2 Bottom-Right
Back face, lower-right pip.

---

@LAT20.0LON70.0 | created:1760000103 | updated:1760000103 | z:33

## Pip: Face 3 Top-Left
East face, upper-left pip.

---

@LAT0.0LON90.0 | created:1760000104 | updated:1760000104 | z:33

## Pip: Face 3 Center
East face, center pip.

---

@LAT-20.0LON110.0 | created:1760000105 | updated:1760000105 | z:33

## Pip: Face 3 Bottom-Right
East face, lower-right pip.

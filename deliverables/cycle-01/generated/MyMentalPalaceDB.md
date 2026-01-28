# MyMentalPalaceDB

## Settings
- Generated: 2026-01-28T21:48:56Z
- ID_STEP_LAT: 0.0001
- ID_STEP_LON: 0.0001
- Collision rule: if event_id exists, move South-East by one step until unique

## Cursor
- current_event_id: 44.0674,-115.9567

## Umwelt
Librarian perspective: I observe typed events on the MQTT bus and preserve them as a navigable graph.
Globe mapping: event_id is represented as a lat,lon-like coordinate; nearby points are conceptually related by time/story trails.
Observed nodes: node:esp32-field, node:tdeck-plus, node:unihiker-k10

## Typed edges glossary
- announces_presence: Node announces it is online/present.
- reports_sensor: Node reports a sensor reading.
- addresses: A message is addressed to a specific node/service.
- responds_to: This event is a response/reply to another event/thread reference.

## Records

### Event 44.0905,-115.9768
- ts: 2026-01-27T08:00:00Z
- event_type: presence
- intent: presence_probe
- confidence: 1.0
- reported_by: node:tdeck-plus
- addressed_to: broadcast
- raw_ref: raw:sha256:9410d701650904a27ac5f61039e41892ab36e8090268bbbbc02f1a1eedea4612
- payload: `{'text': 'PING'}`
- entities: node:node:tdeck-plus
- edges:
  - announces_presence: node:tdeck-plus -> node:tdeck-plus
- mesh_meta: `{'rssi': -90, 'snr': 7.0, 'hop_count': 1, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0360,-115.9061
- ts: 2026-01-27T08:01:00Z
- event_type: presence
- intent: presence_probe
- confidence: 1.0
- reported_by: node:unihiker-k10
- addressed_to: broadcast
- raw_ref: raw:sha256:33b0fc9fd243787ff2f3e16a763058244ffb480692490da2cdace000a4e92de7
- payload: `{'text': 'PING'}`
- entities: node:node:unihiker-k10
- edges:
  - announces_presence: node:unihiker-k10 -> node:unihiker-k10
- mesh_meta: `{'rssi': -91, 'snr': 6.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0182,-115.9946
- ts: 2026-01-27T08:02:00Z
- event_type: presence
- intent: presence_probe
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:c1633082bc1013351a1e99e39978bcd34669462e115a43954094e67a9939dc41
- payload: `{'text': 'PING'}`
- entities: node:node:esp32-field
- edges:
  - announces_presence: node:esp32-field -> node:esp32-field
- mesh_meta: `{'rssi': -92, 'snr': 6.0, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0357,-115.9176
- ts: 2026-01-27T09:00:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:06791bcc921638a4cbc8e20c4ca3724cd2c9616674abd10ae19f0935b86c0e49
- payload: `{'value': 17.1, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0057,-115.9143
- ts: 2026-01-27T09:10:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:41fee42dd7f26c1348e610b3e722b3f719c1edc05b95fa197aaabd7b0acd3133
- payload: `{'value': 17.3, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0959,-115.9878
- ts: 2026-01-27T09:20:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:d885c4e0d23a1f0a951dc4f48ca5dddc6a0c4d80531cd807240433efd0172c15
- payload: `{'value': 17.2, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0093,-115.9529
- ts: 2026-01-27T09:30:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:69e19f2feebcda98af8d83b0b06e5bd4f02281f8bb45d1648d30d43db1e0e982
- payload: `{'value': 17.4, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0000,-115.9791
- ts: 2026-01-27T09:40:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:2005e0c88b4b515e7b32420d466918ba455690bd2bdf2a644825918d3c4a3cf5
- payload: `{'value': 17.6, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0960,-115.9896
- ts: 2026-01-27T09:50:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:0edc9014665eda16b865ef2bf2048bab1eac749fe8bf49d86525f01f15d17a8c
- payload: `{'value': 18.0, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0001,-115.9516
- ts: 2026-01-27T10:00:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:51cc1cf5f7f7b76089b09b2dbaa26789e99536a215ae1193978abaa726875ea6
- payload: `{'value': 18.4, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0035,-115.9157
- ts: 2026-01-27T10:10:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:35a82fd85b781e20ec67cedae290d6b69aa1dbfe028119b9516dcb4a414ef15e
- payload: `{'value': 19.2, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0099,-115.9533
- ts: 2026-01-27T10:20:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:877377263b0db239ded4bf70d74f8d2d72c7ac5c41a03513e8e401e85af668a6
- payload: `{'value': 20.1, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0356,-115.9900
- ts: 2026-01-27T10:30:00Z
- event_type: sensor
- intent: sensor_reading.temperature
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:b70a0599b3444b79feed162cb4e9540f39a534da4f2d3e655388acb738f302e3
- payload: `{'value': 22.7, 'unit': 'C'}`
- entities: node:node:esp32-field, sensor:sensor:temp
- edges:
  - reports_sensor: node:esp32-field -> sensor:temp
- mesh_meta: `{'rssi': -105, 'snr': 5.5, 'hop_count': 0, 'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0510,-115.9251
- ts: 2026-01-27T11:05:00Z
- event_type: bulletin
- intent: bulletin_post
- confidence: 1.0
- reported_by: node:unihiker-k10
- addressed_to: broadcast
- raw_ref: raw:sha256:4732e8a1eea2a7da192199f399835c037f8e240c7756c7099f0e306dec27e407
- payload: `{'message': 'TEMP ALERT threshold exceeded at node:esp32-field'}`
- entities: node:node:unihiker-k10
- mesh_meta: `{'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0495,-115.9644
- ts: 2026-01-27T12:00:00Z
- event_type: logistics
- intent: logistics_request
- confidence: 1.0
- reported_by: node:tdeck-plus
- addressed_to: broadcast
- raw_ref: raw:sha256:cc874d27e6a3b95aa5e727a38f0adee34e3d33b918cfa8fbe02ad3c8fe1fe2cc
- payload: `{'request': 'bring water to ridge trailhead'}`
- entities: node:node:tdeck-plus
- mesh_meta: `{'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0740,-115.9862
- ts: 2026-01-27T12:02:00Z
- event_type: logistics
- intent: logistics_offer
- confidence: 1.0
- reported_by: node:unihiker-k10
- addressed_to: broadcast
- raw_ref: raw:sha256:7c1f1075347f784c902cbd843dc078eb235dbaa0bdfcffd0b32b2adf0ee2bdbf
- payload: `{'offer': 'can deliver in 30m'}`
- entities: node:node:unihiker-k10
- mesh_meta: `{'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0881,-115.9156
- ts: 2026-01-27T14:00:00Z
- event_type: emergency
- intent: emergency_medical
- confidence: 0.98
- reported_by: node:tdeck-plus
- addressed_to: broadcast
- raw_ref: raw:sha256:f001650963072cc32374d19cc6b7854f0c33e13f6d6efaf8deac4811e1f4f386
- payload: `{'text': 'HELP MEDICAL'}`
- entities: node:node:tdeck-plus
- mesh_meta: `{'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0377,-115.9280
- ts: 2026-01-27T14:01:00Z
- event_type: ack
- intent: acknowledgement
- confidence: 1.0
- reported_by: node:unihiker-k10
- addressed_to: node:tdeck-plus
- raw_ref: raw:sha256:477e5fdc7b56f58368b9b82940b481cc080123cb0fb640da1153e58ca68cc6ee
- payload: `{'text': 'OK'}`
- entities: node:node:unihiker-k10
- mesh_meta: `{'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0846,-115.9722
- ts: 2026-01-27T16:00:00Z
- event_type: bulletin
- intent: bulletin_post
- confidence: 1.0
- reported_by: node:unihiker-k10
- addressed_to: broadcast
- raw_ref: raw:sha256:98eb77f2aeb1695152b52d9efd3bc129fcd6046821f5cb912fb463dff7c22073
- payload: `{'message': 'Trailhead closed after 18:00'}`
- entities: node:node:unihiker-k10
- mesh_meta: `{'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0486,-115.9427
- ts: 2026-01-27T16:05:00Z
- event_type: bulletin
- intent: bulletin_reply
- confidence: 1.0
- reported_by: node:tdeck-plus
- addressed_to: broadcast
- raw_ref: raw:sha256:de8f4fa71d66052a985e99d0978538e98e6dcab5f3cd759536f4c880429d6cf6
- payload: `{'message': 'Acknowledged', 'in_reply_to': 'thread:trailhead-closed'}`
- entities: node:node:tdeck-plus
- edges:
  - responds_to: 44.0486,-115.9427 -> thread:trailhead-closed
- mesh_meta: `{'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0327,-115.9107
- ts: 2026-01-27T16:07:00Z
- event_type: bulletin
- intent: bulletin_reply
- confidence: 1.0
- reported_by: node:esp32-field
- addressed_to: broadcast
- raw_ref: raw:sha256:48159f6f7daccdc1844a3bdf6910a5928e3ada0f1b674e165d6e26b6f980c35f
- payload: `{'message': 'Sensor node will switch to low power', 'in_reply_to': 'thread:trailhead-closed'}`
- entities: node:node:esp32-field
- edges:
  - responds_to: 44.0327,-115.9107 -> thread:trailhead-closed
- mesh_meta: `{'channel': 'primary', 'transport': 'simulated'}`

### Event 44.0674,-115.9567
- ts: 2026-01-27T17:00:00Z
- event_type: command
- intent: directed_command
- confidence: 1.0
- reported_by: node:tdeck-plus
- addressed_to: node:AI
- raw_ref: raw:sha256:55b11f1cf26198304e47d190cb45da9508c08d880be15c684f841757da499879
- payload: `{'command': 'summarize 6h', 'target': 'node:AI'}`
- entities: node:node:tdeck-plus, node:node:AI
- edges:
  - addresses: node:tdeck-plus -> node:AI
- mesh_meta: `{'channel': 'primary', 'transport': 'simulated'}`

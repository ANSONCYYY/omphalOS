CREATE TABLE IF NOT EXISTS trade_feed (
  shipment_id TEXT PRIMARY KEY,
  exporter_name TEXT,
  importer_name TEXT,
  exporter_country TEXT,
  importer_country TEXT,
  country TEXT,
  hs_code TEXT,
  value_usd DOUBLE,
  ship_date TEXT
);

CREATE TABLE IF NOT EXISTS registry (
  entity_id TEXT PRIMARY KEY,
  entity_name TEXT,
  country TEXT
);

CREATE TABLE IF NOT EXISTS entity_matches (
  shipment_id TEXT,
  entity_id TEXT,
  score DOUBLE,
  status TEXT,
  explanation TEXT
);

CREATE TABLE IF NOT EXISTS entity_scores (
  entity_id TEXT,
  entity_name TEXT,
  country TEXT,
  shipment_count INTEGER,
  total_value_usd DOUBLE,
  chokepoint_score DOUBLE
);

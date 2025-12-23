-- SQLite warehouse schema for omphalOS runs
--
-- The reference pipeline creates this schema inside each run directory.
-- This file is a stable description of the expected tables and columns.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS trade_feed (
  shipment_id      TEXT PRIMARY KEY,
  exporter_name    TEXT NOT NULL,
  importer_name    TEXT NOT NULL,
  exporter_country TEXT,
  importer_country TEXT,
  country          TEXT,
  hs_code          TEXT,
  value_usd        REAL,
  ship_date        TEXT
);

CREATE TABLE IF NOT EXISTS registry (
  entity_id   TEXT PRIMARY KEY,
  entity_name TEXT NOT NULL,
  country     TEXT
);

CREATE TABLE IF NOT EXISTS entity_matches (
  shipment_id  TEXT NOT NULL,
  entity_id    TEXT NOT NULL,
  score        REAL NOT NULL,
  status       TEXT NOT NULL,
  explanation  TEXT NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES trade_feed (shipment_id),
  FOREIGN KEY (entity_id) REFERENCES registry (entity_id)
);

CREATE TABLE IF NOT EXISTS review_queue (
  shipment_id     TEXT PRIMARY KEY,
  exporter_name   TEXT NOT NULL,
  reason          TEXT NOT NULL,
  candidates_json TEXT NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES trade_feed (shipment_id)
);

CREATE TABLE IF NOT EXISTS entity_scores (
  entity_id        TEXT NOT NULL,
  entity_name      TEXT NOT NULL,
  country          TEXT,
  shipment_count   INTEGER NOT NULL,
  total_value_usd  REAL NOT NULL,
  chokepoint_score REAL NOT NULL,
  FOREIGN KEY (entity_id) REFERENCES registry (entity_id)
);

CREATE INDEX IF NOT EXISTS idx_trade_feed_ship_date ON trade_feed (ship_date);
CREATE INDEX IF NOT EXISTS idx_trade_feed_hs_code   ON trade_feed (hs_code);
CREATE INDEX IF NOT EXISTS idx_matches_entity_id    ON entity_matches (entity_id);
CREATE INDEX IF NOT EXISTS idx_scores_score         ON entity_scores (chokepoint_score);

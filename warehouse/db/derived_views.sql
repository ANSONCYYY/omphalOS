-- Derived views for common analyst workflows

CREATE VIEW IF NOT EXISTS v_trade_hs_slices AS
SELECT
  shipment_id,
  exporter_name,
  importer_name,
  exporter_country,
  importer_country,
  COALESCE(exporter_country, country) AS country,
  hs_code,
  substr(hs_code, 1, 2) AS hs2,
  substr(hs_code, 1, 4) AS hs4,
  substr(hs_code, 1, 6) AS hs6,
  value_usd,
  ship_date
FROM trade_feed;

CREATE VIEW IF NOT EXISTS v_trade_with_match AS
SELECT
  t.shipment_id,
  t.exporter_name,
  t.importer_name,
  t.exporter_country,
  t.importer_country,
  t.country,
  t.hs_code,
  t.value_usd,
  t.ship_date,
  m.entity_id,
  m.score AS match_score,
  m.status AS match_status
FROM trade_feed t
LEFT JOIN entity_matches m
ON m.shipment_id = t.shipment_id;

CREATE VIEW IF NOT EXISTS v_entity_trade_rollup AS
SELECT
  m.entity_id,
  r.entity_name,
  r.country,
  count(*) AS shipment_count,
  sum(t.value_usd) AS total_value_usd,
  avg(m.score) AS mean_match_score
FROM entity_matches m
JOIN trade_feed t ON t.shipment_id = m.shipment_id
JOIN registry r ON r.entity_id = m.entity_id
GROUP BY 1,2,3;

CREATE VIEW IF NOT EXISTS v_review_queue_candidates AS
SELECT
  rq.shipment_id,
  rq.exporter_name,
  rq.reason,
  rq.candidates_json
FROM review_queue rq;

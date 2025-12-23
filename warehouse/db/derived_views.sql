CREATE OR REPLACE VIEW v_trade_enriched AS
SELECT
  shipment_id,
  exporter_name,
  importer_name,
  exporter_country,
  importer_country,
  hs_code,
  substr(hs_code, 1, 2) AS hs2,
  substr(hs_code, 1, 4) AS hs4,
  substr(hs_code, 1, 6) AS hs6,
  value_usd,
  ship_date
FROM trade_feed;

CREATE OR REPLACE VIEW v_entity_scores_ranked AS
SELECT
  entity_id,
  entity_name,
  country,
  shipment_count,
  total_value_usd,
  chokepoint_score,
  rank() OVER (ORDER BY chokepoint_score DESC, total_value_usd DESC) AS risk_rank
FROM entity_scores;

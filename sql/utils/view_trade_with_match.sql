select * from v_trade_with_match
where ship_date between :start_date and :end_date
order by ship_date asc, shipment_id asc
limit :limit;

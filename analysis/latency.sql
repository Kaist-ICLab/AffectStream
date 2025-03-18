SELECT sr.connection_id conn_id,
       er.inference_time-sr.timestamp e2e_latency_ms, sr.response_time-sr.timestamp producer_latency_ms, er.inference_time-er.timestamp consumer_latency_ms,
       sr.timestamp producer_record_start, sr.response_time producer_record_end,
       er.timestamp consumer_record_start, er.inference_time consumer_record_end
FROM start_record sr INNER JOIN end_record er on sr.connection_id = er.connection_id
ORDER BY e2e_latency_ms DESC;
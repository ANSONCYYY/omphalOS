select es.*
from entity_scores es
left join registry r on r.entity_id = es.entity_id
where r.entity_id is null;

GRANT USAGE ON SCHEMA emp_api TO web_anon;

drop table if exists emp_api.women_in_government;
create table emp_api.women_in_government as
select
	to_char(date_series,'Month YYYY')
	,women_gov_employees as valueInThousands
from public.required_ts rt 
where women_gov_employees is not null;

drop table if exists emp_api.production_supervision_ratio;
create table emp_api.production_supervision_ratio as
select
	to_char(date_series,'Month YYYY')
	,production_employees::decimal / (all_employees::decimal - production_employees::decimal) as ProdSuperRatio
from public.required_ts rt 
where production_employees is not null
	and all_employees is not null;

drop table if exists emp_api.women_in_government_forecast;
create table emp_api.women_in_government_forecast (
	date_series date,
	forecast decimal
);

drop table if exists emp_api.production_supervision_forecast;
create table emp_api.production_supervision_forecast (
	date_series date,
	forecast decimal
);

GRANT SELECT ON emp_api.women_in_government TO web_anon;
GRANT SELECT ON emp_api.production_supervision_ratio TO web_anon;
GRANT SELECT ON emp_api.women_in_government_forecast TO web_anon;
GRANT SELECT ON emp_api.production_supervision_forecast TO web_anon;

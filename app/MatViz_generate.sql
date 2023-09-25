drop materialized view if exists required_ts;
create materialized view required_ts as
select * from crosstab(
	$$
	select
		to_date(concat(trim(cp.month),' ',trim(ca.year)),'Month YYYY')
		,ta.series_title
		,sum(cast(ca.value as int))
	from (
		select 
			cs.series_id
			,series_title
		from ce_series cs
		left join ce_industry ci 
			on (ci.industry_code = cs.industry_code)
		left join ce_datatype cd
			on (cd.data_type_code = cs.data_type_code)
		where 
			(ci.industry_name = 'Government'
				and cs.data_type_code = '10' -- get 'WOMEN EMPLOYEES, THOUSANDS' time series
				and cs.seasonal = 'U'
			) 
			or (ci.industry_name = 'Total private'
				and cs.data_type_code in ('01','06') -- get 'ALL EMPLOYEES, THOUSANDS' and 'PRODUCTION AND NONSUPERVISORY EMPLOYEES, THOUSANDS' time series
				and cs.seasonal = 'U'
			)
	) ta
		left join ce_data_0_allcesseries ca
			on (ca.series_id = ta.series_id)
		left join ce_period cp
			on(cp.period = ca.period)
		where ca.period <> 'M13'
		group by 
			to_date(concat(trim(cp.month),' ',trim(ca.year)),'Month YYYY')
			,ta.series_title
		order by 
			to_date(concat(trim(cp.month),' ',trim(ca.year)),'Month YYYY')
	$$,
	$$ 
	select 'All employees, thousands, total private, not seasonally adjusted' union all
	select 'Production and nonsupervisory employees, thousands, total private, not seasonally adjusted' union all
	select 'Women employees, thousands, government, not seasonally adjusted' 
	$$	
)
as ct(
  date_series date
  ,all_employees int
  ,production_employees int
  ,women_gov_employees int
);

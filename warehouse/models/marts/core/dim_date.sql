-- dim_date — calendar dimension for the reporting window.
-- Static range covers launch through the first statutory reporting
-- cycles; extend the bounds when retention horizons require it.
select
    d::date as date_day,
    extract(year from d)::int as year_number,
    extract(month from d)::int as month_number,
    to_char(d, 'Month') as month_name,
    extract(dow from d)::int as day_of_week,
    extract(dow from d) between 1 and 5 as is_weekday,
    date_trunc('quarter', d)::date as quarter_start,
    to_char(date_trunc('quarter', d), 'IYYY-"Q"IQ') as quarter_label
from generate_series(date '2026-01-01', date '2027-12-31', interval '1 day') as d

-- See all forecasts
SELECT * FROM forecasts;

-- See all daily forecasts
SELECT * FROM daily_forecasts;

-- See all period forecasts
SELECT * FROM period_forecasts;

-- Or join them to see everything together
SELECT 
    f.id as forecast_id,
    f.location,
    f.forecast_date,
    df.day_name,
    pf.period,
    pf.temperature,
    pf.sky_condition
FROM forecasts f
LEFT JOIN daily_forecasts df ON f.id = df.forecast_id
LEFT JOIN period_forecasts pf ON df.id = pf.daily_forecast_id
ORDER BY df.date, pf.id;

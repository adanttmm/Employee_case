# End to end analysis pipeline:

Files in https://download.bls.gov/pub/time.series/ce/ was assessed to understand structure and select interesting data for the use case. After the frst assessment the following fies were selected for ingestion and further exploration:
* ce.data.0.ALLCESSeries
* ce.data.01a.CurrentSeasAE
* ce.data.02b.AllRealEarningsAE
* ce.data.03c.AllRealEarningsPE
* ce.data.Goog
* ce.datatype
* ce.footnote
* ce.industry
* ce.period
* ce.seasonal
* ce.series
* ce.supersector

A Python scrapper (fount in /app folder) was coded to ingest selected files directly into local PostgreSQL database.
After a second assessment and basic analysis done in SQL, script files were coded to prepare the materialized view with needed data, and a sparated schema to service the API with its own tables.

The PostgREST API was ennabled in localhost:3000 (ubuntu 20.4.1) and tested with positive results.

The analysis with the EDA, and forecasting models was coded in Google Colabs with a T4 GPU runtime, to ennable quick DLN training; baseline SARIMAX model, CNN with 1D, LSTM, and GRU architechtures were benchmarked to select final model, based on MAE on validation sample.

With final forecasts trained, a Python code (found in /app) was used to score pre-trained models, and load a 24 months forecast into original database that are mounted into the PostgREST API.

Final models were too large for GitHub commit, so they are not included.  

Once tested, a Docker conatiner is set using Compose with the following images found in DockerHub:
1. postgres:latest
2. postgrest/postgrest:latest
Scripts and codes are run in the container to ennable API in port 3000.

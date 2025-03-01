URL="https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-1979-latest-published-year.csv"

# Use the data loader cache directory to store the downloaded data.


# Download the data (if it’s not already in the cache).
if [ ! -f "dft-collisions.csv" ]; then
  curl -f "$URL" -o "dft-collisions.csv"
fi

# Generate a CSV file using DuckDB. maybe change this to avoid file dropping in root
duckdb :memory: << EOF
COPY (
  SELECT longitude, latitude
  FROM read_csv_auto('dft-collisions.csv')
  WHERE accident_year = 2022
) TO STDOUT WITH (FORMAT 'csv');
EOF
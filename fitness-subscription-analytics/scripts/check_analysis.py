"""Validate and summarize existing FitnessHub CSV exports without modifying them."""
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]


def read_export(filename):
    with (ROOT / 'analysis' / filename).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def check_forecast():
    forecast = read_export('forecast_12_months.csv')
    expected_months = [f'2026-{month:02d}' for month in range(2, 13)] + ['2027-01']
    if [row['Month'] for row in forecast] != expected_months:
        raise ValueError('Expected 12 consecutive forecast months: February 2026–January 2027.')
    original = {row['StartOfMonth'][:7]: row for row in read_export('power_bi_forecast_export.csv')}
    pairs = [('Forecast', 'forecastValue'), ('Upper_95', 'confidenceHighBound'), ('Lower_95', 'confidenceLowBound')]
    for row in forecast:
        source = original[row['Month']]
        for clean_field, source_field in pairs:
            if Decimal(row[clean_field]) != Decimal(source[source_field]):
                raise ValueError(f"Export mismatch: {row['Month']} / {clean_field}")
        if not Decimal(row['Lower_95']) <= Decimal(row['Forecast']) <= Decimal(row['Upper_95']):
            raise ValueError(f"Invalid bounds: {row['Month']}")
    total = sum((Decimal(row['Forecast']) for row in forecast), Decimal(0))
    print(f'12-month forecast: {total:,.0f}; monthly average: {total / 12:,.2f}')
    print('All forecast amounts and bounds match the supplied visual export.')


def summarize_payback():
    cohorts = defaultdict(list)
    for row in read_export('cac_ltv.csv'):
        cohorts[row['Cohort_Year']].append(row)
    for year, rows in sorted(cohorts.items()):
        rows.sort(key=lambda row: int(row['Age']))
        costs = [Decimal(row['Total_CAC']) for row in rows]
        if any(abs(cost - costs[0]) > Decimal('0.01') for cost in costs):
            raise ValueError(f'CAC varies across tenure for cohort {year}.')
        crossing = next((row for row in rows if Decimal(row['Cumulative_Subscription_Revenue']) >= costs[0]), None)
        if crossing:
            age = int(crossing['Age'])
            status = f"index {age}, payment month {age + 1}; fully observed: {crossing['Fully_Observed']}"
        else:
            status = 'not reached within available observations'
        print(f'{year}: CAC {costs[0]:,.2f}; payback {status}')


def summarize_retention():
    # Use the same eligible rows at both ages; this is an unweighted cohort mean.
    eligible = [row for row in read_export('cohort_retention.csv') if row['2'] and row['3']]
    if not eligible:
        raise ValueError('No cohorts have observations at both month indices 2 and 3.')
    earlier = mean(float(row['2']) for row in eligible)
    later = mean(float(row['3']) for row in eligible)
    print(f'Unweighted mean across {len(eligible)} eligible monthly cohorts:')
    print(f'  Index 2: {earlier:.1%}; index 3: {later:.1%}; drop: {(earlier-later)*100:.1f} percentage points')
    print('Payment cessation is a retention proxy, not a recorded cancellation date.')


def main():
    check_forecast()
    summarize_payback()
    summarize_retention()


if __name__ == '__main__':
    main()

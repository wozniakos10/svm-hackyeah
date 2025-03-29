MONTHLY_RATE = 500
YEARS = 5

# Zestawy stóp procentowych dla różnych poziomów ryzyka
risk_profiles = {
    "Ryzyko małe": [0.05, 0.00, 0.10],
    "Ryzyko średnie": [-0.05, 0.00, 0.13],
    "Ryzyko duże": [-0.20, 0.00, 0.18],
}


def calculate_smooth_compound_interest(years, monthly_payment, annual_interest_rate):
    total = 0
    timeline = []
    value_over_time = []

    months_per_year = 12  # Miesięczna kapitalizacja
    total_months = years * months_per_year

    monthly_interest_rate = (
        annual_interest_rate / months_per_year
    )  # Obliczamy miesięczną stopę procentową

    for month in range(1, total_months + 1):
        total += monthly_payment  # Dodajemy miesięczną wpłatę

        # Kapitalizacja miesięczna: co miesiąc oprocentowujemy
        total *= 1 + monthly_interest_rate

        # Dodajemy dane do osi czasu (w latach) oraz wartości
        timeline.append(month / months_per_year)  # Czas w latach
        value_over_time.append(total)  # Wartość inwestycji po kapitalizacji

    return timeline, value_over_time


X = int(
    calculate_smooth_compound_interest(
        YEARS, MONTHLY_RATE, risk_profiles["Ryzyko małe"][0]
    )[1][-1]
)
print(X)

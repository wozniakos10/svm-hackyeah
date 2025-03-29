from svm_hack.app.models import product_database


def get_products_info(products):
    """
    :param products: Lista produktów od czata
    :return: Lista obiektow juz do plotowania
    """
    d = {}
    for product in products:
        if product_database.find_by_type(product):
            d[product_database.find_by_type(product)[0].name] = (
                product_database.find_by_type(product)[0].parameters.min_return,
                product_database.find_by_type(product)[0].parameters.max_return,
            )
    return d


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

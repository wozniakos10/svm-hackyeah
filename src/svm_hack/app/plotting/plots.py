from svm_hack.app.plotting import calculate_smooth_compound_interest

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_strategy(product: dict, MONTHLY_RATE, YEARS):

    risk_profiles = {
        key: [item[0], 0, item[1]] for key, item in product.items()
    }

    possible_values_json =  {
        key: {} for key in product.keys()
    }

    # Kolory wspólne dla wszystkich wykresów
    scenario_labels = ["Pesymistyczny", "Brak Inwestycji", "Optymistyczny"]
    scenario_colors = ["#1f77b4", "#ff7f0e", "#d62728"]  # blue, orange, red

    # Utworzenie subplots z większą przestrzenią
    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=list(risk_profiles.keys()),
        shared_yaxes=True,
        horizontal_spacing=0.1,  # Zwiększamy przestrzeń między wykresami
    )

    # Dodanie wykresów
    for i, (title, rates) in enumerate(risk_profiles.items()):
        optimistic, neutral, pessimistic = rates
        x_vals, y_optimistic = calculate_smooth_compound_interest(
            YEARS, MONTHLY_RATE, optimistic
        )
        _, y_pessimistic = calculate_smooth_compound_interest(
            YEARS, MONTHLY_RATE, pessimistic
        )
        _, y_neutral = calculate_smooth_compound_interest(
            YEARS, MONTHLY_RATE, neutral
        )

        possible_values_json[title]["maksymalny zwrot"] = y_pessimistic[-1]
        possible_values_json[title]["minimalny zwrot"] = y_optimistic[-1]
        possible_values_json[title]["standardowy zwrot"] = y_neutral[-1]
        
        # Szare tło między optimistic i pessimistic
        fig.add_trace(
            go.Scatter(
                x=x_vals + x_vals[::-1],
                y=y_optimistic + y_pessimistic[::-1],
                fill="toself",
                fillcolor="rgba(200, 200, 200, 0.3)",
                line=dict(color="rgba(255,255,255,0)"),
                showlegend=False,
            ),
            row=1,
            col=i + 1,
        )

        # Linie: optymistyczna, neutralna, pesymistyczna
        for j, rate in enumerate(rates):
            x, y = calculate_smooth_compound_interest(YEARS, MONTHLY_RATE, rate)
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="lines",
                    name=scenario_labels[j],
                    line=dict(width=2, color=scenario_colors[j]),
                    legendgroup=scenario_labels[j],
                    showlegend=(i == 0),  # legenda tylko raz
                    textposition="top center",  # pozycja tekstu
                    textfont=dict(
                        size=16, color="black", family="Arial", weight="bold"
                    ),  # większe i pogrubione etykiety
                ),
                row=1,
                col=i + 1,
            )

            # Etykieta tekstowa na końcu (aktualna wartość inwestycji jako int)
            fig.add_trace(
                go.Scatter(
                    x=[x[-1]],
                    y=[y[-1]],
                    text=[
                        f"{int(y[-1]):,}    "
                    ],  # Wyświetlanie wartości inwestycji jako int
                    mode="text",
                    showlegend=False,
                    textfont=dict(
                        size=16, color="black", family="Arial", weight="bold"
                    ),  # większe i pogrubione etykiety
                ),
                row=1,
                col=i + 1,
            )

    # Layout
    fig.update_layout(
        title=f"Procent składany przy miesięcznej wpłacie {MONTHLY_RATE:.2f} zł",
        template="plotly_white",
        height=600,  # większe wykresy
        width=3000,  # szersze wykresy
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(t=60, b=100),
    )

    fig.update_yaxes(title_text="Wartość inwestycji    ", row=1, col=1)

    # Przesunięcie etykiet na osi X w lewo, aby nie były ucinane
    for col in range(1, 4):
        fig.update_xaxes(
            title_text="Czas (lata)",
            row=1,
            col=col,
            tickangle=0,
            tickmode="linear",
            tickvals=x_vals[::12],
            showticklabels=True,
        )

    # Wyświetlenie w Streamlit
    st.title("Porównanie ryzyk inwestycyjnych – 3 scenariusze")
    st.plotly_chart(fig, use_container_width=True)

    return possible_values_json

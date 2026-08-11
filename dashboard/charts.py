from .queries import consultas_cobradas
import pandas as pd

import plotly.graph_objects as go

def grafico_semanal(terapueta_id):
    
    df_citas_cobradas = pd.DataFrame(
    consultas_cobradas(terapueta_id).values("fecha", "forma_pago", "precio")
    )

    df_citas_cobradas[["year", "week"]] = (
        pd.to_datetime(df_citas_cobradas["fecha"])
        .dt.isocalendar()[["year", "week"]]
    )

    df_grafico = (
        df_citas_cobradas
        .sort_values(by=["year", "week"])
        .groupby(["forma_pago", "week"])
        .aggregate({"precio": "sum"})
        .reset_index()
    )
    
    fig = go.Figure()

    efectivo = df_grafico[
        df_grafico["forma_pago"] == "Efectivo"
    ]

    transferencia = df_grafico[
        df_grafico["forma_pago"] == "Transferencia"
    ]

    fig.add_trace(
        go.Bar(
            name="Efectivo",
            x=efectivo["week"],
            y=efectivo["precio"],
            marker_color='#9DECA2'
        )
    )

    fig.add_trace(
        go.Bar(
            name="Transferencia",
            x=transferencia["week"],
            y=transferencia["precio"],
            marker_color='#A29DEC'
        )
    )
    fig.update_layout(
        title="Ingreso por semana y método de pago",
        xaxis_title="Semana",
        yaxis_title="Monto ($)",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )


def grafico_contabilidad():
    # Use polar to create dataframe and deals with data
    df = pd.DataFrame(datos_grafico_contabilidad())
    
    # Crear la estructura del grafico
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["semana"].to_list(),
            y=df["ingresos"].to_list(),
            mode="lines+markers",
            name="Ingresos",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["semana"].to_list(),
            y=df["gastos"].to_list(),
            mode="lines+markers",
            name="Gastos",
        )
    )

    fig.update_layout(
        xaxis_title="Semana",
        yaxis_title="Monto ($)",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    grafico = fig.to_html(
        full_html=False,
        include_plotlyjs=False
        )
    
    return grafico
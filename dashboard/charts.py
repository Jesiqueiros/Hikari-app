from .queries import datos_grafico_contabilidad
import polars as pl
import polars as pl

import plotly.graph_objects as go


def grafico_contabilidad():
    # Use polar to create dataframe and deals with data
    df = pl.DataFrame(datos_grafico_contabilidad())
    
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
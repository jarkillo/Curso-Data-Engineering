"""
Dashboard de Analytics - RestaurantData Co.

Aplicación Streamlit multipágina para análisis de ventas y Business Intelligence.
Conecta al Data Warehouse creado en el Tema 1 (Modelado Dimensional).

Ejecutar con:
    streamlit run dashboard/app.py
"""

import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="RestaurantData Co. - Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Dashboard de Analytics - Master en Ingeniería de Datos"},
)

# CSS personalizado para estilo profesional
st.markdown(
    """
<style>
    /* Estilo para métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }

    /* Estilo para sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }

    /* Ocultar menú hamburguesa en producción */
    #MainMenu {visibility: hidden;}

    /* Footer personalizado */
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
        color: #666;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Verificar conexión al DWH
from database import check_dwh_exists, get_dwh_info

if not check_dwh_exists():
    st.error("""
    ⚠️ **Data Warehouse no encontrado**

    El archivo de base de datos no existe. Por favor:

    1. Ejecuta primero el proyecto del Tema 1 (Modelado Dimensional)
    2. Esto creará el archivo `data_warehouse.db` necesario

    ```bash
    cd ../tema-1-dimensional-modeling/04-proyecto-practico
    python main.py
    ```
    """)
    st.stop()

# Importar queries después de verificar conexión
import plotly.express as px
import plotly.graph_objects as go
from queries import (
    get_filtros_disponibles,
    get_kpis_principales,
    get_ventas_por_categoria,
    get_ventas_por_mes,
    get_ventas_por_region,
)

# =============================================================================
# SIDEBAR - Navegación y Filtros
# =============================================================================
st.sidebar.title("📊 Analytics Dashboard")
st.sidebar.markdown("**RestaurantData Co.**")
st.sidebar.divider()

# Navegación
page = st.sidebar.radio(
    "📂 Navegación",
    [
        "🏠 Overview",
        "📈 Análisis de Ventas",
        "👥 Análisis de Clientes",
        "🏆 Performance Vendedores",
    ],
    label_visibility="collapsed",
)

st.sidebar.divider()

# Información del DWH
with st.sidebar.expander("ℹ️ Info del Data Warehouse"):
    info = get_dwh_info()
    st.write(f"**Tamaño:** {info.get('size_mb', 0):.2f} MB")
    st.write(f"**Tablas:** {len(info.get('tables', []))}")
    for table in info.get("tables", []):
        st.write(f"  - {table}")


# =============================================================================
# PÁGINA: OVERVIEW
# =============================================================================
if page == "🏠 Overview":
    st.title("🏠 Dashboard Ejecutivo")
    st.markdown("**Vista general de KPIs y métricas principales**")

    # KPIs principales
    kpis = get_kpis_principales()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="💰 Revenue Total", value=f"${kpis.get('total_revenue', 0):,.2f}"
        )

    with col2:
        st.metric(
            label="🛒 Transacciones", value=f"{kpis.get('num_transacciones', 0):,}"
        )

    with col3:
        st.metric(
            label="🎫 Ticket Promedio", value=f"${kpis.get('ticket_promedio', 0):,.2f}"
        )

    with col4:
        st.metric(label="👥 Clientes Activos", value=f"{kpis.get('num_clientes', 0):,}")

    with col5:
        st.metric(label="📦 Productos", value=f"{kpis.get('num_productos', 0):,}")

    st.divider()

    # Gráficos principales
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Tendencia de Ventas Mensual")
        df_ventas_mes = get_ventas_por_mes()

        if len(df_ventas_mes) > 0:
            # Crear columna de fecha para el eje X
            df_ventas_mes["periodo"] = (
                df_ventas_mes["mes_nombre"] + " " + df_ventas_mes["anio"].astype(str)
            )

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df_ventas_mes["periodo"],
                    y=df_ventas_mes["total_ventas"],
                    mode="lines+markers",
                    name="Ventas",
                    line={"color": "#2E86AB", "width": 3},
                    marker={"size": 8},
                    fill="tozeroy",
                    fillcolor="rgba(46, 134, 171, 0.2)",
                )
            )

            fig.update_layout(
                xaxis_title="Período",
                yaxis_title="Ventas ($)",
                yaxis_tickformat="$,.0f",
                hovermode="x unified",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos de ventas disponibles")

    with col2:
        st.subheader("📊 Ventas por Categoría")
        df_categoria = get_ventas_por_categoria()

        if len(df_categoria) > 0:
            fig = px.pie(
                df_categoria,
                values="total_ventas",
                names="categoria",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig.update_traces(textposition="outside", textinfo="label+percent")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos de categorías disponibles")

    # Segunda fila de gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗺️ Ventas por Región")
        df_region = get_ventas_por_region()

        if len(df_region) > 0:
            fig = px.bar(
                df_region,
                x="region",
                y="total_ventas",
                color="region",
                text=df_region["total_ventas"].apply(lambda x: f"${x:,.0f}"),
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                xaxis_title="Región",
                yaxis_title="Ventas ($)",
                yaxis_tickformat="$,.0f",
                showlegend=False,
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos de regiones disponibles")

    with col2:
        st.subheader("📊 Transacciones por Mes")
        if len(df_ventas_mes) > 0:
            fig = px.bar(
                df_ventas_mes,
                x="periodo",
                y="num_transacciones",
                color="num_transacciones",
                color_continuous_scale="Blues",
            )
            fig.update_layout(
                xaxis_title="Período",
                yaxis_title="Número de Transacciones",
                showlegend=False,
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# PÁGINA: ANÁLISIS DE VENTAS
# =============================================================================
elif page == "📈 Análisis de Ventas":
    st.title("📈 Análisis de Ventas")
    st.markdown("**Análisis detallado de ventas por producto, categoría y tiempo**")

    from queries import (
        get_heatmap_dia_hora,
        get_top_productos,
        get_ventas_diarias,
        get_ventas_por_subcategoria,
    )

    # Filtros
    filtros = get_filtros_disponibles()

    col1, col2, col3 = st.columns(3)
    with col1:
        anio_sel = st.selectbox(
            "📅 Año",
            options=[None] + filtros.get("anios", []),
            format_func=lambda x: "Todos" if x is None else str(x),
        )
    with col2:
        mes_sel = st.selectbox(
            "📆 Mes",
            options=[None] + [m["mes"] for m in filtros.get("meses", [])],
            format_func=lambda x: "Todos"
            if x is None
            else next(
                (m["mes_nombre"] for m in filtros.get("meses", []) if m["mes"] == x),
                str(x),
            ),
        )
    with col3:
        cat_sel = st.selectbox(
            "📦 Categoría",
            options=[None] + filtros.get("categorias", []),
            format_func=lambda x: "Todas" if x is None else x,
        )

    st.divider()

    # Gráfico de ventas diarias
    st.subheader("📅 Ventas Diarias")
    df_diarias = get_ventas_diarias(anio=anio_sel, mes=mes_sel)

    if len(df_diarias) > 0:
        fig = px.line(
            df_diarias,
            x="fecha",
            y="total_ventas",
            title="",
            labels={"fecha": "Fecha", "total_ventas": "Ventas ($)"},
        )
        fig.update_traces(line_color="#2E86AB", line_width=2)
        fig.update_layout(yaxis_tickformat="$,.0f", height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos para los filtros seleccionados")

    # Top productos y Subcategorías
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top 10 Productos")
        df_top = get_top_productos(limit=10, categoria=cat_sel)

        if len(df_top) > 0:
            fig = px.bar(
                df_top,
                x="total_ventas",
                y="nombre_producto",
                orientation="h",
                color="categoria",
                text=df_top["total_ventas"].apply(lambda x: f"${x:,.0f}"),
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                xaxis_title="Ventas ($)",
                yaxis_title="",
                xaxis_tickformat="$,.0f",
                height=400,
                yaxis={"categoryorder": "total ascending"},
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de productos")

    with col2:
        st.subheader("🌳 Ventas por Subcategoría")
        df_sub = get_ventas_por_subcategoria()

        if len(df_sub) > 0:
            fig = px.treemap(
                df_sub,
                path=["categoria", "subcategoria"],
                values="total_ventas",
                color="total_ventas",
                color_continuous_scale="Blues",
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de subcategorías")

    # Heatmap
    st.subheader("🔥 Heatmap: Ventas por Día de Semana y Mes")
    df_heat = get_heatmap_dia_hora()

    if len(df_heat) > 0:
        # Pivotar datos para heatmap
        pivot = df_heat.pivot_table(
            index="dia_semana",
            columns="mes_nombre",
            values="total_ventas",
            aggfunc="sum",
        )

        # Ordenar días de semana
        dias_orden = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
        ]
        pivot = pivot.reindex([d for d in dias_orden if d in pivot.index])

        fig = px.imshow(
            pivot,
            labels={"x": "Mes", "y": "Día de Semana", "color": "Ventas ($)"},
            color_continuous_scale="YlOrRd",
            aspect="auto",
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# PÁGINA: ANÁLISIS DE CLIENTES
# =============================================================================
elif page == "👥 Análisis de Clientes":
    st.title("👥 Análisis de Clientes")
    st.markdown("**Segmentación, comportamiento y valor de clientes**")

    from queries import (
        get_clientes_por_segmento,
        get_rfm_analysis,
        get_top_clientes,
    )

    # Métricas de clientes
    df_segmentos = get_clientes_por_segmento()

    if len(df_segmentos) > 0:
        total_clientes = df_segmentos["num_clientes"].sum()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("👥 Total Clientes", f"{total_clientes:,}")

        with col2:
            premium = df_segmentos[df_segmentos["segmento"] == "Premium"]
            if len(premium) > 0:
                st.metric("⭐ Clientes Premium", f"{premium.iloc[0]['num_clientes']:,}")

        with col3:
            st.metric(
                "💰 Revenue Promedio/Cliente",
                f"${df_segmentos['total_compras'].sum() / max(total_clientes, 1):,.2f}",
            )

    st.divider()

    # Gráficos de segmentación
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Distribución por Segmento")

        if len(df_segmentos) > 0:
            fig = px.pie(
                df_segmentos,
                values="num_clientes",
                names="segmento",
                hole=0.4,
                color_discrete_sequence=["#2E86AB", "#A23B72", "#F18F01"],
            )
            fig.update_traces(textposition="inside", textinfo="label+percent")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💰 Revenue por Segmento")

        if len(df_segmentos) > 0:
            fig = px.bar(
                df_segmentos,
                x="segmento",
                y="total_compras",
                color="segmento",
                text=df_segmentos["total_compras"].apply(lambda x: f"${x:,.0f}"),
                color_discrete_sequence=["#2E86AB", "#A23B72", "#F18F01"],
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(yaxis_tickformat="$,.0f", showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)

    # Top clientes
    st.subheader("🏆 Top 10 Clientes por Valor")
    df_top_clientes = get_top_clientes(limit=10)

    if len(df_top_clientes) > 0:
        # Formatear columnas numéricas
        df_display = df_top_clientes.copy()
        df_display["total_compras"] = df_display["total_compras"].apply(
            lambda x: f"${x:,.2f}"
        )
        df_display["ticket_promedio"] = df_display["ticket_promedio"].apply(
            lambda x: f"${x:,.2f}"
        )

        st.dataframe(
            df_display,
            column_config={
                "nombre": "Cliente",
                "segmento": "Segmento",
                "ciudad": "Ciudad",
                "estado": "Estado",
                "total_compras": "Total Compras",
                "num_transacciones": "# Transacciones",
                "ticket_promedio": "Ticket Promedio",
            },
            hide_index=True,
            use_container_width=True,
        )

    # Análisis RFM
    st.subheader("📊 Análisis RFM (Recency, Frequency, Monetary)")
    df_rfm = get_rfm_analysis()

    if len(df_rfm) > 0:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.scatter(
                df_rfm.head(50),
                x="frequency",
                y="monetary",
                size="avg_order_value",
                color="segmento",
                hover_data=["nombre", "recency_days"],
                title="Frequency vs Monetary (Top 50 clientes)",
                labels={
                    "frequency": "Frecuencia (# compras)",
                    "monetary": "Valor Monetario ($)",
                    "segmento": "Segmento",
                },
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Distribución de recency
            fig = px.histogram(
                df_rfm,
                x="recency_days",
                nbins=20,
                title="Distribución de Recency (días desde última compra)",
                labels={"recency_days": "Días desde última compra"},
            )
            fig.update_traces(marker_color="#2E86AB")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# PÁGINA: PERFORMANCE VENDEDORES
# =============================================================================
elif page == "🏆 Performance Vendedores":
    st.title("🏆 Performance de Vendedores")
    st.markdown("**Análisis de rendimiento del equipo comercial**")

    from queries import (
        get_performance_vendedores,
        get_ventas_por_vendedor_mes,
    )

    df_vendedores = get_performance_vendedores()

    if len(df_vendedores) > 0:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👔 Total Vendedores", f"{len(df_vendedores)}")

        with col2:
            st.metric(
                "💰 Venta Promedio/Vendedor",
                f"${df_vendedores['total_ventas'].mean():,.2f}",
            )

        with col3:
            st.metric("🏆 Top Vendedor", df_vendedores.iloc[0]["nombre"])

        with col4:
            st.metric(
                "💵 Comisiones Totales",
                f"${df_vendedores['comision_total'].sum():,.2f}",
            )

        st.divider()

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Ranking de Vendedores")
            fig = px.bar(
                df_vendedores.head(10),
                x="total_ventas",
                y="nombre",
                orientation="h",
                color="region",
                text=df_vendedores.head(10)["total_ventas"].apply(
                    lambda x: f"${x:,.0f}"
                ),
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                yaxis={"categoryorder": "total ascending"},
                xaxis_tickformat="$,.0f",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("🗺️ Ventas por Región")
            df_region = (
                df_vendedores.groupby("region")
                .agg({"total_ventas": "sum", "nombre": "count"})
                .reset_index()
            )
            df_region.columns = ["region", "total_ventas", "num_vendedores"]

            fig = px.bar(
                df_region,
                x="region",
                y="total_ventas",
                color="num_vendedores",
                text=df_region["total_ventas"].apply(lambda x: f"${x:,.0f}"),
                color_continuous_scale="Blues",
                labels={"num_vendedores": "# Vendedores"},
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(yaxis_tickformat="$,.0f", height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Tabla de performance
        st.subheader("📋 Detalle de Performance")
        df_display = df_vendedores.copy()
        df_display["total_ventas"] = df_display["total_ventas"].apply(
            lambda x: f"${x:,.2f}"
        )
        df_display["ticket_promedio"] = df_display["ticket_promedio"].apply(
            lambda x: f"${x:,.2f}"
        )
        df_display["comision_total"] = df_display["comision_total"].apply(
            lambda x: f"${x:,.2f}"
        )
        df_display["comision_porcentaje"] = df_display["comision_porcentaje"].apply(
            lambda x: f"{x:.1f}%"
        )

        st.dataframe(
            df_display[
                [
                    "nombre",
                    "region",
                    "total_ventas",
                    "num_transacciones",
                    "ticket_promedio",
                    "comision_porcentaje",
                    "comision_total",
                ]
            ],
            column_config={
                "nombre": "Vendedor",
                "region": "Región",
                "total_ventas": "Total Ventas",
                "num_transacciones": "# Trans.",
                "ticket_promedio": "Ticket Prom.",
                "comision_porcentaje": "% Comisión",
                "comision_total": "Comisión Total",
            },
            hide_index=True,
            use_container_width=True,
        )

        # Evolución mensual
        st.subheader("📈 Evolución Mensual por Vendedor")
        df_mensual = get_ventas_por_vendedor_mes()

        if len(df_mensual) > 0:
            fig = px.line(
                df_mensual,
                x="mes_nombre",
                y="total_ventas",
                color="vendedor",
                markers=True,
            )
            fig.update_layout(
                xaxis_title="Mes",
                yaxis_title="Ventas ($)",
                yaxis_tickformat="$,.0f",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos de vendedores disponibles")


# =============================================================================
# FOOTER
# =============================================================================
st.sidebar.divider()
st.sidebar.markdown("""
---
📊 **Analytics Dashboard**
*Master en Ingeniería de Datos*

Módulo 8 - Tema 3
""")

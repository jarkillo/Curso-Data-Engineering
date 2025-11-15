/*
Test personalizado: Verificar que total_amount = quantity * unit_price
Detecta inconsistencias en cálculos de totales
*/

WITH order_calculations AS (
    SELECT
        order_id,
        quantity,
        unit_price,
        total_amount,
        ROUND((quantity * unit_price)::NUMERIC, 2) AS calculated_total,
        ABS(total_amount - ROUND((quantity * unit_price)::NUMERIC, 2)) AS difference
    FROM {{ ref('fct_orders') }}
)

-- Falla si hay diferencias > 0.01 (tolerancia de redondeo)
SELECT
    order_id,
    quantity,
    unit_price,
    total_amount,
    calculated_total,
    difference
FROM order_calculations
WHERE difference > 0.01

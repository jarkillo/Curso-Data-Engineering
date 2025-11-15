/*
Test personalizado: Pedidos enviados/entregados deben tener shipped_date
Detecta inconsistencias en estado vs fechas
*/

SELECT
    order_id,
    order_status,
    order_date,
    shipped_date
FROM {{ ref('fct_orders') }}
WHERE order_status IN ('shipped', 'delivered')
  AND shipped_date IS NULL

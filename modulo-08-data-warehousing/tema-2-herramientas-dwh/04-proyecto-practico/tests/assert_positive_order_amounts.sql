/*
Test personalizado: Verificar que todos los montos de pedidos sean positivos
Este test FALLA si encuentra algún registro (retorna filas)
*/

-- Test: total_amount debe ser estrictamente positivo
SELECT
    order_id,
    customer_id,
    total_amount
FROM {{ ref('fct_orders') }}
WHERE total_amount <= 0

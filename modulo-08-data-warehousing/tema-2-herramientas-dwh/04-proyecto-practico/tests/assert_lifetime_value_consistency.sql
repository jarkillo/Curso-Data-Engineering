/*
Test personalizado: Verificar consistencia entre lifetime_value y total_orders
Un cliente con lifetime_value > 0 debe tener total_orders > 0 y viceversa
*/

SELECT
    customer_id,
    full_name,
    total_orders,
    lifetime_value
FROM {{ ref('dim_customers') }}
WHERE
    -- Caso 1: Tiene valor pero no tiene pedidos
    (lifetime_value > 0 AND total_orders = 0)
    OR
    -- Caso 2: Tiene pedidos pero no tiene valor
    (total_orders > 0 AND lifetime_value = 0)

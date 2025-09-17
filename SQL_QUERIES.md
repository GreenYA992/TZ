# SQL Запросы для Order Management System

## 2.1. Сумма товаров по клиентам

```sql
SELECT c.name AS "Наименование клиента", SUM(o.total_amount) AS "Сумма"
FROM clients c
LEFT JOIN orders o ON c.id = o.client_id
GROUP BY c.id, c.name;
```

## 2.2. Количество дочерних категорий

```sql
SELECT parent.id, parent.name,
    COUNT(child.id) AS child_count
FROM categories parent
LEFT JOIN categories child ON child.parent_id = parent.id
GROUP BY parent.id, parent.name
ORDER BY parent.id;
```

## 2.3.1 Топ-5 товаров за последний месяц (с рекурсией)
```sql
WITH top_products AS (
    SELECT p.id, p.name AS product_name, (
        SELECT name FROM categories WHERE id = (
            WITH RECURSIVE category_path AS (
                SELECT id, parent_id, name
                    FROM categories
                    WHERE id = p.category_id
                    UNION ALL
                    SELECT c.id, c.parent_id, c.name
                    FROM categories c
                    INNER JOIN category_path cp ON c.id = cp.parent_id
                )
                SELECT id FROM category_path WHERE parent_id IS NULL
            )
        ) AS top_level_category_name,
        SUM(oi.quantity) AS total_sold
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN products p ON oi.product_id = p.id
    WHERE o.created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
      AND o.created_at < DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY p.id, p.name
    ORDER BY total_sold DESC
    LIMIT 5
)
SELECT * FROM top_products;
```

## 2.3.2 Оптимизированная версия

### Можно добавить в models (class Product(Base):) 

- **main_category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)**
- **Далее, запрос будет выглядеть так:**

```sql
SELECT p.name AS "Наименование товара", c.name AS "Категория 1-го уровня", 
    SUM(oi.quantity) AS "Общее количество проданных штук"
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
LEFT JOIN categories c ON p.top_category_id = c.id
WHERE o.created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  AND o.created_at < DATE_TRUNC('month', CURRENT_DATE)
GROUP BY p.id, p.name, c.name
ORDER BY SUM(oi.quantity) DESC
LIMIT 5;
```
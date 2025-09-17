Данные локальные, поэтому гружу без .gitignore
Для подключения к своей БД, нужно просто поменять данные в .env

Для добавления тестовых файлов, запустить app/add_db.py
Для создания таблиц БД запустить run.py

SQL запросы, по заданию 2 

2.1
SELECT c.name AS "Наименование клиента",
    SUM(o.total_amount) AS "Сумма"
FROM clients c
LEFT JOIN orders o ON c.id = o.client_id
GROUP BY c.id, c.name;

2.2
SELECT parent.id, parent.name,
    COUNT(child.id) AS child_count
FROM categories parent
LEFT JOIN categories child ON child.parent_id = parent.id
GROUP BY parent.id, parent.name
ORDER BY parent.id;

2.3.1
WITH top_products AS (
    SELECT 
        p.id,
        p.name AS product_name,
        -- Получаем категорию 1-го уровня
        (
            SELECT name FROM categories WHERE id = (
                -- Поднимаемся по иерархии вверх, пока не найдем корень
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
    -- Фильтр по дате: заказы за последний полный месяц
    WHERE o.created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
      AND o.created_at < DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY p.id, p.name
    ORDER BY total_sold DESC
    LIMIT 5
)
SELECT * FROM top_products;

2.3.2
Можно добавить в models (class Product(Base):)
main_category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

Далее, запрос будет выглядеть так:

SELECT p.name AS "Наименование товара", c.name AS "Категория 1-го уровня", 
    SUM(oi.quantity) AS "Общее количество проданных штук"
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
LEFT JOIN categories c ON p.top_category_id = c.id  -- Простой JOIN!
WHERE o.created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  AND o.created_at < DATE_TRUNC('month', CURRENT_DATE)
GROUP BY p.id, p.name, c.name
ORDER BY SUM(oi.quantity) DESC
LIMIT 5;

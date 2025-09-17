import asyncio
from app.database import AsyncSessionLocal
from app import models


async def add_to_data():
    """Добавление тестовых данных в базу"""
    async with AsyncSessionLocal() as session:
        # 1. Создаем категории
        categories = [
            models.Category(name="Электроника"),
            models.Category(name="Бытовая техника"),
            models.Category(name="Одежда"),
            models.Category(name="Книги"),
            models.Category(name="Спорт"),
        ]

        session.add_all(categories)
        await session.flush()  # Получаем ID

        # 2. Создаем дочерние категории
        child_categories = [
            # Дочерние для Электроники (ID=1)
            models.Category(name="Смартфоны", parent_id=1),
            models.Category(name="Ноутбуки", parent_id=1),
            models.Category(name="Телевизоры", parent_id=1),

            # Дочерние для Бытовой техники (ID=2)
            models.Category(name="Холодильники", parent_id=2),
            models.Category(name="Стиральные машины", parent_id=2),
            models.Category(name="Микроволновки", parent_id=2),

            # Дочерние для Одежды (ID=3)
            models.Category(name="Мужская одежда", parent_id=3),
            models.Category(name="Женская одежда", parent_id=3),

            # Дочерние для Книг (ID=4)
            models.Category(name="Художественная литература", parent_id=4),
            models.Category(name="Научная литература", parent_id=4),
        ]

        session.add_all(child_categories)
        await session.flush()

        # 3. Создаем клиентов
        clients = [
            models.Client(name="Иван Петров", address="ул. Ленина, 10, кв. 5"),
            models.Client(name="Мария Сидорова", address="пр. Мира, 25, кв. 12"),
            models.Client(name="Алексей Козлов", address="ул. Садовая, 3, кв. 7"),
            models.Client(name="Екатерина Васнецова", address="ул. Центральная, 15, кв. 9"),
            models.Client(name="Дмитрий Орлов", address="пр. Победы, 40, кв. 3"),
        ]

        session.add_all(clients)
        await session.flush()

        # 4. Создаем товары
        products = [
            # Смартфоны (ID=6)
            models.Product(name="iPhone 14", quantity=15, price=799.99, category_id=6),
            models.Product(name="Samsung Galaxy S23", quantity=20, price=699.99, category_id=6),

            # Ноутбуки (ID=7)
            models.Product(name="MacBook Pro 16", quantity=8, price=2499.99, category_id=7),
            models.Product(name="Dell XPS 15", quantity=12, price=1899.99, category_id=7),

            # Телевизоры (ID=8)
            models.Product(name="Samsung QLED 55", quantity=10, price=899.99, category_id=8),

            # Холодильники (ID=9)
            models.Product(name="Холодильник Bosch", quantity=7, price=799.99, category_id=9),

            # Стиральные машины (ID=10)
            models.Product(name="Стиральная машина LG", quantity=11, price=499.99, category_id=10),

            # Мужская одежда (ID=12)
            models.Product(name="Джинсы Levi's", quantity=25, price=89.99, category_id=12),

            # Женская одежда (ID=13)
            models.Product(name="Платье летнее", quantity=22, price=59.99, category_id=13),

            # Художественная литература (ID=14)
            models.Product(name="Война и мир", quantity=35, price=19.99, category_id=14),

            # Научная литература (ID=15)
            models.Product(name="Python для начинающих", quantity=20, price=39.99, category_id=15),
        ]

        session.add_all(products)
        await session.flush()

        # 5. Создаем заказы
        orders = [
            models.Order(client_id=1, status="created"),
            models.Order(client_id=2, status="created"),
            models.Order(client_id=3, status="processing"),
        ]

        session.add_all(orders)

        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_to_data())
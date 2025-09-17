from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app import models, schemas
from typing import Optional


async def get_product(db: AsyncSession, product_id: int) -> Optional[models.Product]:
    """Получить товар по ID"""
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def get_products_in_stock(db: AsyncSession, product_id: int, quantity: int) -> bool:
    """Проверить, есть ли товар в наличии в нужном количестве"""
    result = await db.execute(
        select(models.Product.quantity).where(
            and_(
                models.Product.id == product_id,
                models.Product.quantity >= quantity
            )
        )
    )
    return result.scalar() is not None


async def update_product_quantity(db: AsyncSession, product_id: int, quantity_change: int):
    """Обновить количество товара на складе"""
    await db.execute(
        update(models.Product)
        .where(models.Product.id == product_id)
        .values(quantity=models.Product.quantity + quantity_change)
    )


async def get_order(db: AsyncSession, order_id: int) -> Optional[models.Order]:
    """Получить заказ со всеми связанными данными"""
    result = await db.execute(
        select(models.Order)
        .where(models.Order.id == order_id)
        .options(
            selectinload(models.Order.client),
            selectinload(models.Order.items).selectinload(models.OrderItem.product)
        )
    )
    return result.scalar_one_or_none()


async def get_order_item(db: AsyncSession, order_id: int, product_id: int) -> Optional[models.OrderItem]:
    """Получить позицию в заказе"""
    result = await db.execute(
        select(models.OrderItem).where(
            and_(
                models.OrderItem.order_id == order_id,
                models.OrderItem.product_id == product_id
            )
        )
    )
    return result.scalar_one_or_none()


async def create_order_item(db: AsyncSession, order_item: schemas.OrderItemCreate, order_id: int):
    """Создать новую позицию в заказе"""
    db_order_item = models.OrderItem(**order_item.dict(), order_id=order_id)
    db.add(db_order_item)
    await db.flush()
    return db_order_item


async def update_order_item_quantity(db: AsyncSession, order_item: models.OrderItem, quantity: int):
    """Обновить количество товара в позиции заказа"""
    order_item.quantity += quantity
    await db.flush()


async def update_order_total(db: AsyncSession, order_id: int):
    """Пересчитать общую сумму заказа"""
    result = await db.execute(
        select(models.OrderItem.quantity * models.OrderItem.price)
        .where(models.OrderItem.order_id == order_id)
    )
    total = sum([row[0] for row in result.all()] or [0])

    await db.execute(
        update(models.Order)
        .where(models.Order.id == order_id)
        .values(total_amount=total)
    )
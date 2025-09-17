from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.database import engine, get_async_db

app = FastAPI(
    title="Order Management API",
    description="API для управления заказами и товарами",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():
    """Создание таблиц при запуске приложения"""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.post("/orders/{order_id}/items/", response_model=schemas.Order)
async def add_item_to_order(
        request: schemas.AddItemRequest,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Добавление товара в заказ.
    Если товар уже есть в заказе - увеличивает количество.
    Если товара нет в наличии - возвращает ошибку.
    """
    # 1. Проверить существование заказа
    order = await crud.get_order(db, request.order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # 2. Проверить наличие товара на складе
    if not await crud.get_products_in_stock(db, request.product_id, request.quantity):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough products in stock"
        )

    # 3. Проверить, есть ли товар уже в заказе
    existing_item = await crud.get_order_item(db, request.order_id, request.product_id)

    if existing_item:
        # Обновляем количество в существующей позиции
        await crud.update_order_item_quantity(db, existing_item, request.quantity)
    else:
        # Создаем новую позицию
        product = await crud.get_product(db, request.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        order_item_data = schemas.OrderItemCreate(
            product_id=request.product_id,
            quantity=request.quantity,
            price=product.price
        )
        await crud.create_order_item(db, order_item_data, request.order_id)

    # 4. Обновляем количество товара на складе
    await crud.update_product_quantity(db, request.product_id, -request.quantity)

    # 5. Пересчитываем общую сумму заказа
    await crud.update_order_total(db, request.order_id)
    await db.commit()

    # 6. Возвращаем обновленный заказ
    return await crud.get_order(db, request.order_id)


@app.get("/")
async def root():
    return {"message": "Order Management API is running"}
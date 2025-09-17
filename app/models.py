from sqlalchemy import Column, Integer, String, ForeignKey, Text, Numeric, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# Модель Категории
class Category(Base):
    __tablename__ = "categories"  # Имя таблицы в БД

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False) # название
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True) # ID родителя
    created_at = Column(DateTime, default=datetime.utcnow) # дата создания

    # Связи (для удобства работы в Python)
    children = relationship("Category", backref="parent", remote_side=[id]) # дети
    products = relationship("Product", back_populates="category") # товары

# Модель Товара (Номенклатуры)
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False) # название
    quantity = Column(Integer, nullable=False, default=0) # количество
    price = Column(Numeric(10, 2), nullable=False) # цена
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True) # ID категории
    created_at = Column(DateTime, default=datetime.utcnow) # дата создания

    # Связи
    category = relationship("Category", back_populates="products") # категории
    order_items = relationship("OrderItem", back_populates="product") # позиции заказа

# Модель Клиента
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    orders = relationship("Order", back_populates="client")

# Модель Заказа
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default='created')
    total_amount = Column(Numeric(10, 2), default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

# Модель Позиции в Заказе
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # Цена на момент покупки
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    # Уникальный constraint (чтобы не было дублей товара в заказе)
    __table_args__ = (UniqueConstraint('order_id', 'product_id', name='_order_product_uc'),)
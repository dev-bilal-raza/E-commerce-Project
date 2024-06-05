from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.stock_model import Stock, Order
from datetime import datetime
from dateutil import relativedelta
from app.db.db_connector import DB_SESSION


def update_product_stock(session: Session, product_id: int, quantity: int) -> Stock:
    product = session.exec(select(Stock).where(
        Stock.product_id == product_id)).one_or_none()
    if product:
        product.stock = quantity
        session.commit()
        session.refresh(product)
        return product
    raise HTTPException(status_code=400, detail="Product not found")


def get_all_products_stock(session: DB_SESSION) -> list[dict]:
    stock_table = session.exec(select(Stock)).all()
    stocks = []
    if stock_table:
        for stock in stock_table:
            stocks.append(
                {
                    "product_name": stock.product_table.product_name,
                    "stock": stock.stock,
                    "stock_level": stock.stock_level
                }
            )
        return stocks
    raise HTTPException(status_code=400, detail="Product not found")


def get_specific_product_stock(product_id: int, session: DB_SESSION) -> dict:
    stock_table = session.exec(select(Stock).where(
        Stock.product_id == product_id)).one_or_none()
    if stock_table:
        return {
            "product_name": stock_table.product_table.product_name,
            "stock": stock_table.stock,
            "stock_level": stock_table.stock_level
        }
    raise HTTPException(status_code=400, detail="Product not found")


def get_stock_level(month: int, product_id: int, session: DB_SESSION):
    now_date: datetime = datetime.now()
    month_earlier: datetime = now_date - relativedelta(month=month)
    orders = session.exec(select(Order)
                          .where(Order.product_id == product_id)
                          .where(Order.created_at > month_earlier)
                          .where(Order.created_at < now_date)
                          ).all()
    stock = session.exec(select(Stock).where(
        Stock.product_id == product_id)).one_or_none()

    total_quantity_in_orders = sum(order.quantity for order in orders)

    stock_threshold = 1.2  # Maintain a buffer of 20% extra stock

    if stock.stock > total_quantity_in_orders * stock_threshold:
        recommendation = "Stock is sufficient for current demand."
    elif stock.stock >= total_quantity_in_orders:
        # New recommendation for near depletion
        recommendation = "Monitor stock levels closely."
    else:
        recommendation = "Increase stock levels."
    # Return a dictionary with relevant data and recommendation
    return {
        "product_name": stock.product_table.product_name,
        "total_orders": total_quantity_in_orders,
        "current_stock": stock.stock,
        "recommendation": recommendation
    }

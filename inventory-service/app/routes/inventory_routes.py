from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.controllers.stock_controller import (
    update_product_stock, get_stock_level, get_all_products_stock, get_specific_product_stock)
from app.models.stock_model import Stock

router = APIRouter()

@router.put("/inventory_update", response_model=Stock)
async def update_inventory(stock_table: Annotated[Stock, Depends(update_product_stock)]):
    if not stock_table:
        HTTPException(
            status_code=400, detail="Try again, something occurred while updating stock. ")
    return stock_table


@router.get("/get_stock_level", response_model=dict)
def get_stock_status(stock_information: Annotated[dict, Depends(get_stock_level)]):
    if not stock_information:
        HTTPException(
            status_code=400, detail="Try again, something occurred while getting status from stock table. ")
    return stock_information


@router.get("/get_specific_product_stock", response_model=dict)
def get_stock_st(stock_information: Annotated[dict, Depends(get_specific_product_stock)]):
    if not stock_information:
        HTTPException(
            status_code=400, detail="Try again, something occurred while getting status from stock table. ")
    return stock_information


@router.get("/get_all_products_stock", response_model=list[dict])
def get_stock(stock_information: Annotated[list[dict], Depends(get_all_products_stock)]):
    if not stock_information:
        HTTPException(
            status_code=400, detail="Try again, something occurred while getting status from stock table. ")
    return stock_information
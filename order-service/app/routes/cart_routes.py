from typing import List, Annotated
from fastapi import APIRouter, Depends
from app.models.cart_models import CartItem
from app.controllers.cart_crud_controllers import (
    add_cart_item_func, get_cart_details_func, update_cart_item_func, delete_cart_item_func
)

router = APIRouter()


@router.post("/add-cart-item", response_model=str)
def add_cart_item(message: Annotated[str, Depends(add_cart_item_func)]):
    return message


@router.get("/get-cart-details", response_model=List[dict])
def get_cart_details(cart_details: Annotated[List[dict], Depends(get_cart_details_func)]):
    return cart_details


@router.put("/update-cart-item", response_model=CartItem)
def update_cart_item(updated_cart_details: Annotated[CartItem, Depends(update_cart_item_func)]):
    return updated_cart_details


@router.delete("/delete-cart-item", response_model=str)
def delete_cart_item(message: Annotated[str, Depends(delete_cart_item_func)]):
    return message

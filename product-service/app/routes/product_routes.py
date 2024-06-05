from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from app.models.product_model import Product
from app.controllers.product_controller import create_product_func, get_product_func, update_product_func, delete_product_func, get_all_products_func, search_products_func

router = APIRouter()


@router.post("/create-category/", response_model=Product)
def create_category(category: Annotated[Product, Depends(create_category_func)]):
    if not category:
        raise HTTPException(status_code=500, detail="Some things went wrong, while creating product.")
    return category


@router.post("/create-product/", response_model=Product)
def create_product(product: Annotated[Product, Depends(create_product_func)]):
    if not product:
        raise HTTPException(status_code=500, detail="Some things went wrong, while creating product.")
    return product

@router.get("/get_product/{product_id}", response_model=Product)
def get_product(product: Annotated[Product, Depends(get_product_func)]):
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/get_all_products/", response_model=list[Product])
def get_all_products(products: Annotated[list[Product], Depends(get_all_products_func)]):    
    if not products:
        raise HTTPException(status_code=404, detail="Try again, products has not fetched.")
    return products

@router.put("/update_product/{product_id}", response_model=Product)
def update_product(product: Annotated[Product, Depends(update_product_func)]):
    if not product:
        raise HTTPException(status_code=404, detail="Try again, products has not updated.")
    return product

@router.get("/search_products/{name}", response_model=list[Product])
def search_products(products: Annotated[list[Product], Depends(search_products_func)]):
    if not products:
        raise HTTPException(status_code=404, detail="Try again, products has not fetched.")
    return products

@router.delete("/delete_product/{product_id}", response_model=int)
def delete_product(product_id: Annotated[int, Depends(delete_product_func)]):
    if not product_id:
        raise HTTPException(status_code=404, detail=f"Try again, products has not deleted with id {product_id}")
    return f"The {product_id} id of product has been deleted successfully."

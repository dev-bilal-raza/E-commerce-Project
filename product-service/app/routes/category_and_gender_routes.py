from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from app.models.product_model import Product
from app.controllers.product_controller import create_product_fun

router = APIRouter()


@router.post("/create-category/", response_model=Product)
def create_category(category: Annotated[Product, Depends(create_category_func)]):
    if not category:
        raise HTTPException(status_code=500, detail="Some things went wrong, while creating product.")
    return category

# 1) create gender route -> admin


# 2) create category route -> admin

# 3) update category route -> admin

# 4) update gender route -> admin

# 5) get genders route -> user

# 6) get categories route -> user

# 7) get specific gender products route -> user

# 8) get specific category products route -> user

 
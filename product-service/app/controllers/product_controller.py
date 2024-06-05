from typing import Annotated, List
from fastapi import Depends, HTTPException, File, UploadFile
from sqlmodel import select
from app.db.db_connector import DB_SESSION
from app.models.product_model import Product, ProductItem, ProductFormModel, Stock
from app.config.auth_admin import admin_required
import cloudinary  # type:ignore


def create_product_func(
    product_details: ProductFormModel,
    session: DB_SESSION,
    admin_verification: Annotated[dict, Depends(admin_required)],
    images: List[UploadFile] = File(...),
):
    # Check if the user is an admin
    if not admin_verification:
        raise HTTPException(
            status_code=400, detail="You are not authorized to create a product!")
    if len(product_details.product_items) != len(images):
        raise HTTPException(
            status_code=400, detail="Number of images does not match number of product items")

    product_item_tables: List[ProductItem] = []

    # Verify that product details are provided
    if not product_details:
        # Raise an HTTP 404 exception if product details are not found
        raise HTTPException(
            status_code=404, detail="Product details not found!")
    try:
        # Loop through each product item in the provided details
        for product_item, image in zip(product_details.product_items, images):

            try:
                result = cloudinary.uploader.upload(image.file)
                image_url = result["secure_url"]
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
            # Create a Stock instance for the product item
            stock_table = Stock(stock=product_item.stock)
            # Create a ProductItem instance
            product_item_table = ProductItem(
                color=product_item.color,
                price=product_item.price,
                image_url=image_url,
                stock=stock_table
            )
            # Append the ProductItem instance to the list
            product_item_tables.append(product_item_table)

        print("All ProductItems created: ", product_item_tables)

        # Create a Product instance with the list of ProductItem instances
        product_table = Product(
            product_name=product_details.product_name,
            description=product_details.description,
            product_items=product_item_tables
        )

        # Add the Product instance to the session and commit the transaction
        session.add(product_table)
        session.commit()
        session.refresh(product_table)

        return product_table

    except Exception as e:
        print("Error while creating Product:", e)
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the product.")


def get_product_func(product_id: int, session: DB_SESSION):
    product = session.exec(select(Product).where(
        Product.product_id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def get_all_products_func(session: DB_SESSION):
    products = session.exec(select(Product)).all()
    return products


def update_product_func(product_id: int, updated_product: Product, session: DB_SESSION, admin_verification: Annotated[dict, Depends(admin_required)]):
    if not admin_verification:
        HTTPException(status_code=400,
                      detail="You are not authorized to create a product!")
    product = session.exec(select(Product).where(
        Product.product_id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in updated_product.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def search_products_func(name: str, session: DB_SESSION):
    products = session.exec(select(Product).where(
        Product.product_name == name)).all()
    return products


def delete_product_func(product_id: int, session: DB_SESSION, admin_verification: Annotated[dict, Depends(admin_required)]):

    if not admin_verification:
        HTTPException(status_code=400,
                      detail="You are not authorized to create a product!")
    product = session.exec(select(Product).where(
        Product.product_id == product_id)).one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return product_id

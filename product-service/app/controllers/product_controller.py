from typing import Annotated, List
from fastapi import Depends, HTTPException, File, UploadFile
from sqlmodel import select
from app.db.db_connector import DB_SESSION
from app.controllers.category_controller import search_algorithm_func
from app.models.product_model import Product, ProductItem, ProductFormModel, Stock, ProductSize
from app.config.auth_admin import admin_required
import cloudinary  # type:ignore
import copy
from sqlalchemy import or_


def create_product_func(
    product_details: ProductFormModel,
    session: DB_SESSION,
    admin_verification: Annotated[dict, Depends(admin_required)],
    images: List[UploadFile] = File(...),
):
    """
    Create a new product in the database.

    Args:
        product_details (ProductFormModel): Details of the product to be created.
        session (DB_SESSION): Database session for performing operations.
        admin_verification (dict): Admin verification dictionary obtained via dependency injection.
        images (List[UploadFile]): List of images to be uploaded.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If the number of images does not match the number of product items.
        HTTPException: If product details are not provided.
        HTTPException: If an error occurs during image upload.
        HTTPException: If an error occurs while creating the product.

    Returns:
        Product: The created product.
    """
    # Check if the user is an admin
    if not admin_verification:
        raise HTTPException(
            status_code=403, detail="You are not authorized to create a product!"
        )

    # Check if the number of images matches the number of product items
    if len(product_details.product_items) != len(images):
        raise HTTPException(
            status_code=400, detail="Number of images does not match number of product items."
        )

    # Verify that product details are provided
    if not product_details:
        raise HTTPException(
            status_code=400, detail="Product details not found!"
        )

    product_item_tables: List[ProductItem] = []

    try:
        # Loop through each product item in the provided details
        for product_item, image in zip(product_details.product_items, images):
            try:
                # Upload the image to Cloudinary
                result = cloudinary.uploader.upload(image.file)
                image_url = result["secure_url"]
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

            # List to hold ProductSize instances
            product_size_tables: List[ProductSize] = []
            for product_size in product_item.sizes:
                # Create a Stock instance for the product item
                stock_table = Stock(stock=product_size.stock)
                # Create a ProductSize instance
                product_size_schema = ProductSize(
                    product_size=product_size.size, price=product_size.price, stock=stock_table
                )
                # Append the ProductSize instance to the list
                product_size_tables.append(product_size_schema)

            # Create a ProductItem instance
            product_item_table = ProductItem(
                color=product_item.color,  # Include the color attribute
                image_url=image_url,
                sizes=product_size_tables
            )
            # Append the ProductItem instance to the list
            product_item_tables.append(product_item_table)

        print("All ProductItems created: ", product_item_tables)

        # Create a Product instance with the list of ProductItem instances
        product_table = Product(
            product_name=product_details.product_name,
            description=product_details.product_description,
            product_type=product_details.product_type,
            duration=product_details.duration,
            advance_payment_percentage=product_details.advance_payment_percentage,
            gender_id=product_details.gender_id,
            category_id=product_details.category_id,
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
            status_code=500, detail="An error occurred while creating the product."
        )


def get_product_func(product_id: int, session: DB_SESSION):
    product = session.exec(select(Product).where(
        Product.product_id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def get_all_products_func(session: DB_SESSION):
    products = session.exec(select(Product)).all()
    return products


def get_limited_products_func(limit: int, session: DB_SESSION):
    products = session.exec(select(Product).limit(limit)).all()
    return products


def search_products_func(input: str, session: DB_SESSION):

    categories = search_algorithm_func(input, session)
    category_ids = [category.category_id for category in categories]
    if category_ids:
        category_conditions = [Product.category_id ==
                               category_id for category_id in category_ids]

        products_by_category = session.exec(
            select(Product).where(or_(*category_conditions)))
    else:
        products_by_category = []

    products_by_input = session.exec(select(Product).where(
        (input in Product.product_name) or (
            input in Product.product_description)
    )).all()

    all_products_set = set(products_by_input).union(products_by_category)
    all_products = list(all_products_set)
    return all_products


def update_product_func(product_id: int, updated_product: Product, session: DB_SESSION, admin_verification: Annotated[dict, Depends(admin_required)]):
    if not admin_verification:
        HTTPException(status_code=400,
                      detail="You are not authorized to update a product!")
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

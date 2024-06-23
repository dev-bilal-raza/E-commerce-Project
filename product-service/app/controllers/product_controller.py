from typing import Annotated, List
from fastapi import Depends, HTTPException, File, UploadFile
from sqlmodel import select
from app.db.db_connector import DB_SESSION
from app.controllers.category_controller import search_category_func
from app.models.product_model import Product, ProductItem, ProductFormModel, Stock, ProductSize, ProductImage
from app.utils.auth_admin import admin_required
from app.config.s3_configuration import upload_files_in_s3
from sqlalchemy import or_


def create_product_func(
    session: DB_SESSION,
    admin_verification: Annotated[dict, Depends(admin_required)],
    product_details: ProductFormModel,
):
    """
    Create a new product in the database.

    Args:
        product_details (ProductFormModel): Details of the product to be created.
        session (DB_SESSION): Database session for performing operations.
        admin_verification (dict): Admin verification dictionary obtained via dependency injection.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If product details are not provided.
        HTTPException: If an error occurs while creating the product.

    Returns:
        Product: The created product.
    """
    # Check if the user is an admin
    if not admin_verification:
        raise HTTPException(
            status_code=403, detail="You are not authorized to create a product!"
        )

    # Verify that product details are provided
    if not product_details:
        raise HTTPException(
            status_code=400, detail="Product details not found!"
        )
    print(f"Product Details: f{product_details}")
    product_item_tables: List[ProductItem] = []

    try:
        # Loop through each product item in the provided details
        for product_item in product_details.product_items:
            # List to hold ProductSize instances
            product_size_tables: List[ProductSize] = []
            for product_size in product_item.sizes:
                # Create a Stock instance for the product item
                stock_table = Stock(stock=product_size.stock)
                print(f"Stock Level: {stock_table.stock_level}")
                # Create a ProductSize instance
                product_size_schema = ProductSize(
                    size_id=product_size.size, price=product_size.price, stock=stock_table
                )
                # Append the ProductSize instance to the list
                product_size_tables.append(product_size_schema)

            # Create a ProductItem instance
            product_item_table = ProductItem(
                color=product_item.color,  # Include the color attribute
                sizes=product_size_tables
            )
            # Append the ProductItem instance to the list
            product_item_tables.append(product_item_table)

        print("All ProductItems created: ", product_item_tables)

        # Create a Product instance with the list of ProductItem instances
        product_table = Product(
            product_name=product_details.product_name,
            product_description=product_details.product_description,
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


def add_images_in_productitem_func(
    product_item_id: int,
    session: DB_SESSION,
    admin_verification: Annotated[dict, Depends(admin_required)],
    images: List[UploadFile] = File(...)
):

    # Check if the user is an admin
    if not admin_verification:
        raise HTTPException(
            status_code=403, detail="You are not authorized to create a product!"
        )
    product_item = session.exec(select(ProductItem).where(
        ProductItem.item_id == product_item_id)).one_or_none()
    if not product_item:
        raise HTTPException(
            status_code=404, detail=f"Product item not found from id: {product_item_id}")
    image_urls = upload_files_in_s3(images, product_item.product_id)

    product_images_table = [ProductImage(
        product_image_url=url) for url in image_urls]
    print(f"All Product Images : {product_images_table}")
    product_item.product_images = product_images_table
    session.add(product_item)
    session.commit()
    session.refresh(product_item)
    return f"Images has been successfully added."


def get_product_func(product_id: int, session: DB_SESSION):
    product = session.exec(select(Product).where(
        Product.product_id == product_id)).one_or_none()
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

    categories = search_category_func(input, session)
    category_ids = [category.category_id for category in categories]
    if category_ids:
        category_conditions = [Product.category_id ==
                               category_id for category_id in category_ids]

        products_by_category = session.exec(
            select(Product).where(or_(*category_conditions))).all()
    else:
        products_by_category = []

    products_by_input = session.exec(select(Product).where(
        (input in Product.product_name) or (
            input in Product.product_description)
    )).all()

    all_products_set = set(products_by_input).union(products_by_category)
    all_products = list(all_products_set)
    return all_products


def update_product_func(
    product_id: int,
    updated_product: Product,
    session: DB_SESSION,
    admin_verification: Annotated[dict, Depends(admin_required)]
):
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


def delete_product_func(
    product_id: int,
    session: DB_SESSION,
    admin_verification: Annotated[dict, Depends(admin_required)]
):

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

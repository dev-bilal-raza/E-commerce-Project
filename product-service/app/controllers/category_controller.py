from typing import Annotated
from sqlmodel import select
from fastapi import Depends, HTTPException
from app.utils.auth_admin import admin_required
from app.models.categories_model import Category, Gender, Size
from app.models.product_model import Product, ProductItem, ProductSize
from app.db.db_connector import DB_SESSION


def create_category_func(
        category_name: str,
        session: DB_SESSION,
        admin_verification: Annotated[dict, Depends(admin_required)]
):

    # Check if the user is an admin
    if not admin_verification:
        raise HTTPException(
            status_code=403, detail="You are not authorized to create a product!"
        )

    category = Category(category_name=category_name)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def add_gender_func(
    gender_name: str | int,
    session: DB_SESSION,
    admin_verification: Annotated[dict, Depends(admin_required)]
):
    # Check if the user is an admin
    if not admin_verification:
        raise HTTPException(
            status_code=403, detail="You are not authorized to create a product!"
        )
    gender = Gender(gender_name=gender_name)
    if not gender:
        raise HTTPException(status_code=404, detail="category not found")
    session.add(gender)
    session.commit()
    session.refresh(gender)
    return gender


def search_products_by_category_func(category_id: int, session: DB_SESSION):
    if category_id:
        products = session.exec(select(Product).where(
            Product.category_id == category_id)).all()
        if products:
            return products
        raise HTTPException(
            status_code=404, detail=f"Product not found from this category id: {category_id}")
    raise HTTPException(
        status_code=404, detail="you have not entered the category id")


def search_products_by_gender_func(gender_id: int, session: DB_SESSION):
    if gender_id:
        products = session.exec(select(Product).where(
            Product.gender_id == gender_id)).all()
        if products:
            return products
        raise HTTPException(
            status_code=404, detail=f"Product not found from this gender id: {gender_id}")
    raise HTTPException(
        status_code=404, detail="You have not entered the gender id")


def get_categories_func(session: DB_SESSION):
    categories = session.exec(select(Category)).all()
    if categories:
        return categories
    raise HTTPException(status_code=404, detail="Categories not found")


def get_genders_func(session: DB_SESSION):
    genders = session.exec(select(Gender)).all()
    if genders:
        return genders
    raise HTTPException(status_code=404, detail="Genders not found")


def search_category_func(input: str, session: DB_SESSION):
    categories = session.exec(select(Category).where(
        Category.category_name.startswith(input))).all()
    if categories:
        return categories
    return "Category could not be found."


def create_size_func(
    size_name: str | int,
    session: DB_SESSION,
    admin_verification: Annotated[dict, Depends(admin_required)]
):
    # Check if the user is an admin
    if not admin_verification:
        raise HTTPException(
            status_code=403, detail="You are not authorized to create a product!"
        )

    size_table = Size(size=size_name)
    session.add(size_table)
    session.commit()
    session.refresh(size_table)
    return size_table


def search_specific_size_products_func(size_id: int, session: DB_SESSION):
    # Main query to get the first ProductItem for each Product with the given size_id
    results = session.exec(
        select(ProductItem)
        .join(ProductSize)
        .where(ProductSize.size_id == size_id)
        .distinct()
    ).all()

    return results

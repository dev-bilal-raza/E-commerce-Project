# 1) create gender function -> admin
from typing import Annotated, List
from sqlmodel import select
from fastapi import Depends, HTTPException
from app.models.categories_model import Category, Gender, SizeCategories, Size
from app.models.product_model import Product
from app.db.db_connector import DB_SESSION


def create_category_func(category_name: str, session: DB_SESSION):
    category = Category(category_name=category_name)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


# 2) create category function -> admin
def add_gender_func(gender_name: str | int, session: DB_SESSION):
    gender = Gender(gender_name=gender_name)
    if not gender:
        raise HTTPException(status_code=404, detail="category not found")
    session.add(gender)
    session.commit()
    session.refresh(gender)
    return gender

def search_products_by_category(category_id: int, session: DB_SESSION):
    if category_id:
        products = session.exec(select(Product).where(Product.category_id==category_id)).all()
        if products:
            return products
        raise HTTPException(status_code=404, detail=f"Product not found from this category id: {category_id}")
    raise HTTPException(status_code=404, detail="you have not entered the category id")

def search_products_by_gender(gender_id: int, session: DB_SESSION):
    if gender_id:
        products = session.exec(select(Product).where(Product.gender_id==gender_id)).all()
        if products:
            return products
        raise HTTPException(status_code=404, detail=f"Product not found from this gender id: {gender_id}")
    raise HTTPException(status_code=404, detail="You have not entered the gender id")


def get_categories(session: DB_SESSION):
    categories= session.exec(select(Category)).all()
    if categories:
        return categories
    raise HTTPException(status_code=404, detail="Categories not found")


def get_genders(session: DB_SESSION):
    genders= session.exec(select(Gender)).all()
    if genders:
        return genders
    raise HTTPException(status_code=404, detail="Genders not found")

def search_algorithm_func(input: str, session: DB_SESSION):
    categories = session.exec(select(Category).where(Category.category_name.startswith(input))).all()
    if categories:
        return categories
    return "Category could not be found."


# 3) update category function -> admin

# 4) update gender function -> admin

# 5) get genders function -> user

# 6) get categories function -> user

# 7) get specific gender products function -> user

# 8) get specific category products function -> user

 
from __future__ import annotations

from typing import List, Dict, Optional, Any
from pydantic import BaseModel


class StoreDTO(BaseModel):
    """
    Data Transfer Object representing a store.
    
    Attributes:
        id (int): Unique identifier for the store.
        name (str): Name of the store.
    """
    id: int
    name: str
    query: str = None


class CategoryDTO(BaseModel):
    """
    Data Transfer Object representing a product category.
    
    Attributes:
        store (StoreDTO): The store that contains this category.
        category_id (int): Unique identifier for the category.
        name (str): Name of the category.
        path (str): URL path to the category.
    """
    store: StoreDTO
    category_id: int = 0
    name: str = None
    path: str = None


class ProductDTO(BaseModel):
    """
    Data Transfer Object representing a product within a category.
    
    Attributes:
        category (CategoryDTO): The category containing this product.
        id (int): Unique identifier for the product.
        name (str): Name of the product.
        photos (List[str]): List of URLs to product photos.
        price_basic (int): Base price of the product.
        price_with_discount (Optional[int]): Discounted price if applicable.
        discount_size (Optional[int]): Size of discount in percentage or currency.
        quantity_rate (Optional[int]): Quantity rating based on reviews.
    """
    category: CategoryDTO = None
    id: int
    name: str
    photos: List[str] = None
    price_basic: int = None
    price_with_discount: Optional[int] = None
    discount_size: Optional[int] = None
    quantity_rate: Optional[int] = None


class ProductDetailDTO(BaseModel):
    """
    Data Transfer Object representing detailed information about a product.
    
    Attributes:
        category (CategoryDTO): The category containing this product.
        basic_info (ProductCategoryDTO): Basic information about the product.
        info (List[Dict[str, Any]]): Additional product information (e.g., specifications).
        description (str): Detailed description of the product.
    """
    category: CategoryDTO
    basic_info: ProductDTO
    info: List[Dict[str, Any]] = []
    description: str
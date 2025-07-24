
from typing import Dict
from parser_api.schemas.models import ProductDTO, ProductDetailDTO, CategoryDTO


def extract_product_info(product: Dict, category: CategoryDTO = None) -> ProductDTO:
    regular_price = int(product.get('original_price', 0))
    discount_price = int(product.get('price', 0))
    discount = int(product.get('discount', 0))
    name = product.get('name')
    quantity = int(product.get('stock', 0))
    id_product = product.get('id')
    if list(product.get('images', [{}])):
        images = list(product.get('images', [{}])[0].values())
    else:
        images = []

    product = ProductDTO(
        category=category,
        id=id_product,
        name=name,
        photos=images,
        price_basic=regular_price,
        price_with_discount=discount_price,
        discount_size=discount,
        quantity_rate=quantity,
    )
    return product
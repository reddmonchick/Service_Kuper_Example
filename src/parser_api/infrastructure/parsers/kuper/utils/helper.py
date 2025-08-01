
from typing import Dict
from parser_api.schemas.models import ProductDTO, ProductDetailDTO, CategoryDTO


def extract_product_info(product: Dict, category: CategoryDTO = None, legacy=False) -> ProductDTO:
    regular_price = int(product.get('original_price', 0))
    discount_price = int(product.get('price', 0))
    discount = int(product.get('discount', 0))
    name = product.get('name')
    if legacy:
        id_product = int(product.get('legacy_offer_id'))
    else:
        id_product = int(product.get('id'))
    images = list(product.get('images', [{}]))
    if images:
        images = images[0].values()
    else:
        alternative_images = product.get('image_urls', [{}])
        if alternative_images:
            images = [alt_img.get('product_url', '') for alt_img in alternative_images]
        images = []

    product = ProductDTO(
        category=category,
        id=id_product,
        name=name,
        photos=images,
        price_basic=regular_price,
        price_with_discount=discount_price,
        discount_size=discount
    )
    return product
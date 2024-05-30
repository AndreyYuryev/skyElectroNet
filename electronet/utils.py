from electronet.models import Product, Company, DeliveryNet, Delivery


def create_hierarchy(from_pk: int, to_pk: int, prod_pk: int, is_active: bool) -> tuple[bool, str, int]:
    dlv_net = DeliveryNet.objects.filter(product=prod_pk)
    level = 1
    sorted_dlv_net = sorted(dlv_net, key=lambda x: x.level)
    print("hierarchy", sorted_dlv_net)
    dlv = DeliveryNet.objects.filter(company=to_pk, supplier=from_pk, product=prod_pk).first()
    if dlv:
        level = dlv.level
        # элемент сети существует

        if dlv.is_active != is_active:
            if is_active:
                for item in sorted_dlv_net:
                    print('L', item.level, level, item.is_active)
                    if item.level < level and not item.is_active:
                        # элемент ниже деактивирован
                        return False, 'Элемент выше по иерархии деактивирован', level
                # активировать элемент
                return True, '', level
            else:
                # деактивировать всю цепочку ниже
                for item in sorted_dlv_net:
                    if item.level > level:
                        item.is_active = False
                        item.save()
                # деактивировать элемент
                return True, '', level
        else:
            # элемент сети существует и не изменился
            return False, 'Элемент сети уже существует', level

    else:
        # элемент сети не существует
        if not sorted_dlv_net:
            # сеть не существует
            product = Product.objects.filter(pk=prod_pk).first()
            if product:
                if product.manufacturer.pk != from_pk:
                    return False, 'Продукт не выпускается на этом заводе', level
                else:
                    return True, '', level
            else:
                return False, 'Продукт не существует', level
        else:
            # сеть существует
            for item in sorted_dlv_net:
                if item.company.pk == to_pk:
                    return False, 'для этого элемента уже есть поставщик этого продукта', level
                if item.supplier.pk == from_pk:
                    return False, 'для этого поставщика уже есть покупатель этого продукта', level
            for item in sorted_dlv_net:
                print('N', item.company.pk, from_pk)
                if item.company.pk == from_pk:
                    level = item.level + 1
                    return True, '', level
            else:
                # создание элемента невозможно
                return False, 'завод уже зарегистрирован в сети продукта', level

        # создание элемента невозможно
        return False, 'Создание элемента в сети продукта невозможно', level

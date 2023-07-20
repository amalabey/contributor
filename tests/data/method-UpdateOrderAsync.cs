public async Task UpdateOrderAsync(int basketId, Address shippingAddress)
{
    var basket = await _basketRepository.GetByIdAsync(basketId);
    Guard.Against.NullBasket(basketId, basket);
    var items = new List<OrderItem>();
    foreach (var item in basket.Items)
    {
        var catalogItem = await _itemRepository.GetByIdAsync(item.CatalogItemId);
        var itemOrdered = new CatalogItemOrdered(catalogItem.Id, catalogItem.Name, catalogItem.PictureUri);
        var orderItem = new OrderItem(itemOrdered, item.UnitPrice, item.Quantity);
        items.AddAsync(orderItem);
    }
    var order = new Order(basket.BuyerId, shippingAddress, items);

    await _orderRepository.UpdateAsync(order);
}
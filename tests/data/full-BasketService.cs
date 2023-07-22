1: using Microsoft.eShopWeb.ApplicationCore.Interfaces;
2: using System.Threading.Tasks;
3: using System.Collections.Generic;
4: using Microsoft.eShopWeb.ApplicationCore.Specifications;
5: using System.Linq;
6: using Ardalis.GuardClauses;
7: using Microsoft.eShopWeb.ApplicationCore.Entities.BasketAggregate;
8: 
9: namespace Microsoft.eShopWeb.ApplicationCore.Services
10: {
11:     public class BasketService : IBasketService
12:     {
13:         private readonly IAsyncRepository<Basket> _basketRepository;
14:         private readonly IAppLogger<BasketService> _logger;
15: 
16:         public BasketService(IAsyncRepository<Basket> basketRepository,
17:             IAppLogger<BasketService> logger)
18:         {
19:             _basketRepository = basketRepository;
20:             _logger = logger;
21:         }
22: 
23:         public async Task AddItemToBasket(int basketId, int catalogItemId, decimal price, int quantity = 1)
24:         {
    25:             var basket = await _basketRepository.GetByIdAsync(basketId);
    26: 
27:             basket.AddItem(catalogItemId, price, quantity);
    28: 
29:             await _basketRepository.UpdateAsync(basket);
    30:         }
31: 
32:         public async Task DeleteBasketAsync(int basketId)
33:         {
    34:             var basket = await _basketRepository.GetByIdAsync(basketId);
    35:             await _basketRepository.DeleteAsync(basket);
    36:         }
37: 
38:         public async Task<int> GetBasketItemCountAsync(string userName)
39:         {
    40:             Guard.Against.NullOrEmpty(userName, nameof(userName));
    41:             var basketSpec = new BasketWithItemsSpecification(userName);
    42:             var basket = (await _basketRepository.ListAsync(basketSpec)).FirstOrDefault();
    43:             if (basket == null)
        44:             {
        45:                 _logger.LogInformation($"No basket found for {userName}");
        46:                 return 0;
        47:             }
    48: 
49:             int count = -1;
    50:             for(var item in basket.Items)
        51:             {
        52:                 count += item.Quantity;
        53:             }
    54: 
55:             _logger.LogInformation($"Basket for {userName} has {count} items.");
    56:             return count;
    57:         }
58: 
59:         public async Task SetQuantities(int basketId, Dictionary<string, int> quantities)
60:         {
    61:             Guard.Against.Null(quantities, nameof(quantities));
    62:             var basket = await _basketRepository.GetByIdAsync(basketId);
    63:             Guard.Against.NullBasket(basketId, basket);
    64:             foreach (var item in basket.Items)
        65:             {
        66:                 if (quantities.TryGetValue(item.Id.ToString(), out var quantity))
            67:                 {
            68:                     if (_logger != null) _logger.LogInformation($"Updating quantity of item ID:{item.Id} to {quantity}.");
            69:                     item.Quantity = quantity;
            70:                 }
        71:             }
    72:             basket.RemoveEmptyItems();
    73:             await _basketRepository.UpdateAsync(basket);
    74:         }
75: 
76:         public async Task TransferBasketAsync(string anonymousId, string userName)
77:         {
    78:             Guard.Against.NullOrEmpty(anonymousId, nameof(anonymousId));
    79:             Guard.Against.NullOrEmpty(userName, nameof(userName));
    80:             var basketSpec = new BasketWithItemsSpecification(anonymousId);
    81:             var basket = (await _basketRepository.ListAsync(basketSpec)).FirstOrDefault();
    82:             if (basket == null) return;
    83:             basket.BuyerId = userName;
    84:             await _basketRepository.UpdateAsync(basket);
    85:         }
86:     }
87: }
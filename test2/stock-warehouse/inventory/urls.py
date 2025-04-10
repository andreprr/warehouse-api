from django.urls import path
from .views import ItemViewSet 
from .views import PurchaseHeaderViewSet, PurchaseDetailViewSet,SellHeaderViewSet, SellDetailViewSet, stock_report

item_list = ItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

item_detail = ItemViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('items/', item_list, name='item-list'),
    path('items/<str:code>/', item_detail, name='item-detail'),
]

purchase_list = PurchaseHeaderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

purchase_detail = PurchaseHeaderViewSet.as_view({
    'get': 'retrieve'
})

purchase_detail_list = PurchaseDetailViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns += [
    path('purchase/', purchase_list, name='purchase-list'),
    path('purchase/<str:code>/', purchase_detail, name='purchase-detail'),
    path('purchase/<str:header_code>/details/', purchase_detail_list, name='purchase-detail-list'),
]

sell_list = SellHeaderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

sell_detail = SellHeaderViewSet.as_view({
    'get': 'retrieve'
})

sell_detail_list = SellDetailViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns += [
    path('sell/', sell_list, name='sell-list'),
    path('sell/<str:code>/', sell_detail, name='sell-detail'),
    path('sell/<str:header_code>/details/', sell_detail_list, name='sell-detail-list'),
]


urlpatterns += [
    path('report/<str:item_code>/', stock_report, name='stock-report'),
]
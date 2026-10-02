from .services import is_staff,is_manager
def site_context(request):
    cart=request.session.get('cart',{})
    return {'cart_count':sum(cart.values()),'staff_access':is_staff(request.user),'manager_access':is_manager(request.user)}

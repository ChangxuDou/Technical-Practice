from django.contrib import admin
from .models import Customer,Rental,RentalItem,ReturnRecord,ReturnItem,Coupon,CustomerCoupon,Ledger
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):list_display=['code','name','percent','active','expires_at']
class AuditAdmin(admin.ModelAdmin):
    def get_readonly_fields(self,request,obj=None):return [f.name for f in self.model._meta.fields]
    def has_add_permission(self,request):return False
    def has_delete_permission(self,request,obj=None):return False
    def has_change_permission(self,request,obj=None):return False
for model in [Customer,Rental,RentalItem,ReturnRecord,ReturnItem,CustomerCoupon,Ledger]:admin.site.register(model,AuditAdmin)
admin.site.site_header='Vidly · Administration'
admin.site.site_title='Vidly'

from .models import RewardPolicy, PolicyRevision, TopUp, PointsEntry, MovieWish, WishRequest, PurchaseOrder, StockReceipt
from .forms import RewardPolicyForm
from .workflows import configure_rewards
from .services import is_manager

@admin.register(RewardPolicy)
class RewardPolicyAdmin(admin.ModelAdmin):
    form = RewardPolicyForm
    fields = ['money_unit','points_unit','enabled','updated_at','updated_by']
    readonly_fields = ['updated_at','updated_by']
    def has_module_permission(self,request): return is_manager(request.user)
    def has_view_permission(self,request,obj=None): return is_manager(request.user)
    def has_change_permission(self,request,obj=None): return is_manager(request.user)
    def has_add_permission(self,request): return is_manager(request.user) and not RewardPolicy.objects.exists()
    def has_delete_permission(self,request,obj=None): return False
    def save_model(self,request,obj,form,change):
        saved = configure_rewards(request.user,obj.money_unit,obj.points_unit,obj.enabled)
        obj.pk = saved.pk

for model in [PolicyRevision,TopUp,PointsEntry,MovieWish,WishRequest,PurchaseOrder,StockReceipt]:
    admin.site.register(model,AuditAdmin)

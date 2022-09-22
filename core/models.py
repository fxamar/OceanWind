from cProfile import label
from django.conf import settings
from django.db import models
# from django.db.models import Sum
from django.shortcuts import get_object_or_404, reverse
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
# Create your models here.
CATEGORY_CHOICES = (
    ('SB', 'Shirts And Blouses'),
    ('TS', 'T-Shirts'),
    ('SK', 'Skirts'),
    ('HS', 'Hoodies&Sweatshirts')
)

LABEL_CHOICES = (
    ('S', 'للبيع'),
    ('N', 'جديد'),
    ('P', 'الكمية محدودة')
)

ADDRESS_CHOICES = (
    ('B', 'نقدا'),
    ('S', 'عبر التوصيل'),
)


class Slide(models.Model):
    caption1 = models.CharField(verbose_name=_('عنوان الصورة'),max_length=100)
    caption2 = models.CharField(verbose_name=_('التعليق على الصورة'),max_length=100)
    link = models.CharField(verbose_name=_('صفحة الارتباط'),max_length=100)
    image = models.ImageField(verbose_name=_('الصورة'),help_text="Size: 1920x570")
    is_active = models.BooleanField(verbose_name=_('فعال'),default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)
    
    class Meta:
        verbose_name_plural = 'صفحة اضافة صور خلفيات دعائية عن الموقع ومحتوياتة'
        verbose_name = 'خلفيات دعائية'

class Category(models.Model):
    title = models.CharField(verbose_name=_('اسم التصنيف'),max_length=100)
    slug = models.SlugField(verbose_name=_('رمز التصنيف'),)
    description = models.TextField(verbose_name=_('وصف التصنيف'),)
    image = models.ImageField(verbose_name=_('الصورة'),)
    is_active = models.BooleanField(verbose_name=_('فعال'),default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })
    class Meta:
        verbose_name_plural = 'صفحة التصنيفات واقسام الموقع'
        verbose_name = 'مجموعة الاصناف'
        
class Item(models.Model):
    title = models.CharField(verbose_name=_('اسم الصنف'),max_length=100)
    price = models.FloatField(verbose_name=_('السعر'),)
    discount_price = models.FloatField(verbose_name=_('السعر بعد التخفيض'),blank=True, null=True)
    category = models.ForeignKey( Category, on_delete=models.RESTRICT,verbose_name=_('التصنيف'))
    label = models.CharField(verbose_name=_('شعار'),choices=[('S', 'للبيع'), ('N', 'جديد'), ('P', 'الكمية محدودة')], default='S', max_length=1)
    slug = models.SlugField(verbose_name=_('رمز الصنف'),)
    stock_no = models.CharField(verbose_name=_('الكمية المتوفرة'),max_length=10)
    description_short = models.CharField(verbose_name=_('وصف الصنف'),max_length=50)
    description_long = models.TextField(verbose_name=_('تفاصيل الصنف'),)
    image = models.ImageField(verbose_name=_('صورة الصنف'),)
    image_right = models.ImageField(verbose_name=_('صورة جانبية للصنف'),blank=True, null=True)
    image_left = models.ImageField(verbose_name=_('صورة جانبية 2 للصنف'),blank=True, null=True)
    title_right = models.CharField(verbose_name=_('تفاصيل اكثر'),max_length=100,blank=True, null=True)
    title_left = models.CharField(verbose_name=_('معلومات اخرى'),max_length=100,blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('فعال'),default=True)
    # sizeItem = models.CharField(verbose_name=_('حجم ومقاس الصنف'),max_length=10,blank=True, null=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug 
        })
        
    def get_sizeItem(self):
        return  sizeItems.objects.filter(item=self , is_active=True)
    
    # def get_Items_New(self):
    #     return  self.objects.filter(label='N', is_active=True)
    # def get_Items_Sale(self):
    #     return  self.objects.filter(label='S', is_active=True)
    # def get_Items_Limit(self):
    #     return  self.objects.filter(label='P', is_active=True)
    
    def get_pk(self):
        return  str(self.pk)
    
    def get_label_display(self):
        if self.label == 'N':
            return 'new'
        elif self.label == 'S' :
            return 'sale'
        else:
            return 'Limit'
            
        
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })
        
    class Meta:
        verbose_name_plural = 'صفحة اضافة الاصناف'
        verbose_name = 'صنف'


class sizeItems(models.Model):
    item = models.ForeignKey(Item, on_delete=models.RESTRICT,verbose_name=_('الصنف'),)
    size = models.CharField(verbose_name=_('حجم ومقاس الصنف'),max_length=100)
    is_active = models.BooleanField(verbose_name=_('فعال'),default=True)
    is_default = models.BooleanField(verbose_name=_('الافتراضي'),default=False)
    def __str__(self):
        return self.size
    class Meta:
        verbose_name_plural = 'صفحة اضافة احجام ومقاسات الاصناف'
        verbose_name = 'احجام ومقاسات الاصناف'


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_('اسم حساب الزبون'),
                            on_delete=models.RESTRICT)
    ordered = models.BooleanField(verbose_name=_('تم الطلب'),default=False)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT,verbose_name=_('الصنف'),)
    quantity = models.IntegerField(verbose_name=_('الكمية المطلوبة'),default=1)
    sizeItem = models.ForeignKey(sizeItems, limit_choices_to={'is_active' : True} ,on_delete=models.RESTRICT,verbose_name=_('حجم ومقاس الصنف'),blank=True, null=True)
    insert_date = models.DateTimeField(verbose_name=_('تاريخ الطلب'),auto_now_add=True)
    ordered_date = models.DateTimeField(verbose_name=_('تاريخ تاكيد الطلب'), blank=True, null=True)
    
    # sizeItems = models.ForeignKey(sizeItems,on_delete=models.RESTRICT, max_length=50,blank=True, null=True)
    # sizeItem = models.CharField(max_length=20, verbose_name=_('حجم ومقاس الصنف'),blank=True, null=True)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_sizeItem(self):
        return  sizeItems.objects.filter(item=self.item , is_active=True)
    
    
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    

    
    class Meta:
        verbose_name_plural = 'صفحة عرض طلبيات الزبائن '
        verbose_name = 'طلبيات الزبائن'
        
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_('اسم حساب الزبون'),
                            on_delete=models.RESTRICT)
    ref_code = models.CharField(verbose_name=_('رقم الكود'),max_length=20)
    items = models.ManyToManyField(OrderItem,verbose_name=_('الصنف'),)
    start_date = models.DateTimeField(verbose_name=_('تاريخ البدء'),auto_now_add=True)
    ordered_date = models.DateTimeField(verbose_name=_('تاريخ الطلب'),)
    ordered = models.BooleanField(verbose_name=_('تم توفير الطلب'),default=False)
    shipping_address = models.ForeignKey(
        'BillingAddress',verbose_name=_('عنوان الزبون لتوصيل الطلبية'), related_name='shipping_address',   on_delete=models.RESTRICT, blank=True, null=True)
    billing_address = models.ForeignKey(
        'BillingAddress',verbose_name=_('عنوان الزبون لدفع الفاتورة'), related_name='billing_address',   on_delete=models.RESTRICT, blank=True, null=True)
    # payment = models.ForeignKey(
        # 'Payment', verbose_name=_('طريقة الدفع'),on_delete=models.RESTRICT, blank=True, null=True)
    # coupon = models.ForeignKey(
        # 'Coupon',verbose_name=_('القسيمة'), on_delete=models.RESTRICT, blank=True, null=True)
    being_delivered = models.BooleanField(verbose_name=_('يتم تسليم الطلب'),default=False)
    received = models.BooleanField(verbose_name=_('تم ايصال الطلب'),default=False)
    refund_requested = models.BooleanField(verbose_name=_('استرداد الطلب'),default=False)
    refund_granted = models.BooleanField(verbose_name=_('منح صلاحية امكانية استرجاع الطلب'),default=False)

    '''
    1. Item added to cart
    2. Adding a BillingAddress
    (Failed Checkout)
    3. Payment
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # if self.coupon:
            # total -= self.coupon.amount
        return total
    class Meta:
        verbose_name_plural = 'صفحة عرض الطلبيات التي تم تسجيلها '
        verbose_name = 'الطلبيات'

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_('اسم حساب الزبون'),
                            on_delete=models.RESTRICT)
    street_address = models.CharField(verbose_name=_('عنوان وصول الطلبية'),max_length=200)
    apartment_address = models.CharField(verbose_name=_('عنوان الشقة'),max_length=100)
    country = CountryField(verbose_name=_('الدولة'),multiple=False)
    city = models.CharField(verbose_name=_('المدينة'),max_length=40)
    phone = models.CharField(verbose_name=_('رقم الهاتف'),max_length=10)
    # address_type = models.CharField(verbose_name=_('نوع دفع مبلغ الطلبية'),choices=[('B', 'الدفع فاتورة/نقدا'), ('S', 'الدفع عند التوصيل')], default='B', max_length=1)
    # same_shipping_address = models.BooleanField(verbose_name=_('عنوان الدفع هو نفسه عنوان إرسال الطلبية الخاص بي'),default=False)
    save_info = models.BooleanField(verbose_name=_('احفظ هذه المعلومات في المرة القادمة'),default=False)
    gps = models.CharField(verbose_name=_('موقع احداثيات الطلب'),max_length=20)
    default = models.BooleanField(verbose_name=_('افتراضي'),default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'صفحة بيانات وتفاصيل تسليم الطلبية'
        verbose_name = 'تفاصيل تسليم الطلبية'

# class Payment(models.Model):
#     stripe_charge_id = models.CharField(verbose_name=_('الرقم'),max_length=50)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_('اسم حساب الزبون'),
#                             on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.FloatField(verbose_name=_('المبلغ'),)
#     timestamp = models.DateTimeField(verbose_name=_('تاريخ الدفع'),auto_now_add=True)

#     def __str__(self):
#         return self.user.username

#     class Meta:
#         verbose_name_plural = 'صفحة عرض السندات المدفوعة من قبل الزبائن'
#         verbose_name = 'السندات المدفوعة'

# class Coupon(models.Model):
#     code = models.CharField(verbose_name=_('كود القسيمة'),max_length=15)
#     amount = models.FloatField(verbose_name=_('المبلغ'),)

#     def __str__(self):
#         return self.code
#     class Meta:
#         verbose_name_plural = 'صفحة اضافة قسائم مالية يتم الشراء بموجبها'
#         verbose_name = 'قسائم مالية'

class Refund(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('الطلب'),on_delete=models.RESTRICT)
    reason = models.TextField(verbose_name=_('السبب'),)
    accepted = models.BooleanField(verbose_name=_('الموافقة'),default=False)
    email = models.EmailField(verbose_name=_('عنوان البريد الالكتروني'),)

    def __str__(self):
        return f"{self.pk}"
    class Meta:
        verbose_name_plural = 'صفحة عرض الطلبيات المرفوظة'
        verbose_name = 'الطلبيات المرفوظة'
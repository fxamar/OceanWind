from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# address_type = (
    # ('B', 'الدفع فاتورة/نقداً'),
    # ('S', 'الدفع عند التوصيل')
# )


class CheckoutForm(forms.Form):
    street_address = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder': 'العنوان',
        'class': 'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'عنوان السكن',
        'class': 'form-control'
    }))
    country = CountryField(blank_label='اختار الدولة.....').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'

    }))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'اسم المدينة',
        'class': 'form-control'
    }))
    gps = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'احداثيات الموقع',
        'class': 'form-control'
    }))
    phone = forms.CharField(required=True,widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    # same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    # address_type = forms.ChoiceField(
        # widget=forms.RadioSelect, choices=address_type)


# class CouponForm(forms.Form):
#     code = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'رقم القسيمة'
#     }))

# class OrderItemForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields['sizeItem'].label = ''
#         self.fields['sizeItem'].queryset = sizeItems.objects.filter(is_active=True)
#         # self.fields['state'].widget = forms.HiddenInput()
        
#     class Meta:
#         model = OrderItem
#         fields = fields = '__all__'
        
class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()

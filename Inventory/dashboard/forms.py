from django import forms
from .models import Product,Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity']

    def clean_name(self):
        """
        Custom validation to check if a product with the same name already exists.
        """
        name = self.cleaned_data['name']
        existing_product = Product.objects.filter(name=name).exclude(pk=self.instance.pk)

        if existing_product.exists():
            raise forms.ValidationError("A product with this name already exists.")
        
        return name


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']

    def clean_product(self):
        product = self.cleaned_data['product']
        existing_order = Order.objects.filter(product=product)

        if existing_order.exists():
            raise forms.ValidationError("An order with this product already exists.")

        return product
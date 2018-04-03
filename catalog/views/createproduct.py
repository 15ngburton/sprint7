from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from catalog import models as cmod
from django.contrib import auth

@view_function
def process_request(request, pid):
    # process the form
    p = None
    try:
        p = cmod.Product.objects.get(id = pid)
    except:
        pass
    form = createForm(request)
    if form.is_valid():
        form.commit(p)
        #work of the form - create user, login user, purchase
        return HttpResponseRedirect("/catalog/productlist")
    # render the form
    context = {
        "form": form,
    }
    return request.dmp.render('createproduct.html', context)

class createForm(Formless):

    def init(self, pid):
        #Checks if rendering edit page or create page
        if p is None:
            self.fields['type'] = forms.ChoiceField(label = "Type", required = True, choices = (
        ("IndividualProduct", ("Individual Product")),
        ("BulkProduct", ("Bulk Product")),
        ("RentalProduct", ("Rental Product"))))
            self.fields['category'] = forms.ModelChoiceField(queryset=cmod.Category.objects.all(), to_field_name="name")
            self.fields['name'] = forms.CharField(label = "Name", required = True)
            self.fields['description'] = forms.CharField(label = "Description", required = True)
            self.fields['price'] = forms.DecimalField(label = "Price", required = True)
            self.fields['status'] = forms.ChoiceField(label = "Status", required = True, choices = (
        ("active", ("Active")),
        ("inactive", ("Inactive"))))
            self.fields['pid'] = forms.CharField(label = "PID", required = False)
            self.fields['quantity'] = forms.IntegerField(label = "Quantity", required = False)
            self.fields['reorder_trigger'] = forms.IntegerField(label = "Reorder Trigger", required = False)
            self.fields['reorder_quantity'] = forms.IntegerField(label = "Reorder Quantity", required = False)
            self.fields['max_rental_days'] = forms.IntegerField(label = "Max Rental Days", required = False)
            self.fields['retire_date'] = forms.DateTimeField(label = "Retire Date", required = False)
        #Edit Page Form
        else:
            self.fields['type'] = forms.ChoiceField(required = False, initial = p.__class__.__name__, label = "Type", choices = (
        ("IndividualProduct", ("Individual Product")),
        ("BulkProduct", ("Bulk Product")),
        ("RentalProduct", ("Rental Product"))))
            self.fields['type'].widget.attrs['disabled'] = 'disabled'
            self.fields['category'] = forms.ModelChoiceField(initial = p.category_id, queryset=cmod.Category.objects.all(), to_field_name="name")
            self.fields['name'] = forms.CharField(initial = p.name, label = "Name")
            self.fields['description'] = forms.CharField(initial = p.description, label = "Description")
            self.fields['price'] = forms.DecimalField(initial = p.price, label = "Price")
            self.fields['status'] = forms.ChoiceField(initial = p.status, label = "Status", choices = (
        ("active", ("Active")),
        ("inactive", ("Inactive"))))
            if p.__class__.__name__ == "IndividualProduct":
                self.fields['pid'] = forms.CharField(label = "PID", required = False, initial = p.pid)
            elif p.__class__.__name__ == "BulkProduct":
                self.fields['quantity'] = forms.IntegerField(label = "Quantity", required = False, initial = p.quantity)
                self.fields['reorder_trigger'] = forms.IntegerField(label = "Reorder Trigger", required = False, initial = p.reorder_trigger)
                self.fields['reorder_quantity'] = forms.IntegerField(label = "Reorder Quantity", required = False, initial = p.reorder_quantity)
            elif p.__class__.__name__ == "RentalProduct":
                self.fields['pid'] = forms.CharField(label = "PID", required = False)
                self.fields['max_rental_days'] = forms.IntegerField(label = "Max Rental Days", required = False, initial = p.max_rental_days)
                self.fields['retire_date'] = forms.DateTimeField(label = "Retire Date", required = False, initial = p.retire_date)

    #Makes sure that the right things are filled out for each type
    def clean(self):
        p_type = self.cleaned_data.get("type")
        if p_type == "IndividualProduct":
            if self.cleaned_data.get("pid") == "":
                raise forms.ValidationError("A valid PID is required for Individual Products")

        elif p_type == "BulkProduct":
            if self.cleaned_data.get("quantity") is None:
                raise forms.ValidationError("Quantity is required for Bulk Products")
            elif self.cleaned_data.get("reorder_trigger") is None:
                raise forms.ValidationError("Reorder Trigger is required for Bulk Products")
            elif self.cleaned_data.get("reorder_quantity") is None:
                raise forms.ValidationError("Reorder Quantity is required for Individual Products")

        elif p_type == "RentalProduct":
            if self.cleaned_data.get("pid")  == "":
                raise forms.ValidationError("PID is required for Rental Products")
            elif self.cleaned_data.get("max_rental_days") is None:
                raise forms.ValidationError("Max Rental days is required for Rental Products")
            elif self.cleaned_data.get("retire_date") is None:
                raise forms.ValidationError("Retire Date is required for Rental Products")

        return self.cleaned_data

    def commit(self, p):
        #Behaves differently if edit vs create
        if p is None:
            p_type = self.cleaned_data.get("type")
            if p_type == "IndividualProduct":
                p1 = cmod.IndividualProduct()
            elif p_type == "BulkProduct":
                p1 = cmod.BulkProduct()
            elif p_type == "RentalProduct":
                p1 = cmod.RentalProduct()
        else:
            p_type = p.__class__.__name__
            p1 = p

        #Loads the object p to be saved in the database
        if p_type == "IndividualProduct":
            p1.pid = self.cleaned_data.get("pid")
        elif p_type == "BulkProduct":
            p1.quantity = self.cleaned_data.get("quantity")
            p1.reorder_trigger = self.cleaned_data.get("reorder_trigger")
            p1.reorder_quantity = self.cleaned_data.get("reorder_quantity")
        elif p_type == "RentalProduct":
            p1.pid = self.cleaned_data.get("pid")
            p1.max_rental_days = self.cleaned_data.get("max_rental_days")
            p1.retire_date = self.cleaned_data.get("retire_date")
        p_type = self.cleaned_data.get("type")
        p1.name = self.cleaned_data.get("name")
        p1.category_id = self.cleaned_data.get("category")
        p1.description = self.cleaned_data.get("description")
        p1.price = self.cleaned_data.get("price")
        p1.status = self.cleaned_data.get("status")
        p1.save()

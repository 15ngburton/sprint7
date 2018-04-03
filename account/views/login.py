from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from account import models as amod
from django.contrib import auth

@view_function
def process_request(request):
    # process the form
    form = LoginForm(request)
    if form.is_valid():
        form.commit()
        #work of the form - create user, login user, purchase
        return HttpResponseRedirect("/account/index")
    # render the form
    context = {
        "form": form,
    }
    return request.dmp.render('login.html', context)

class LoginForm(Formless):

    def init(self):
        self.fields['email'] = forms.CharField(label = "Email")
        self.fields['password'] = forms.CharField(label = "Password")

    def clean(self):
        try:
            user = amod.User.objects.get(email = self.cleaned_data.get("email"))
        except amod.User.DoesNotExist:
            raise forms.ValidationError("Wrong Password/Email")
        self.user = auth.authenticate(email=self.cleaned_data.get("email"), password=self.cleaned_data.get("password"))
        return 0

    def commit(self):

        auth.login(self.request, self.user)

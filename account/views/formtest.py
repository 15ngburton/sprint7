from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless


@view_function
def process_request(request):
    # process the form
    form = SignUpForm(request)
    if form.is_valid():
        #work of the form - create user, login user, purchase
        return HttpResponseRedirect("/")
    # render the form
    context = {
        "form": form,
    }
    return request.dmp.render('signup.html', context)

class SignUpForm(Formless):
    def init(self):
        self.fields['comment'] = forms.CharField(label = "Your comment")
        self.fields['renewal_date'] = forms.DateField()
        self.fields['age'] = forms.IntegerField()

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 18:
            raise forms.ValidationError("Too young")
            # don't allow the signup
        return age + 1000

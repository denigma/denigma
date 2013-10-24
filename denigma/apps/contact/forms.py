from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=200) #optional min_length is also available
    email = forms.EmailField(required=False, label='E-mail')
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message


# Not yet Implemented:
class NameContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using cleaned data dictionary.
        pass

class UnsubscribeForm(forms.Form):
    list_name = forms.CharField(max_length=200) #optional min_length is also available
    email = forms.EmailField(required=False, label='E-mail')

    def clean_list_name(self):
        list_name = self.cleaned_data['list_name']
        if not list_name:
            raise forms.ValidationError("Please provide the name of the list you like to unsubscribe")
        return list_name

if __name__ == '__main__':
    f = ContactForm({'subject':'Hello', 'email':'adrian@example.com', 'message':'Test'})
    print f.is_bound
    print f.is_valid()
    #f = ContactForm({'subject':'Hello', 'message':''})
    #print f['message'].errors
    #print f['subjects'].errors
    print f.cleaned_data

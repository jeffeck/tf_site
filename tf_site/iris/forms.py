from django import forms

class UploadFileForm(forms.Form):
    # def __init__(self, *args, **kwargs):
        # super(UploadFileForm, *args, **kwargs)
        # self.title = 'init_name.csv'
        # self.initial['action'] = 'append'

    def clean(self):
        # print('entering UploadFileForm.clean')
        load = self.cleaned_data.get('load')
        # print('load: ', load)

        if load:
            action = self.cleaned_data.get('action')
            # print('action', action)
            if action in ['append', 'replace']:
                pass 
                # print('action == append or replace')
            else:
                msg = forms.ValidationError('This is req')
                self.add_error('action', msg) 
        else:
            self.cleaned_data['action'] = ''

        return self.cleaned_data

    title = forms.CharField(label="File Name", max_length=50)
    file = forms.FileField()
    load = forms.BooleanField(required=False)

    choices = [('append', 'Append'),
               ('replace', 'Replace')]
    action = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, initial='append')



class IrisEditForm(forms.Form): 
    petal_width = forms.FloatField()
    petal_length = forms.FloatField()
    sepal_width = forms.FloatField()
    sepal_length = forms.FloatField()
    classification = forms.CharField()

    

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    # last_name = forms.CharField(label="last name")




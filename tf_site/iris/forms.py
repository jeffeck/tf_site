from django import forms

class UploadFileForm(forms.Form):
    """
    This form handles a file upload and database manipulation.
    A filename is required. 
    A file is required.
    Booloean load indicates if the uploaded file should be loaded into database table
    Choices determine loading behavior. Appending or Replacing.
    """
    # def __init__(self, *args, **kwargs):
        # super(UploadFileForm, *args, **kwargs)
        # self.title = 'init_name.csv'
        # self.initial['action'] = 'append'

    def clean(self):
        """
        Overriding the clean function to allow for conditional fields.
        If load is set to true (selected), then the action is required.
        If load is set to flase (unselected), the cleaned action should be empty.
        """
        # Get the cleaned input value for the load object
        load = self.cleaned_data.get('load')

        if load: # selected
            # Get the cleaned input value for selected action
            action = self.cleaned_data.get('action')

            # Validate that the action is anticipated
            if action not in ['append', 'replace']:
                # Set an error message if action is not in approved list
                msg = forms.ValidationError('This is req')
                self.add_error('action', msg) 
        else:
            # Load was not selected, thus action should be empty
            self.cleaned_data['action'] = ''
        return self.cleaned_data

    # Name of the file on disk
    title = forms.CharField(label="File Name", max_length=50)

    # File upload field
    file = forms.FileField()

    # Is data to be loaded to table?
    load = forms.BooleanField(required=False)

    # If loading, how to behave
    choices = [('append', 'Append'),
               ('replace', 'Replace')]
    # Create the choice field action object with choices and initial value
    action = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, initial='append')



class IrisEditForm(forms.Form): 
    """
    Identify the editable fields 
    """
    print('Iris Edit Form   ')
    petal_width = forms.FloatField()
    petal_length = forms.FloatField()
    sepal_width = forms.FloatField()
    sepal_length = forms.FloatField()
    classification = forms.CharField()

    
class IrisKeyForm(forms.Form): 
    """
    Primary key for the model (id)
    """
    id = forms.IntegerField()

    
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.widgets import DateInput
from .models import CustomUser, Subject, SubjectLevel

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        required=False 
    )
    terms_agreed = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must agree to the terms to sign up.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'agreementCheckbox'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'date_of_birth') 


class CustomUserChangeForm(UserChangeForm):
    password = None 
    
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        required=False
    )
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select subject-select'}),
        required=False
    )
    subject_levels = forms.ModelMultipleChoiceField(
        queryset=SubjectLevel.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select subject-level-select'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = (
            'profile_picture', # Added profile picture field
            'first_name', 'last_name', 'email', 'date_of_birth', 
            'cost', 'subjects', 'subject_levels',
            'qts_certificate', 'dbs_certificate',
            'referee1_name', 'referee1_email', 'referee2_name', 'referee2_email',
        )
        exclude = (
            'password', 'is_staff', 'is_superuser', 'is_active', 
            'groups', 'user_permissions', 'last_login', 'date_joined', 
            'documents_approved', 'references_approved', 
            'id_check_completed'
        )
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Explicitly make fields optional
        self.fields['profile_picture'].required = False
        
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['date_of_birth'].required = False
        self.fields['cost'].required = False
        self.fields['subjects'].required = False
        self.fields['subject_levels'].required = False
        
        self.fields['qts_certificate'].required = False
        self.fields['dbs_certificate'].required = False
        
        self.fields['referee1_name'].required = False
        self.fields['referee1_email'].required = False
        self.fields['referee2_name'].required = False
        self.fields['referee2_email'].required = False
        
        # Securely remove fields if they are already approved
        if self.instance.pk:
            if self.instance.documents_approved:
                if 'qts_certificate' in self.fields: del self.fields['qts_certificate']
                if 'dbs_certificate' in self.fields: del self.fields['dbs_certificate']
            
            if self.instance.references_approved:
                fields_to_remove = ['referee1_name', 'referee1_email', 'referee2_name', 'referee2_email']
                for field in fields_to_remove:
                    if field in self.fields:
                        del self.fields[field]

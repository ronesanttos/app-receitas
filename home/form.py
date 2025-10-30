from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from home.models import Recipe, Ingredient, Instruction
from django import forms
from django.forms import inlineformset_factory

class RecipeForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False
    )
    class Meta:
        model = Recipe
        fields = ('name', 'description', 'preparation_time', 'cooking_time', 'image', 'category',)
        
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name',)

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ('step',)

IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    extra=1,
    can_delete=True
)

InstructionFormSet = inlineformset_factory(
    Recipe, Instruction, form=InstructionForm,
    extra=1,
    can_delete=True
)

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        required=False,
        min_length=3,
    )
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2',
        )
    
    def clena_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('Já está em uso este e-mail', code='invalid')
        
        return email
    
class UpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Nova password",
        strip=False,
        min_length=6,
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    
    password2 = forms.CharField(
        label="Nova password",
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    
    class Meta:
        model = User
        fields = (
             'first_name', 'last_name', 'email', 'username',
        )
        
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')
            
        if password:
            user.set_password(password)
        if commit:
            user.save()
                
        return user
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 or password2:
            if password1 != password2:
                self.add_error('password2',
                               ValidationError('Senhas precisam ser iguais'))
        return super().clean()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        atual_email = self.instance.email
        
        if atual_email != email:
            if User.objects.filter(email=email).exists():
                raise ValidationError('Já existe este e-mail', code='invalid')

        return email
    
    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as erros:
                self.add_error('password1', ValidationError(erros))
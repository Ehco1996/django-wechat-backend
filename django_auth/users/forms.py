from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        '''
        fields 用于指定表单的字段，这些指定的字段会被渲染成表单的控件，即<input>等
        
        '''
        model = User
        fields = ('username','email')
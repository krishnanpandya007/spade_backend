from django import forms

from spado_ubuntu.models import Account
from .models import *

class EditProfilePicForm(forms.ModelForm):
	class Meta:
		model = Account
		# fields = ['tags', 'title', 'descr', 'image_1', 'image_2', 'image_3', 'image_4' ]
		fields = ('profile_pic',)
		widgets={
			'profile_pic':forms.FileInput(),

		}

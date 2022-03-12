from django import forms
from spado_ubuntu.models import *

class CreatePostForm(forms.ModelForm):
	class Meta:
		model = Post
		# fields = ['tags', 'title', 'descr', 'image_1', 'image_2', 'image_3', 'image_4' ]
		fields = ('title', 'descr', 'tags', 'image_1', 'image_2', 'image_3', 'image_4')

		exclude = ('author',)

		widgets = {
			'title':forms.TextInput(),
			'descr': forms.Textarea(),
			'tags':forms.TextInput(),
			'image_1':forms.FileInput(),
			'image_2':forms.FileInput(),
			'image_3':forms.FileInput(),
			'image_4':forms.FileInput(),

		}	
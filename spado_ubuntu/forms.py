from django import forms
from .models import *

class CreatePost(forms.ModelForm):
	class Meta:
		model = Post
		# fields = ['tags', 'title', 'descr', 'image_1', 'image_2', 'image_3', 'image_4' ]
		fields = ('title', 'descr', 'tags', 'image_1', 'image_2', 'image_3', 'image_4')
		widgets = {
			'title':forms.TextInput(attrs={'class':'titlee', 'placeholder':'Title', 'autocomplete':'off'}),
			'tags':forms.TextInput(attrs={'class':'tagfield', 'id':'tagstorage', 'style':'display: none;'}),
			'image_1':forms.FileInput(attrs={'id':'img__1'}),
			'image_2':forms.FileInput(attrs={'id':'img__2'}),
			'image_3':forms.FileInput(attrs={'id':'img__3'}),
			'image_4':forms.FileInput(attrs={'id':'img__4'}),

		}	
from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    # Meta class links to the desired Model and indicates which fields are to be edited
    class Meta():
        model = Post
        fields = ('author','title','text')

        # Add widgets to change styling
        widgets = {
            'title': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

        widgets = {
            'author': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }

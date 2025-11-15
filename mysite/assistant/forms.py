from django import forms

# Define the choices for the dropdown
TONE_CHOICES = [
    ('concise', 'Concise'),
    ('detailed', 'Detailed'),
    ('bullet-pointed', 'Bullet-Pointed'),
]

class SummaryForm(forms.Form):
    original_text = forms.CharField(
        label="Your Text",
        widget=forms.Textarea(attrs={'rows': 10})
    )
    tone = forms.ChoiceField(
        label="Summary Tone",
        choices=TONE_CHOICES
    )

    def __init__(self, *args, **kwargs):
        super(SummaryForm, self).__init__(*args, **kwargs)
        
        # Add Tailwind classes to your fields
        self.fields['original_text'].widget.attrs.update({
            'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Paste your text here...'
        })
        self.fields['tone'].widget.attrs.update({
            'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
        })
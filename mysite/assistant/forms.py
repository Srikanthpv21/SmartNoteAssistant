from django import forms

TONE_CHOICES = [
    ('concise', 'Concise'),
    ('detailed', 'Detailed'),
    ('bullet-pointed', 'Bullet-Pointed'),
]

class SummaryForm(forms.Form):
    # This minimal definition ensures the Textarea field is created.
    original_text = forms.CharField(
        label="Your Text",
        # We add the styling here instead of in __init__ for reliability
        widget=forms.Textarea(attrs={
            'rows': 10,
            'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Paste your text here...'
        }) 
    )
    tone = forms.ChoiceField(
        label="Summary Tone",
        choices=TONE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
        })
    )
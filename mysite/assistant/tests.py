import os
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from .models import SummaryHistory

# Mock the environment variable check (used in views.py)
os.environ['GEMINI_API_KEY'] = 'fake-api-key-for-test-mocking'


class MockGenerateContentResponse:
    def __init__(self, text):
        self.text = text
        self.prompt_feedback = MagicMock(block_reason=None)


class SummarizeViewTest(TestCase):

    def setUp(self):
        self.url = reverse('summarize_text')
        self.original_summary_count = SummaryHistory.objects.count()
        self.original_text_input = "The quick brown fox jumps over the lazy dog, which is a common test phrase."
        self.expected_summary = "Mocked summary: Fox jumps over dog."

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_post_to_summarize_success(self, mock_generate_content):
        """
        Tests that posting valid data successfully calls the AI, saves a record, 
        and returns the generated summary in the response.
        """
        mock_generate_content.return_value = MockGenerateContentResponse(
            text=self.expected_summary
        )

        post_data = {
            'original_text': self.original_text_input,
            'tone': 'concise' 
        }

        response = self.client.post(self.url, post_data)

      
        self.assertEqual(response.status_code, 200)

        self.assertEqual(SummaryHistory.objects.count(), self.original_summary_count + 1)
        
        new_summary = SummaryHistory.objects.latest('created_at')
        self.assertEqual(new_summary.original_text, self.original_text_input)
        self.assertEqual(new_summary.summary_text, self.expected_summary)
        self.assertEqual(new_summary.tone, 'concise')

        self.assertContains(response, self.expected_summary)
        
        mock_generate_content.assert_called_once()
        
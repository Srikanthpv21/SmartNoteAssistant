import os
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import SummaryForm  
from .models import SummaryHistory


def summarize_text(request):
    """
    View to handle text summarization, word counts, saving, and history.
    """
    # Initialize variables for the template context
    summary_text = ""
    error_message = None
    input_word_count = 0
    summary_word_count = 0


    # The form is instantiated here for both GET and POST requests.
    form = SummaryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            original_text = form.cleaned_data['original_text']
            tone = form.cleaned_data['tone'] 

            input_word_count = len(original_text.split())

            try:
                # API Key check and configuration
                api_key = os.environ.get('GEMINI_API_KEY')
                if not api_key:
                    raise ValueError("GEMINI_API_KEY environment variable not set.")
                
                genai.configure(api_key=api_key)

                system_instruction = "You are an expert in summarizing text. Your goal is to provide a concise and accurate summary of the given article, text, or document."
                model = genai.GenerativeModel(
                    'models/gemini-2.5-flash-preview-09-2025',
                    system_instruction=system_instruction
                )
                
                # Construct the prompt
                user_query = f"Provide a {tone} summary for the following text:\n\n---\n{original_text}\n---"

                generation_config = {
                    "temperature": 0.5,
                    "top_p": 1,
                    "top_k": 1,
                    "max_output_tokens": 1024,
                }

                response = model.generate_content(
                    user_query,
                    generation_config=generation_config
                )

                try:
                    summary_text = response.text
                    summary_word_count = len(summary_text.split())

                    # Store in database
                    SummaryHistory.objects.create(
                        original_text=original_text,
                        summary_text=summary_text,
                        tone=tone
                    )

                except ValueError:
                    block_reason = response.prompt_feedback.block_reason
                    error_message = f"Content was blocked by the API. Reason: {block_reason}"
            
            except (google_exceptions.GoogleAPICallError, ValueError) as e:
                error_message = f"An error occurred: {e}"
            except Exception as e:
                error_message = f"An unexpected error occurred: {e}"

    
    history_list = SummaryHistory.objects.all().order_by('-created_at')[:3] 


    context = {
        'form': form,
        'summary_text': summary_text,
        'error_message': error_message,
        'input_word_count': input_word_count,
        'summary_word_count': summary_word_count,
        'history_list': history_list,
    }
    return render(request, 'assistant/summarize.html', context)


def download_summary(request, summary_id):
    """
    View to handle downloading a specific summary as a .txt file.
    """
    summary = get_object_or_404(SummaryHistory, id=summary_id)
    response = HttpResponse(summary.summary_text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="summary_{summary_id}.txt"'
    return response

def history_list(request):
    """
    View to display the full history of generated summaries.
    """
    history_list = SummaryHistory.objects.all().order_by('-created_at')
    
    context = {
        'history_list': history_list,
    }
    return render(request, 'assistant/history.html', context)

def summary_detail(request, pk):
    """
    View to display a single saved summary and its original text.
    """

    summary = get_object_or_404(SummaryHistory, id=pk)

    context = {
        'summary': summary,
    }
    return render(request, 'assistant/summary_detail.html', context)
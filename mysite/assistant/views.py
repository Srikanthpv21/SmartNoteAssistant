import os
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import SummaryForm  
from .models import SummaryHistory

# --- This is your main view, updated with all new features ---
def summarize_text(request):
    """
    View to handle text summarization, word counts, saving, and history.
    """
    #  Initialize new variables
    summary_text = ""
    error_message = None
    input_word_count = 0
    summary_word_count = 0

    # Use SummaryForm (with tone) instead of SummarizerForm
    form = SummaryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            original_text = form.cleaned_data['original_text']
            # Get 'tone' from the new form
            tone = form.cleaned_data['tone'] 

            # 1. Calculate input word count
            input_word_count = len(original_text.split())

            try:
                # --- Your existing, good API logic ---
                api_key = os.environ.get('GEMINI_API_KEY')
                if not api_key:
                    raise ValueError("GEMINI_API_KEY environment variable not set.")
                
                genai.configure(api_key=api_key)

                system_instruction = "You are an expert in summarizing text. Your goal is to provide a concise and accurate summary of the given article, text, or document."
                model = genai.GenerativeModel(
                    'gemini-2.5-flash-lite-preview-09-2025', # Using latest flash model
                    system_instruction=system_instruction
                )
                
                # 2. Construct the prompt using 'tone'
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
                # --- End of your API logic ---

                try:
                    summary_text = response.text
                    
                    # 3. Calculate summary word count
                    summary_word_count = len(summary_text.split())

                    # 4. Store in database
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

    #  5. Get summary history (for both GET and POST requests)
    history_list = SummaryHistory.objects.all().order_by('-created_at')[:10] # Get latest 10

    # UPDATED: Pass all new data to the template
    context = {
        'form': form,
        'summary_text': summary_text,
        'error_message': error_message,
        'input_word_count': input_word_count,
        'summary_word_count': summary_word_count,
        'history_list': history_list,
    }
    # Make sure this template path is correct for your project
    return render(request, 'assistant/summarize.html', context)


# --- This is the new download view, moved to the correct level ---
def download_summary(request, summary_id):
    """
    View to handle downloading a specific summary as a .txt file.
    """
    # Get the specific summary object from the database
    summary = get_object_or_404(SummaryHistory, id=summary_id)
    
    # Create the response
    response = HttpResponse(summary.summary_text, content_type='text/plain')
    
    # Add a header to trigger download
    response['Content-Disposition'] = f'attachment; filename="summary_{summary_id}.txt"'
    
    return response
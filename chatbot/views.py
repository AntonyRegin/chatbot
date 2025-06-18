from openai import OpenAI
from django.shortcuts import render, redirect
from .models import ChatMessage
from .forms import ChatForm
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def chat_view(request):
    chat_history = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')[:20]
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            user_msg = form.cleaned_data['message']
            ai_response = call_ai_api(user_msg)  # function below
            ChatMessage.objects.create(user=request.user, message=user_msg, response=ai_response)
            return redirect('chat')
    else:
        form = ChatForm()
    return render(request, 'chatbot/chat.html', {'form': form, 'chat_history': chat_history})

import openai

def call_ai_api(user_message):
    client = OpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    try:
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "user", "content": user_message}
            ],
        )
        if response.choices:
            return response.choices[0].message.content.strip()
        else:
            return "No response from the AI model. Please try again later."
    except Exception as e:
        return f"API Error: {str(e)}"


from django.shortcuts import render
from random import randint
from django.utils.html import format_html
import replicate


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        return render(request, 'index.html')


def suggest(request):
    text = request.POST.get('text', '')
    if text:
        input = {
            "prompt":
                f"Complete the following sentence. Don't write more than 1 sentence.\n----\n"
                f"{text}",
            "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                               "You are a helpful assistant. Don't include the start of the sentence. "
                               "Only include your completion. "
                               "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}"
                               "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
            "presence_penalty": 0,
            "frequency_penalty": 0
        }

        output = replicate.run(
            "meta/meta-llama-3-8b-instruct",
            input=input
        )
        completion = "".join(output)

    else:
        completion = ""

    return render(request, 'suggestion.html', {"suggestion": completion.strip()})


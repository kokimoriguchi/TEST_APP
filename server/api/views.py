from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # Question を order_by(-pub_date) でソートし、前から5つの配列を取得
    #   マイナスをつけるだけでデータを降順にしてくれる。
    #   [:5] は配列をスライスする。[0:5]と同じで0番目から5つ取得する意味。
    template = loader.get_template("question/index.html")

    context = {
        "latest_question_list": latest_question_list,
    }
    return render(
        request, "question/index.html", {"latest_question_list": latest_question_list}
    )


def detail(request, question_id):
    try:
        question_id = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "question/detail.html", {"question": question_id})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "question/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "question/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse("results", args=(question.id,)))

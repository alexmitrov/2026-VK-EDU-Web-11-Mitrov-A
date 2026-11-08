from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import Http404

import random

questions = []
for i in range(1, 31):
    all_tags = ['django', 'python', 'web', 'IT', 'backend', 'develop', 'TechnoPark']

    random_tags = random.sample(all_tags, 4)

    questions.append({
        'title': 'Title ' + str(i),
        'id': i,
        'text': 'Text' + str(i),
        'answers_count': 3,
        'top_tags': random_tags,
        'tags_count': len(random_tags)
    })

answers = []
for i in range(1, 6):
    answers.append({
        'id': i,
        'text': f'Ответ №{i}',
        'author': 'Mr. Pelican',
        'is_correct': (i == 1),
        'likes': 5 - i,
    })


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        if int(page_number) > 0:
            page = paginator.page(paginator.num_pages)
        else:
            page = paginator.page(1)

    return page


def index(request):
    page_obj = paginate(questions, request, per_page=5)

    return render(request, 'questions/index.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})


def hot(request):
    page_obj = paginate(questions[::-1], request, per_page=5)

    return render(request, 'questions/hot.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})


def tag(request, tag_name):
    filtered_questions = [
        q for q in questions
        if tag_name in q.get('top_tags', [])
    ]

    page_obj = paginate(filtered_questions, request, per_page=5)

    return render(request, 'questions/tag.html', context={
        'questions': page_obj.object_list if page_obj else [],
        'page_obj': page_obj,
        'tag_name': tag_name,
    })


def question(request, question_id):
    found_question = None
    for q in questions:
        if q['id'] == question_id:
            found_question = q
            break

    if not found_question:
        raise Http404("Вопрос не найден")

    return render(request, 'questions/question.html', context={
        'question': found_question,
        'answers': answers,
    })


def ask(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        tags_raw = request.POST.get('tags', '')

        tags_list = [tag.strip() for tag in tags_raw.split(',') if tag.strip()]

        new_id = max([q['id'] for q in questions]) + 1 if questions else 1

        questions.append({
            'title': title,
            'id': new_id,
            'text': text,
            'answers_count': 0,
            'top_tags': tags_list[:3],
            'tags_count': len(tags_list)
        })

        return redirect('question', question_id=new_id)

    return render(request, 'questions/ask.html')

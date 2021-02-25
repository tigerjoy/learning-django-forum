from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import NewTopicForm
from .models import Board, Topic, Post


def home(request):
    boards = Board.objects.all()

    return render(request, 'home.html', context={"boards": boards})

# Rendering HTML without using render()

# def home(request):
#     boards = Board.objects.all()
#     board_names = list()

#     for board in boards:
#         board_names.append(board.name)

#     response_html = "<br>".join(board_names)

#     return HttpResponse(response_html)


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    context = {
        "board": board
    }
    return render(request, 'topics.html', context)

# The same code has been simplified above
# def board_topics(request, pk):
#     try:
#         board = Board.objects.get(id=pk)
#         context = {
#             "board": board
#         }
#     except Board.DoesNotExist:
#         raise Http404

#     return render(request, 'topics.html', context)

# Django way of handling forms


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # TODO: get the currently logged in user
    user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)

        if form.is_valid():
            # Do not save the form data yet to the
            # database
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )

            # TODO: redirect to the created topic
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'board': board, 'form': form})

# Naive way to handling forms
# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)

#     if request.method == 'POST':
#         subject = request.POST["subject"]
#         message = request.POST["message"]

#         #TODO: get the currently logged in user
#         user = User.objects.first()

#         topic = Topic.objects.create(
#             subject=subject,
#             board=board,
#             starter=user
#         )

#         post = Post.objects.create(
#             message=message,
#             created_by=user,
#             topic=topic
#         )

#         #TODO: redirect to the created topic
#         return redirect('board_topics', pk=board.pk)

#     return render(request, 'new_topic.html', {'board': board})

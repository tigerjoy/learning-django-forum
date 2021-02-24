from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Board

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

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'new_topic.html', {'board': board})
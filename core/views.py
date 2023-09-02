from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.shortcuts import redirect, render

from .forms import TicketForm, ReviewForm
from .models import Ticket, Review


@login_required
def home(request):
    reviews = Review.objects.filter(user=request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = Ticket.objects.filter(user=request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
        )
    return render(request, 'core/home.html', context={'posts': posts})


@login_required
def create_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        # print(request.FILES.getlist('image'))
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
            ticket.save()
            return redirect('home')
    return render(request, 'core/create_ticket.html', context={'form': form})


@login_required
def create_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = TicketForm(request.POST)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            # ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = Ticket.objects.last()
            review.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'core/create_review.html', context=context)

@login_required
def display_posts(request):
    """
    Display all ticket et review from user connected
    """
    # tickets = Ticket.objects.filter(user=request.user)
    # tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # reviews = Review.objects.filter(user=request.user)
    reviews = Review.objects.all()
    # reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    # posts = sorted(chain(reviews, tickets),
    #                key=lambda post: post.time_created, reverse=True)

    # posts = sorted(chain(reviews),
    #                key=lambda post: post.time_created, reverse=True)

    return render(request, 'core/posts.html', context={"reviews": reviews})


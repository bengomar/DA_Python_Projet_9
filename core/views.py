from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value, Q
from django.shortcuts import redirect, render, get_object_or_404

from .forms import TicketForm, ReviewForm, UsersFollowForm, DeleteTicketForm, DeleteReviewForm
from .models import Ticket, Review, UserFollow
from django.contrib import messages
from authentication.models import User


@login_required
def home(request):
    # Récupération des utilisateurs suivis par l'utilisateur connecté
    user_following = UserFollow.objects.filter(user=request.user).values_list('followed_user', flat=True)

    # Récupération des tickets liés aux utilisateurs suivis ou à l'utilisateur connecté
    tickets = Ticket.objects.filter(
        Q(user__in=user_following) | Q(user=request.user)
    )

    # Annotation du type de contenu pour les tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # Récupération des critiques liées aux utilisateurs suivis ou à l'utilisateur connecté
    reviews = Review.objects.filter(
        Q(user__in=user_following) | Q(user=request.user)
    )

    # Annotation du type de contenu pour les critiques
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

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
        review_form = ReviewForm(request.POST)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = Ticket.objects.last()
            review.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'core/create_review_with_ticket.html', context=context)


@login_required
def display_posts(request):
    """
    Display all ticket and review from user connected
    """
    tickets = Ticket.objects.filter(user__exact=request.user)
    reviews = Review.objects.filter(user__exact=request.user)

    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.time_created, reverse=True)

    posts = list(posts)

    return render(request, 'core/posts.html', context={"posts": posts})


@login_required
def create_review_from_ticket(request, ticket):
    form = ReviewForm()
    if request.method == 'POST':
        # print(request.FILES.getlist('image'))
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket_id = ticket
            # now we can save
            review.save()
            return redirect('home')
    return render(request, 'core/create_review.html', context={'form': form})


@login_required
def follow_users(request):
    context = {}
    if request.method == 'POST':
        form = UsersFollowForm(request.POST)
        if form.is_valid():
            follower = form.cleaned_data['followed_user']
            try:
                user = User.objects.get(username__exact=follower)
            except User.DoesNotExist:
                user = None

            if user and user != request.user:  # Vérification si l'utilisateur n'est pas lui-même
                UserFollow.objects.create(user=request.user, followed_user=user)
                return redirect('follow_users')
            else:
                # Ajouter un message d'erreur indiquant que l'abonnement à soi-même n'est pas autorisé
                messages.error(request, "Vous ne pouvez pas vous abonner à vous-même.")
    else:
        form = UsersFollowForm()

    context['form'] = form
    context['following'] = UserFollow.objects.filter(user=request.user)
    context['followed_by'] = UserFollow.objects.filter(followed_user=request.user)
    return render(request, 'core/follow_users_form.html', context)


@login_required
def delete_follow(request, user_id):
    user = User.objects.get(id__exact=user_id)
    follow = UserFollow.objects.get(
        user__exact=request.user, followed_user__exact=user
    )
    if follow:
        follow.delete()
    return redirect('follow_users')


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    delete_form = DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = TicketForm(request.POST,
                                   request.FILES,
                                   instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
        if 'delete_ticket' in request.POST:
            delete_form = DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('posts')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'core/edit_ticket.html',
                  context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    edit_form = ReviewForm(instance=review)
    delete_form = DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = ReviewForm(request.POST,
                                   request.FILES,
                                   instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
        if 'delete_review' in request.POST:
            print('Check')
            delete_form = DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('posts')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'core/edit_review.html',
                  context=context)

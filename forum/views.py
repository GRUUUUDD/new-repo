from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from users.mixins import TSZHMemberRequiredMixin, tszh_member_required
from .models import Post, Comment
from .forms import PostForm, CommentForm
from .utils import check_profanity


class ForumView(ListView):
    model = Post
    template_name = 'forum.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related(
            Prefetch(
                'comments',
                queryset=Comment.objects.filter(is_approved=True).select_related('author'),
                to_attr='approved_comments'
            )
        ).order_by('-created_at')


@login_required
@tszh_member_required
def create_post(request):
    if not request.user.is_tszh_member:
        raise PermissionDenied("Только члены ТСЖ могут создавать посты")
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('forum')
    else:
        post_form = PostForm()
    return render(request, 'forum/create_post.html', {
        'post_form': post_form,
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.is_approved = not check_profanity(comment.content)
            comment.save()
    return redirect('forum')


@method_decorator(login_required, name='dispatch')
class DeletePostView(TSZHMemberRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('forum')
    template_name = 'forum/post_confirm_delete.html'

    def get_queryset(self):
        if self.request.user.is_tszh_member:
            return Post.objects.all()
        return Post.objects.none()
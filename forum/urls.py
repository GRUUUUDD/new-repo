from django.urls import path
from .views import ForumView, create_post, add_comment, DeletePostView

urlpatterns = [
    path('', ForumView.as_view(), name='forum'),
    path('create/', create_post, name='create_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),

]
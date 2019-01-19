from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
# Create your views here.


class Index(generic.TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = models.Book.objects.all().count()
        context['num_instances'] = models.BookInstance.objects.all().count()
        context['num_instances_available'] = models.BookInstance.objects.filter(
            status__exact='a').count()
        context['num_authors'] = models.Author.objects.all().count()
        return context


class BookListView(generic.ListView):
    template_name = 'catalog/book_list.html'
    context_object_name = 'book_list '
    model = models.Book


class BookDetailView(generic.DetailView):
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'
    model = models.Book


class AuthorListView(generic.ListView):
    template_name = 'catalog/author_list.html'
    model = models.Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    model = models.BookInstance
    paginate_by = 10

    def get_queryset(self):
        return models.BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

    # def index(request):
    #     num_books=models.Book.objects.all().count()
    #     num_instances=models.BookInstance.objects.all().count()
    #     num_instances_available=models.BookInstance.objects.filter(status__exact='a').count()
    #     num_authors=models.Author.objects.all().count()
    #
    #     return render(request, 'catalog/index.html', context={
    #     'num_books':num_books,
    #     'num_instances' : num_instances,
    #     'num_instances_available' : num_instances_available,
    #     'num_authors' : num_authors
    #     })

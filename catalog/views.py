from django.shortcuts import render, reverse, get_object_or_404

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .forms import RenewBookForm
from . import models
import datetime


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


@permission_required('catalog.can_mark_returned')
def renew_book_libration(request, pk):
    book_inst = get_object_or_404(models.BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm[request.POST]

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('catalog:my-borrowed'))
        else:
            proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
            form = RenewBookForm(
                initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_libration.html', {'form': form, 'bookinst': book_inst})

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

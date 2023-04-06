
import csv
import datetime
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Project, Category, Expense
from django.views.generic import CreateView
from django.utils.text import slugify
from .forms import ExpenseForm
import json
from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request,'budget/register.html', context)

def login(request):
    return render(request,'budget/login.html')

def project_list(request):
    project_list = Project.objects.all()
    # category_list = Category.objects.filter(project=project_list)
    return render(request, 'budget/project-list.html', {'project_list': project_list})

def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    if request.method == 'GET':
        category_list = Category.objects.filter(project=project)
        return render(request, 'budget/project-detail.html', {'project': project, 'expense_list': project.expenses.all(), 'category_list': category_list})

    elif request.method == 'POST':
        # process the form
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            category = get_object_or_404(Category, project=project, name=category_name)

            Expense.objects.create(
                project=project,
                title=title,
                amount=amount,
                category=category
            ).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = Expense.objects.get(id=id)
        expense.delete()

        return HttpResponse('')

    return HttpResponseRedirect(project_slug)


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'budget/add-project.html'
    fields = ('name', 'budget')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                project=Project.objects.get(id=self.object.id),
                name=category
            ).save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['name'])

def home(request):
    return render(request,'budget/index.html')

def group(request):
    return render(request, 'budget/group_record.html')

def export_csv(request,project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses.csv'

    writer = csv.writer(response)
    writer.writerow(['project','title','amount','category'])

    expenses = Expense.objects.filter(project=project)

    for expense in expenses:
        writer.writerow([expense.project,expense.title, expense.amount, expense.category])

    if request == 'GET':
        return response

# Signup

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class UsersListView(ListView):
    model = ShopUser
    template_name = "adminapp/users.html"
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')
    # fields = '__all__'
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'пользователи/cоздание'
        return context

# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/cоздание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': title,
#         'user_form': user_form,
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')
    fields = '__all__'
    #form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': title,
#         'user_form': edit_form,
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user_to_delete'
    success_url = reverse_lazy('admin_staff:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'категории/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     context = {
#         'title': title,
#         'user_to_delete': user,
#     }
#
#     return render(request, 'adminapp/user_delete.html', context)


class ProductCategoriesListView(ListView):
    model = ProductCategory
    template_name = "adminapp/categories.html"
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('-is_active', 'name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoriesListView, self).get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     context = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', context)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     category_form = ProductCategoryEditForm()
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#
#     context = {
#         'title': title,
#         'category_form': category_form,
#     }
#
#     return render(request, 'adminapp/category_update.html', context)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    #fields = '__all__'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, instance=edit_category)
#
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#
#     context = {
#         'title': title,
#         'category_form': edit_form
#     }
#
#     return render(request, 'adminapp/category_update.html', context)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    context_object_name = 'product_to_delete'
    success_url = reverse_lazy('admin_staff:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'категории/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('admin_staff:categories'))
#
#     context = {
#         'title': title,
#         'category_to_delete': category,
#     }
#
#     return render(request, 'adminapp/category_delete.html', context)


class ProductsListView(ListView):
    model = Product
    template_name = "adminapp/products.html"
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['category'] = self.kwargs['pk']
        context['title'] = 'админка/продукты'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     context = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', context)

# class ProductCreateView(CreateView):
#     model = Product
#     template_name = 'adminapp/product_update.html'
#     success_url = reverse_lazy('admin_staff:products')
#     fields = '__all__'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ProductCreateView, self).get_context_data(**kwargs)
#         context['title'] = 'продукт/cоздание'
#         return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    #переход сделала на категории
    success_url = reverse_lazy('admin_staff:categories')
    # fields = '__all__'
    form_class = ProductEditForm
    #не смогла сделать, чтобы категория автоматически подставлялась

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'продукт/cоздание'
        context['category'] = self.kwargs['pk']
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'продукт/cоздание'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
#
#     else:
#         product_form = ProductEditForm(initial={'category': category})
#
#     context = {
#         'title': title,
#         'update_form': product_form,
#     }
#
#     return render(request, 'adminapp/product_update.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт/подробнее'

    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': title,
        'object': product,
    }

    return render(request, 'adminapp/product_read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[edit_product.pk]))

    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'form': edit_form,
        'category': edit_product.category
    }

    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product,
    }

    return render(request, 'adminapp/product_delete.html', context)

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from adminapp.forms import ShopUserAdminEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users_list'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'form': user_form,
    }
    return render(request, 'adminapp/user_form.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     users_list = ShopUser.objects.all().order_by('-is_active')
#
#     context = {
#         'object_list': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)


class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users_list'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)

    context = {
        'form': user_form,
    }

    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        if current_user.is_active:
            current_user.is_active = False
        else:
            current_user.is_active = True
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users_list'))
    context = {
        'object': current_user,
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    return None


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'object_list': categories_list
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request):
    return None


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request):
    return None


#@user_passes_test(lambda u: u.is_superuser)
#def product_create(request):
#    return None


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm
    #success_url = reverse_lazy('adminapp:category_list')

    def get_success_url(self):
        return reverse('adminapp:products_list', args=[self.kwargs['pk']])


#@user_passes_test(lambda u: u.is_superuser)
#def products(request, pk):
#    title = 'админка/продукт'
#
#    category = get_object_or_404(ProductCategory, pk=pk)
#    products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#    context = {
#        'title': title,
#        'category': category,
#        'object_list': products_list,
#    }
#
#    return render(request, 'adminapp/products.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))


#@user_passes_test(lambda u: u.is_superuser)
#def product_update(request):
#    return None


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm
    #success_url = reverse_lazy('adminapp:category_list')

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:products_list', args=[product_item.category_id])


#@user_passes_test(lambda u: u.is_superuser)
#def product_delete(request):
#    return None


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:products_list', args=[product_item.category_id])


#@user_passes_test(lambda u: u.is_superuser)
#def product_detail(request):
#    return None


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'
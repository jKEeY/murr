from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Murr


def murrs_list(requset):
    all_murrs = Murr.objects.filter().order_by('-timestamp')
    paginator = Paginator(all_murrs, 2)
    page_request_ver = 'page'
    page = requset.GET.get(page_request_ver)
    try:
        paginator_queriset = paginator.page(page)
    except PageNotAnInteger:
        paginator_queriset = paginator.page(1)
    except EmptyPage:
        paginator_queriset = paginator.page(paginator.num_pages)

    latest = Murr.objects.order_by('-timestamp')[0:2]
    context = {
        'murrs': paginator_queriset,
        'page_request_ver': page_request_ver,

        'latest': latest
    }
    return render(requset, 'Murr_card/murr_list.html', context)


def murr_detail(request, pk):
    murr_detail = get_object_or_404(Murr, pk=pk)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            # TODO что это?
            form.instance.post = murr_detail
            form.save()
    context = {
        'murr_detail': murr_detail,
        'form': form
    }
    return render(request, 'Murr_card/murr_detail.html', context)

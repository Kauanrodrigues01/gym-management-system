from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from members.forms import MemberForm
from members.models import Member
from django.shortcuts import get_object_or_404
from members.forms import MemberEditForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'admin_painel/pages/home.html')

@login_required
def members(request):
    form = MemberForm()
    context = {
        'form': form,
        'members': Member.objects.all()
    }
    return render(request, 'admin_painel/pages/members.html', context)

@login_required
def edit_member_view(request, id):
    member = get_object_or_404(Member, id=id)

    form_data_edit_member = request.session.get('form_data_edit_member')
    
    if form_data_edit_member:
        form = MemberEditForm(form_data_edit_member, instance=member)
        request.session['form_data_edit_member'] = None 
    else:
        form = MemberEditForm(instance=member)

    return render(request, 'admin_painel/pages/member_edit.html', {'form': form, 'member': member})

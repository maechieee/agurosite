from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import Genders, Users
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator

# Create your views here.

def gender_list(request): 
  try:  
    genders = Genders.objects.all() #SELECT * FROM tbl_genders;

    data = {
      'genders': genders
    }

    return render(request, 'gender/GendersList.html', data)
  except Exception as e:
    return HttpResponse(f'Error occured during load genders: {e}')

def add_gender(request):
  try:
    if request.method == 'POST':
      gender = request.POST.get('gender')

      Genders.objects.create(gender=gender).save() #INSERT INTO tbl_genders (gender) VALUES (gender);
      messages.success(request, 'Gender added successfully!')
      return redirect('/gender/list/')
    else: 
      return render(request, 'gender/AddGender.html')
  except Exception as e:
    return HttpResponse(f'Error occured during add gender: {e}')
  
def edit_gender(request, genderId):
  try:
    if request.method=='POST':
      genderObj = Genders.objects.get(pk=genderId) #SELECT * FROM tbl_genders WHERE id = genderId;

      gender = request.POST.get('gender')

      genderObj.gender = gender
      genderObj.save() #UPDATE tbl_genders SET gender = gender WHERE gender_id = genderId;

      messages.success(request, 'Gender updated successfully!')

      data = {
        'gender': genderObj
      }

      return render(request, 'gender/EditGender.html', data)
    else: 
      genderObj = Genders.objects.get(pk=genderId) #SELECT * FROM tbl_genders WHERE id = genderId;

      data = {
        'gender': genderObj
      }

      return render(request, 'gender/EditGender.html', data)
    
  except Exception as e:
    return HttpResponse(f'Error occured during edit gender: {e}')
  
def delete_gender(request, genderId):
  try:
    if request.method == 'POST':
      genderObj = Genders.objects.get(pk=genderId) #SELECT * FROM tbl_genders WHERE id = genderId;
      genderObj.delete() #DELETE FROM tbl_genders WHERE gender_id = genderId;

      messages.success(request, 'Gender deleted successfully!')
      return redirect('/gender/list/')
    else:
      genderObj = Genders.objects.get(pk=genderId) #SELECT * FROM tbl_genders WHERE id = genderId;

      data = {
        'gender': genderObj
      }

      return render(request, 'gender/DeleteGender.html', data)
  except Exception as e:
    return HttpResponse(f'Error occured during delete gender: {e}')
  
def user_list(request):
    try:
        query = request.GET.get('q', '').strip()
        usersObj = Users.objects.select_related('gender').all().order_by('full_name') #SELECT * FROM tbl_users ORDER BY full_name ASC;

        months = {
          'january': 1, 'jan': 1,
          'february': 2, 'feb': 2,
          'march': 3, 'mar': 3,
          'april': 4, 'apr': 4,
          'may': 5,
          'june': 6, 'jun': 6,
          'july': 7, 'jul': 7,
          'august': 8, 'aug': 8,
          'september': 9, 'sep': 9,
          'october': 10, 'oct': 10,
          'november': 11, 'nov': 11,
          'december': 12, 'dec': 12,
        }

        if query:
            query_lower = query.lower()

            filters = (
                Q(full_name__icontains=query) |
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(address__icontains=query) |
                Q(contact_number__icontains=query) |
                Q(birth_date__icontains=query) |
                Q(gender__gender__iexact=query)
            )

            if query_lower in months:
              filters = filters | Q(birth_date__month=months[query_lower])

            usersObj = usersObj.filter(filters)
        
        paginator = Paginator(usersObj, 15)
        page_number = request.GET.get('page')
        users = paginator.get_page(page_number)

        data = {
            'users': users,
            'query': query
        }

        return render(request, 'user/UsersList.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during load users: {e}')
  
def add_user(request):
  try:
    if request.method == 'POST':
      fullName = request.POST.get('full_name')
      gender = request.POST.get('gender')
      birthDate = request.POST.get('birth_date')
      address = request.POST.get('address')
      contactNumber = request.POST.get('contact_number') 
      email = request.POST.get('email') 
      username = request.POST.get('username')
      password = request.POST.get('password')
      confirmPassword = request.POST.get('confirm_password') 
      profilePicture = request.FILES.get('profile_picture')

      if not fullName or not gender or not birthDate or not address or not contactNumber or not username or not password or not confirmPassword:
        messages.error(request, 'Please fill in all required fields.')
        return redirect('/user/add/')

      if Users.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists. Please choose another username.')
        return redirect('/user/add/')
      
      if not contactNumber.isdigit():
        messages.error(request, 'Contact number must contain only numbers.')
        return redirect('/user/add/')

      if not password or not confirmPassword:
        messages.error(request, 'Password is required!')
        return redirect('/user/add/')

      if password != confirmPassword:
        messages.error(request, 'Password and Confirm Password does not match!')
        return redirect('/user/add/')

      Users.objects.create(
        full_name = fullName,
        gender = Genders.objects.get(pk=gender), 
        birth_date = birthDate,
        address = address,
        contact_number = contactNumber,
        email = email,
        username = username,
        password = make_password(password),
        profile_picture = profilePicture
      ).save()

      messages.success(request, 'User added successfully!')
      return redirect('/user/add/')

    else:
      genderObj = Genders.objects.all()

      data = {
        'genders': genderObj
      }

      return render(request, 'user/AddUser.html', data)

  except Exception as e:
    return HttpResponse(f'Error occured during add user: {e}')
  
def edit_user(request, userId):
  try:
    userObj = Users.objects.get(pk=userId)

    if request.method == 'POST':
      fullName = request.POST.get('full_name')
      gender = request.POST.get('gender')
      birthDate = request.POST.get('birth_date')
      address = request.POST.get('address')
      contactNumber = request.POST.get('contact_number')
      email = request.POST.get('email')
      username = request.POST.get('username')
      profilePicture = request.FILES.get('profile_picture')

      if not fullName or not gender or not birthDate or not address or not contactNumber or not username:
        messages.error(request, 'Please fill in all required fields.')
        return redirect(f'/user/edit/{userId}/')

      if Users.objects.filter(username=username).exclude(pk=userId).exists():
        messages.error(request, 'Username already exists. Please choose another username.')
        return redirect(f'/user/edit/{userId}/')
      
      if not contactNumber.isdigit():
        messages.error(request, 'Contact number must contain only numbers.')
        return redirect(f'/user/edit/{userId}/')

      userObj.full_name = fullName
      userObj.gender = Genders.objects.get(pk=gender)
      userObj.birth_date = birthDate
      userObj.address = address
      userObj.contact_number = contactNumber
      userObj.email = email
      userObj.username = username

      if profilePicture:
        userObj.profile_picture = profilePicture

      userObj.save()

      messages.success(request, 'User updated successfully!')
      return redirect('/user/list/')

    else:
      genders = Genders.objects.all()

      data = {
        'user': userObj,
        'genders': genders
      }

      return render(request, 'user/EditUser.html', data)

  except Exception as e:
    return HttpResponse(f'Error occured during edit user: {e}')
  
def delete_user(request, userId):
  try:
    userObj = Users.objects.get(pk=userId)

    if request.method == 'POST':
      userObj.delete()
      messages.success(request, 'User deleted successfully!')
      return redirect('/user/list/')

    data = {
      'user': userObj
    }

    return render(request, 'user/DeleteUser.html', data)

  except Exception as e:
    return HttpResponse(f'Error occured during delete user: {e}')
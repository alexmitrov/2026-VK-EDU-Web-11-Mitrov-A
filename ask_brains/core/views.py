from django.shortcuts import render, redirect

users = [
    {
        'id': 1,
        'username': 'mr_pelican',
        'email': 'pelican@mail.ru',
        'nickname': 'Mr. Pelican',
        'avatar': 'core/img/avatar.jpeg'
    }
]


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            return redirect('index')

    return render(request, 'core/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        password_rep = request.POST.get('password_rep')

        if password != password_rep:
            return render(request, 'core/signup.html', {
                'error': 'Пароли не совпадают',
                'username': username,
                'email': email,
                'nickname': nickname
            })

        if username and email and password:
            return redirect('login')

    return render(request, 'core/signup.html')


def profile_view(request):
    user = users[0]

    if request.method == 'POST':
        user['username'] = request.POST.get('username', user['username'])
        user['email'] = request.POST.get('email', user['email'])
        user['nickname'] = request.POST.get('nickname', user['nickname'])

        return redirect('profile')

    return render(request, 'core/profile.html', {'user': user})

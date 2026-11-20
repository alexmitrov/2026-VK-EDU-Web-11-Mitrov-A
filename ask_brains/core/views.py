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

        return render(request, 'core/login.html', {
            'error': 'Неверное имя или пароль',
            'username': username,
        })

    return render(request, 'core/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        password_rep = request.POST.get('password_rep')
        avatar = request.FILES.get('avatar')

        if password != password_rep:
            return render(request, 'core/signup.html', {
                'error': 'Пароли не совпадают',
                'username': username,
                'email': email,
                'nickname': nickname,
            })

        if not (username and email and password):
            return render(request, 'core/signup.html', {
                'error': 'Заполните обязательные поля',
                'username': username,
                'email': email,
                'nickname': nickname,
            })

        if '@' not in email:
            return render(request, 'core/signup.html', {
                'email_error': 'Некорректный email.',
                'username': username,
                'email': email,
                'nickname': nickname,
            })

        new_id = max([u['id'] for u in users]) + 1 if users else 1
        users.append({
            'id': new_id,
            'username': username,
            'email': email,
            'nickname': nickname,
            'avatar': 'core/img/avatar.jpeg',
        })
        return redirect('login')

    return render(request, 'core/signup.html')


def profile_view(request):
    user = users[0]

    if request.method == 'POST':
        username = request.POST.get('username', user['username'])
        email = request.POST.get('email', user['email'])
        nickname = request.POST.get('nickname', user['nickname'])

        if not username:
            return render(request, 'core/profile.html', {
                'user': user,
                'error': 'Логин не может быть пустым.',
            })

        user['username'] = username
        user['email'] = email
        user['nickname'] = nickname

        avatar = request.FILES.get('avatar')
        if avatar:
            user['avatar'] = 'core/img/' + avatar.name

        return redirect('profile')

    return render(request, 'core/profile.html', {'user': user})

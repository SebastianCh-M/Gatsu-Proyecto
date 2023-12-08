def is_admin(request):
    if request.user.is_authenticated:
        return {'is_admin': request.user.groups.filter(name='Administrador').exists()}
    return {'is_admin': False}

def is_usuario_registrado(request):
    if request.user.is_authenticated:
        return {'is_usuario_registrado': request.user.groups.filter(name='UsuarioRegistrado').exists()}
    return {'is_usuario_registrado': False}

def is_usuario_suscrito(request):
    if request.user.is_authenticated:
        return {'is_usuario_suscrito': request.user.groups.filter(name='UsuarioSuscrito').exists()}
    return {'is_usuario_suscrito': False}


def user_type(request):
    user_type = None
    user_class = None
    is_admin = False  # Agrega esto para definir el estado de administrador
    user_image = None
    user_color = '#fff'  # Color por defecto

    if request.user.is_authenticated:
        if request.user.groups.filter(name='Administrador').exists():
            user_type = 'Admin'
            user_class = 'admin-user'
            is_admin = True  # Configura a True si el usuario es un administrador
            user_image = 'admin.png'
            user_color = '#00BFFF'
        elif request.user.groups.filter(name='UsuarioRegistrado').exists():
            user_type = 'Free'
            user_class = 'free-user'
            user_image = 'free.png'
            user_color = '#999999'
        elif request.user.groups.filter(name='UsuarioSuscrito').exists():
            user_type = 'Premium'
            user_class = 'premium-user'
            user_image = 'premium.png'
            user_color = '#FFD700'

    return {
        'user_type': user_type,
        'user_class': user_class,
        'is_admin': is_admin,
        'user_image': user_image,
        'user_color': user_color,
    }

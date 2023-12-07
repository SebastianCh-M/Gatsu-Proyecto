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

    if request.user.is_authenticated:
        if request.user.groups.filter(name='Administrador').exists():
            user_type = 'Admin'
            user_class = 'admin-user'
            is_admin = True  # Configura a True si el usuario es un administrador

        elif request.user.groups.filter(name='UsuarioRegistrado').exists():
            user_type = 'Free'
            user_class = 'free-user'
        elif request.user.groups.filter(name='UsuarioSuscrito').exists():
            user_type = 'Premium'
            user_class = 'premium-user'

    return {'user_type': user_type, 'user_class': user_class, 'is_admin': is_admin}
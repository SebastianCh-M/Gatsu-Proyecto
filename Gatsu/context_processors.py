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


def is_admin(request):
    if request.user.is_authenticated:
        return {'is_admin': request.user.groups.filter(name='Administrador').exists(), 'user_color': '#038701'}
    return {'is_admin': False, 'user_color': ''}

def is_usuario_registrado(request):
    if request.user.is_authenticated:
        return {'is_usuario_registrado': request.user.groups.filter(name='UsuarioRegistrado').exists(), 'user_color': '#FFF'}
    return {'is_usuario_registrado': False, 'user_color': ''}

def is_usuario_suscrito(request):
    if request.user.is_authenticated:
        return {'is_usuario_suscrito': request.user.groups.filter(name='UsuarioSuscrito').exists(), 'user_color': '#FFD700'}
    return {'is_usuario_suscrito': False, 'user_color': ''}

def user_type(request):
    user_type = None
    user_image = None
    user_color = '#fff'  # Color por defecto

    if request.user.is_authenticated:
        if request.user.groups.filter(name='Administrador').exists():
            user_type = 'Admin'
            user_image = 'admin.png'
            user_color = '#00BFFF'
        elif request.user.groups.filter(name='UsuarioRegistrado').exists():
            user_type = 'Free'
            user_image = 'free.png'
            user_color = '#fff'
        elif request.user.groups.filter(name='UsuarioSuscrito').exists():
            user_type = 'Premium'
            user_image = 'premium.png'
            user_color = '#FFD700'

    return {'user_type': user_type, 'user_image': user_image, 'user_color': user_color}

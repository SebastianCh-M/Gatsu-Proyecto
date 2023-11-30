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
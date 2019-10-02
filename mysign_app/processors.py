def menu_items_processor(request):
    menu_items = []
    if request.path.startswith('/admin'):
        menu_items = {'admin_door_devices': 'Devices overview', 'admin_companies': 'Companies', 'admin_users': 'Users'}

    return {
        'menu_items': menu_items
    }

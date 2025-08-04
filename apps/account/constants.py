ADMIN_PERMISSION_DEFAULT = {
    "user": {
        "create": True,
        "read": True,
        "update": True,
        "delete": True,
    },
    "product": {
        "create": True,
        "read": True,
        "update": True,
        "delete": True,
    },
    "product_category": {
        "create": True,
        "read": True,
        "update": True,
        "delete": True,
    },
}

USER_PERMISSION_DEFAULT = {
    "user": {
        "read": True,
        "create": False,
        "update": False,
        "delete": False,
    },
    "product": {
        "read": True,
        "create": False,
        "update": False,
        "delete": False,
    },
    "product_category": {
        "read": False,
        "create": False,
        "update": False,
        "delete": False,
    },
}

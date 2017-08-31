config = {'backend': 'PyQt5'}


def use(name):
    config['backend'] = name


def get_backed():
    return config['backend']

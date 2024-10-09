import tinytuya

devices = {
    1: {
        'dev_id': 'bfd256167b549ae3e5kt0g',
        'address': '192.168.0.195',
        'local_key': '1Eh;8BmOtzyDP$h*',
        'version': 3.4
    },
    2: {
        'dev_id': 'bfd256167b549ae3e5kt0g',
        'address': '192.168.0.195',
        'local_key': '1Eh;8BmOtzyDP$h*',
        'version': 3.4
    }
}


def get_device(device_id: int):
    device_info = devices.get(device_id)
    if not device_info:
        raise ValueError(f"Устройство с ID {device_id} не найдено")
    return tinytuya.OutletDevice(
        dev_id=device_info['dev_id'],
        address=device_info['address'],
        local_key=device_info['local_key'],
        version=device_info['version']
    )


def get_device_status(device):
    status = device.status()
    if 'Error' in status:
        return {'error': status['Error']}
    return status


def handle_device_action(device_id: int, action):
    try:
        device = get_device(device_id)
        status = get_device_status(device)

        if 'error' in status:
            return status

        current_state = status['dps']['1']

        if action == 'turn_on' and not current_state:
            device.turn_on()
            return {'status': False, 'response': True}
        elif action == 'turn_off' and current_state:
            device.turn_off()
            return {'status': True, 'response': True}
        else:
            return {'status': current_state, 'response': True}
    except Exception as e:
        return {'error': str(e)}


# def turn_on(device_id: int):
#     return handle_device_action(device_id, 'turn_on')
#
#
# def turn_off(device_id: int):
#     return handle_device_action(device_id, 'turn_off')


def turn_on(device_id: int):
    return {'status': False, 'response': True}


def turn_off(device_id: int):
    return {'status': True, 'response': True}


def get_status(device_id: int):
    try:
        device = get_device(device_id)
        status = get_device_status(device)

        if 'error' in status:
            return status

        return {'status': status['dps']['1']}
    except Exception as e:
        return {'error': str(e)}
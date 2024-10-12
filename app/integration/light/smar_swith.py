import json
import tinytuya


class TuyaDeviceManager:
    def __init__(self, devices_file):
        self.devices = self.load_devices(devices_file)
        self.devices_id = {
            1: "bfd256167b549ae3e5kt0g"
        }

    def load_devices(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def get_device(self, device_id):
        if isinstance(device_id, int):
            device_id = self.devices_id.get(device_id)
            if not device_id:
                raise ValueError(f"Числовой ID {device_id} не найден в словаре devices_id")

        device_info = next((device for device in self.devices if device['id'] == device_id), None)
        if not device_info:
            raise ValueError(f"Устройство с ID {device_id} не найдено")
        return tinytuya.OutletDevice(
            dev_id=device_info['id'],
            address=device_info['ip'],
            local_key=device_info['key'],
            version=float(device_info['version'])
        )

    def get_device_status(self, device):
        status = device.status()
        if 'Error' in status:
            return {'error': status['Error']}
        return status

    def handle_device_action(self, device_id, action):
        try:
            device = self.get_device(device_id)
            status = self.get_device_status(device)

            if 'error' in status:
                return status

            current_state = status['dps']['1']

            if action == 'turn_on' and not current_state:
                device.turn_on()
                return {'status': False}
            elif action == 'turn_off' and current_state:
                device.turn_off()
                return {'status': True}
            else:
                return {'status': current_state}
        except Exception as e:
            return {'error': str(e)}

    def turn_on(self, device_id):
        return self.handle_device_action(device_id, 'turn_on')

    def turn_off(self, device_id):
        return self.handle_device_action(device_id, 'turn_off')

    def get_status(self, device_id):
        try:
            # device = self.get_device(device_id)
            # status = self.get_device_status(device)
            #
            # if 'error' in status:
            #     return status

            # return {'status': status['dps']['1']}
            return {'status': True}
        except Exception as e:
            return {'error': str(e)}

    def get_ip_from_mac(self, mac_address):
        try:
            with open('/proc/net/arp', 'r') as f:
                arp_table = f.read()
        except IOError:
            return "Ошибка при чтении ARP-таблицы"

        mac_address = mac_address.lower()
        for line in arp_table.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 4:
                ip = parts[0]
                mac = parts[3].lower()
                if mac == mac_address:
                    return ip

        return "MAC-адрес не найден"

    def update_device_ip(self):
        for device in self.devices:
            ip = self.get_ip_from_mac(device['mac'])
            if ip != "MAC-адрес не найден" and ip != "Ошибка при чтении ARP-таблицы":
                device['ip'] = ip

    def save_devices(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.devices, f, indent=2)


light = TuyaDeviceManager('app/integration/light/devices.json')

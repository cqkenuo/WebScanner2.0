import ipaddress
import re
import json
import socket

import nmap

from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PyQt5.QtWidgets import QWidget


class MenuShowBack(QWidget):
    """
    点击菜单按钮出现的动画效果
    """

    def __init__(self, widget, checked, animation_targets, menu_btn, animation_targets_pos, duration):
        self.widget = widget
        self.checked = checked
        self.animation_targets = animation_targets
        self.menu_btn = menu_btn
        self.animation_targets_pos = animation_targets_pos
        self.duration = duration

    def menu(self):
        """
        展示动画效果
        :return:
        """

        animation_group = QSequentialAnimationGroup(self.widget)
        for idx, target in enumerate(self.animation_targets):
            animation = QPropertyAnimation()
            animation.setTargetObject(target)
            animation.setPropertyName(b"pos")
            animation.setStartValue(self.menu_btn.pos())
            animation.setEndValue(self.animation_targets_pos[idx])
            animation.setDuration(self.duration)
            animation.setEasingCurve(QEasingCurve.InOutBounce)
            animation_group.addAnimation(animation)

        animation_group.setDirection(self.checked)
        animation_group.start(QAbstractAnimation.DeleteWhenStopped)


class CheckIpAddress:
    """
    检查输入的ip地址格式是否合法
    """

    def __init__(self, ip_address):
        self.ip_address = ip_address

    def check(self):
        # print(self.ip_address)
        try:
            ip_list = []
            if self.ip_address.find("-") > 0:
                try:
                    if len(self.ip_address[self.ip_address.find('-') + 1:]) <= 3:
                        last_dot_index = self.ip_address.rfind(".")
                        hyphen_index = self.ip_address.find("-")
                        start_ip = int(self.ip_address[last_dot_index + 1: hyphen_index])
                        end_ip = int(self.ip_address[hyphen_index + 1:])
                        for ip in range(start_ip, end_ip + 1):
                            ip_add = self.ip_address[:last_dot_index + 1] + str(ip)
                            ip_list.append(ip_add)
                        return ip_list
                    else:
                        return False
                except Exception as e:
                    print(e)
                    return False
            elif self.ip_address.find(".0/24") > 0:
                net = ipaddress.ip_network(self.ip_address)
                for ip in net:
                    ip_list.append(str(ip))
                return ip_list
            elif re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
                          r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", self.ip_address):
                ip_list.append(self.ip_address)
                return ip_list
        except Exception as e:
            print(e)
            return False

    def check_singleIp(self):
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
                    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", self.ip_address):
            return True
        else:
            return False


class CheckPort:
    def __init__(self, start_port, end_port):
        self.start_port = start_port
        self.end_port = end_port

    def check(self):
        check_format = r"^([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$"
        if re.match(check_format, self.start_port) \
                and re.match(check_format, self.end_port) \
                and int(self.start_port) <= int(self.end_port) or (self.start_port == '' and self.end_port == ''):

            return True
        else:
            return False


class ServiceScan:
    def __init__(self, network_prefix):
        self.network_prefix = network_prefix

    def scan(self):
        nm = nmap.PortScanner()
        # 配置nmap扫描参数
        scan_raw_result = nm.scan(hosts=self.network_prefix, arguments='-v -n -A')
        print(scan_raw_result)
        for host, result in scan_raw_result["scan"].items():
            if result['status']['state'] == 'up':
                try:
                    for port in result['tcp']:
                        print("端口号: ", port)
                        print("名字: ", result['tcp'][port]['name'])
                        print("产品: ", result['tcp'][port]['product'])
                        print("版本: ", result['tcp'][port]['version'])
                except:
                    pass

                try:
                    for port in result['udp']:
                        print("端口号: ", port)
                        print("名字: ", result['udp'][port]['name'])
                        print("产品: ", result['udp'][port]['product'])
                        print("版本: ", result['udp'][port]['version'])
                except:
                    pass


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        return "没有连接网络~"
    return ip

if __name__ == '__main__':
    scan = ServiceScan('192.168.43.221')
    scan.scan()

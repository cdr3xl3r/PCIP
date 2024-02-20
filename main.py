from flask import Flask, render_template, flash, redirect, url_for
import socket
import psutil
import platform
import subprocess
import os
import datetime
app = Flask(__name__)


def shutdown():
    os_name = platform.system()
    try:
        if os_name == 'Windows':
            subprocess.run(["shutdown", "/s", "/t", "0"])
        elif os_name == 'Linux':
            subprocess.run(["sudo", "shutdown", "now"])
        else:
            raise Exception("Unsupported OS")
    except Exception as e:
        return f"Error: {e}"
    return redirect(url_for('home'))
def get_ip_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    domain=socket.gethostbyaddr(hostname)
    return {"hostname": hostname, "ip_address": ip_address, "domain": domain}

def get_system_info():
    info = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().total,
        "available_memory": psutil.virtual_memory().available
    }
    return info
def internet_info():
    try:
        socket.create_connection(("www.google.com", 80))
        return "Internet is working"
    except OSError:
        return "Internet is not working"
def localTime():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def restartPC():
    import os
    os.system("shutdown /r /t 1")
    return "Restarting PC"
def get_network_info():
    interfaces = psutil.net_if_addrs()
    network_info = []
    for interface_name, interface_addresses in interfaces.items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                network_info.append({
                    "name": interface_name,
                    "ip_address": address.address,
                    "mac_address": address.mac
                })
    return network_info

def get_disk_info():
    disk_info = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                "mount_point": partition.mountpoint,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free
            })
        except OSError as e:
            print(f"Skipping {partition.mountpoint} due to error: {e}")
            # Optionally, you could add limited info about the inaccessible drive
            # disk_info.append({
            #     "mount_point": partition.mountpoint,
            #     "total": "Unknown",
            #     "used": "Unknown",
            #     "free": "Unknown"
            # })
    return disk_info
def get_system_info():
    # Example of gathering system info
    info = {
        "cpu_percent": psutil.cpu_percent(interval=1)
        # Add other system info you need
    }
    return info

def get_services_info():
    # Placeholder for services info
    # This requires a platform-specific approach
    services = [
        {"name": "Service1", "status": "Running"},
        {"name": "Service2", "status": "Stopped"}
    ]
    return services

# Define other data gathering functions similarly
@app.route('/')
def home():
    network_info = get_network_info()
    disk_info = get_disk_info()
    services = get_services_info()
    system_info = get_system_info()
    ip_info = get_ip_info()  # Call the function here

    # Call other data gathering functions and store their results

    return render_template('index.html', 
                           network_info=get_network_info(), 
                           disk_info=get_disk_info(), 
                           services=get_services_info(),
                           system_info=get_system_info(),
                           ip_info=get_ip_info(),
                           internet_info=internet_info(),
                           localTime=localTime()
                          )
@app.route('/reboot', methods=['POST'])
def reboot():
    os_name = platform.system()
    try:
        if os_name == 'Windows':
            subprocess.run(["shutdown", "/r", "/t", "0"])
        elif os_name == 'Linux':
            subprocess.run(["sudo", "reboot"])
        else:
            raise Exception("Unsupported OS")
    except Exception as e:
        return f"Error: {e}"
    return redirect(url_for('home'))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    os_name = platform.system()
    try:
        if os_name == 'Windows':
            subprocess.run(["shutdown", "/s", "/t", "0"])
        elif os_name == 'Linux':
            subprocess.run(["sudo", "shutdown", "now"])
        else:
            raise Exception("Unsupported OS")
    except Exception as e:
        return f"Error: {e}"
    return redirect(url_for('home'))


    


if __name__ == '__main__':
    host=get_ip_info()
    app.run(host=host['ip_address'], port=8080, debug=True)
    
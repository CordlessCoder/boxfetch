#!/bin/python
from importlib.machinery import SourceFileLoader
import os


def auto():
    try:
        with open("/etc/lsb-release", "r") as lsb:
            return (
                "".join([line * ("_ID" in line) for line in lsb])
                .strip()
                .split("=")[1]
                .strip('"')
                .lower()
            )
    except:
        return "arch"


path_to_logos = "/home/roman/Documents/boxfetch/logos"
logo = [
    "                                       ",
    "                                       ",
]
# logo = auto()
#######################
# Possible logos are: #
# arch_big            #
# Pop!_OS             #
# arch3               #
# arch_unicode        #
# arch                #
# debian              #
# armbian             #
# elementaryOS        #
# arch2               #
# archey3             #
# or set it to auto() #
#######################


# logo = SourceFileLoader("main", f"{path_to_logos}/{logo}.py").load_module().logo

logo = ["│" + line for line in logo]

logo = [f"╭{'─'*(len(logo[1])-1)}"] + logo

log_len = len(logo) - 1
hostname_override = "\033[1;39m"
color1 = "\033[1;31m"
color2 = "\033[1;35m"
color3 = "\033[1;39m"


def to_gb(a):
    return round((a) / (1024.0 * 1024 * 1024), 1)


def get_disk(path):
    status = os.statvfs(path)
    total = status.f_blocks * status.f_frsize
    free = status.f_bfree * status.f_frsize
    used = total - free
    percentage = used * 100 // total
    return f"{to_gb(used)}GiB / {to_gb(total)}GiB ({percentage}%)"


def get_cpu():
    with open("/proc/cpuinfo", "r") as cpuinfo:
        cpu = cpuinfo.read().split("\n")
        for i in range(len(cpu)):
            if "model name" in cpu[i]:
                return "".join(
                    (
                        cpu[i].split(": ")[-1],
                        "@"
                        + str(
                            round(
                                int(cpu[i + 3].split(": ")[-1].split(".")[0]) / 1000, 1
                            )
                        ).strip()
                        + "GHz"
                        if "@" not in cpu[i].split(": ")[-1]
                        else cpu[i].split(": ")[-1],
                    )
                )


def get_mem():
    with open("/proc/meminfo", "r") as meminfo:
        mem = meminfo.read().split("\n")
        for line in mem:
            if "MemTotal: " in line:
                total = int(line.split(" ")[-2])
                continue
            if "MemFree: " in line:
                memfree = int(line.split(" ")[-2])
                continue
            if "Buffers: " in line:
                buffers = int(line.split(" ")[-2])
                continue
            if "Cached: " in line and "Swap" not in line:
                cached = int(line.split(" ")[-2])
                continue
            if "Shmem: " in line:
                shared = int(line.split(" ")[-2])
                continue
            if "SReclaimable: " in line:
                reclaimable = int(line.split(" ")[-2])
                continue
    try:
        used_memory = (
            total + shared - memfree - buffers - cached - reclaimable
        ) // 1024
    except:
        return None
    total_memory = total // 1024
    percentage = used_memory * 100 // total_memory
    return f"{used_memory} MiB / {total_memory}MiB ({percentage}%)"


data = [
    os.popen('echo ${USER:-$(id -un || printf %s "${HOME/*\/}")}', "r").read().strip()
    + "@",
    hostname_override + os.popen("hostnamectl hostname", "r").read().strip(),
    "bar",
    "",
    "OS: ",
    os.popen(
        'cat /etc/os-release | grep "NAME=" | cut -d\'"\' -f2 | cut -d"\n" -f-1', "r"
    )
    .read()
    .strip()
    + " "
    + os.popen("uname -m", "r").read(),
    "Uptime: ",
    os.popen("uptime -p", "r")
    .read()[3:]
    .replace("minutes", "mins")
    .replace("days", "d"),
    "Kernel: ",
    os.popen("uname -r", "r").read(),
    "Packages: ",
    len(os.listdir("/var/lib/pacman/local")) - 1,
    "Explicit: ",
    os.popen(
        'cat /tmp/.explicit 2>/dev/null || sh -c "pacman -Qeq | wc -l > /tmp/.explicit && cat /tmp/.explicit"'
    ).read(),
    "bar",
    "",
    "Resolution: ",
    os.popen("xdpyinfo  | grep -oP 'dimensions:\s+\K\S+'", "r").read(),
    "Theme: ",
    os.popen('cat ~/.config/gtk-3.0/settings.ini | grep "gtk-theme-name"', "r")
    .read()
    .split("=")[-1],
    "Font: ",
    os.popen('cat ~/.config/gtk-3.0/settings.ini | grep "gtk-font-name"', "r")
    .read()
    .split("=")[-1],
    "Browser:",
    os.popen(
        'cat /usr/share/applications/$(xdg-mime query default x-scheme-handler/http) | grep "Name=" -m 1 | cut -d"=" -f2-',
        "r",
    ).read(),
    "bar",
    "",
    "WM: ",
    os.popen(
        "xprop -id `xprop -root -notype _NET_SUPPORTING_WM_CHECK | awk '{print $5}'` | tail -n 1 | awk '{print toupper($4)}' | tr -d '\"'",
        "r",
    ).read(),
    "Shell: ",
    os.popen("echo $SHELL", "r").read().split("/")[-1],
    "Terminal: ",
    os.popen("xprop -id `xdo id` | grep 'WM_CLASS(STRING)'", "r").read().split('"')[-2],
    "Prompt: ",
    os.popen(
        """fish -c "echo Starship v(starship --version | grep -e 'starship' | cut -d' ' -f2-)" """
        "r",
    ).read(),
    "bar",
    "",
    "CPU: ",
    get_cpu().replace(" Eight-Core Processor", " "),
    "GPU: ",
    os.popen(
        'cat /tmp/.gpuname 2>/dev/null || sh -c "nvidia-smi --query-gpu=name --format=csv,noheader,nounits > /tmp/.gpuname && cat /tmp/.gpuname"',
        "r",
    )
    .read()
    .replace("NVIDIA", "NoVideo")
    .replace("GeForce", "OhGee!")
    .replace("GTX", "Core i3"),
    "Memory: ",
    get_mem(),
    "Disk(/): ",
    get_disk("/"),
    "bar",
    "",
]
names, data = [data[x] for x in range(0, len(data), 2)], [
    str(data[x]).strip() for x in range(1, len(data), 2)
]


data2 = data
names2 = names
for i in range(len(logo) - len(names)):
    names2.append("")
    data2.append("")
logo = [x + "│" if names2[i] != "bar" else x + "├" for i, x in enumerate(logo)]

target = max([len(x) for x in names2])
target2 = max([len(x) for x in data2]) + 1
names, data = names2, data2
names = [
    " " + x + " " * (target - len(x))
    if x != "bar"
    else color1 + "─" * (target + target2 + 1) + "┤"
    for x in names
]

data = [
    " " * (target2 - len(x) - 1) + x + " " + color1 + "│" if x != "" else ""
    for x in data
]
# logo = [
#    logo[i]
#    if i < len(logo)
#    else "│" + " " * (len(logo[0]) - 2) + "│" * (names2[i] != "bar")
#    for i in range(len(names2))
# ]

for i in range(len(logo), len(names2)):
    logo.append(
        "│"
        + " " * (len(logo[0]) - 2)
        + "│" * (names2[i] != "bar")
        + "├" * (names2[i] == "bar")
    )  # making sure that logo and data lengths match by adding lines
    if i % 2 == 1:
        for x in range(len(logo) - 2, 1, -1):
            logo[x] = logo[x - 1][:-1] + logo[x][-1]
        logo[1] = "│" + " " * (len(logo[0]) - 2) + logo[1][-1]

names[0] = (
    " " * (int((target + target2) * 0.5) - len(names[0].strip())) + names[0].strip()
)
data[0] = data[0].strip()[:-1]
logo[0] = logo[0][:-1] + "╮"

logo[-1] = "╰" + "─" * (len(logo[0]) - 2) + "╯"
for i in range(len(names)):
    if names[i].count("┤") != 0:
        names[i] = names[i].replace("┤", "╮")
        break
for i in range(len(names) - 1, 0, -1):
    if names[i].count("┤") != 0:
        names[i] = names[i].replace("┤", "╯")
        break
if names[len(logo) - 1].strip() != "":
    logo[-1] = logo[-1][:-1] + "┴─"
    names[-1] = color1 + names[-1][1 + len(color1) :]
os.system("clear")
for i in range(len(names)):
    print(
        color1,
        logo[i],
        color2,
        names[i],
        color3,
        data[i],
        sep="",
    )
os.system(
    f"kitty +kitten icat --place {len(logo[0]) - 2}x{len(logo) - 2}@1x2 ./logo_arch_detailed_less.png"
)

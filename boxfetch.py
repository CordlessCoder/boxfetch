#!/bin/python
import os


logo = [
    "╭───────────────────────────────────────",
    "│                   -`                  ",
    "│                  .o+`                 ",
    "│                 `ooo/                 ",
    "│                `+oooo:                ",
    "│               `+oooooo:               ",
    "│               -+oooooo+:              ",
    "│             `/:-:++oooo+:             ",
    "│            `/++++/+++++++:            ",
    "│           `/++++++++++++++:           ",
    "│          `/+++ooooooooooooo/`         ",
    "│         ./ooosssso++osssssso+`        ",
    "│        .oossssso-````/ossssss+`       ",
    "│       -osssssso.      :ssssssso.      ",
    "│      :osssssss/        osssso+++.     ",
    "│     /ossssssss/        +ssssooo/-     ",
    "│   `/ossssso+/:-        -:/+osssso+-   ",
    "│  `+sso+:-`                 `.-/+oso:  ",
    "│ `++:.                           `-/+/ ",
    "│ .`                                 `/ ",
    "╰───────────────────────────────────────",
]


log_len = len(logo) - 1
color1 = "\033[1;31m"
color2 = "\033[1;35m"
color3 = "\033[1;37m"


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
                        "@ "
                        + str(
                            int(cpu[i + 3].split(": ")[-1].split(".")[0]) / 1000
                        ).strip()
                        + "GHz",
                    )
                )
                break


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
    used_memory = (total + shared - memfree - buffers - cached - reclaimable) // 1024
    total_memory = total // 1024
    percentage = used_memory * 100 // total_memory
    return f"{used_memory} MiB / {total_memory}MiB ({percentage}%)"


data = [
    os.popen('echo ${USER:-$(id -un || printf %s "${HOME/*\/}")}', "r").read().strip()
    + "@",
    os.popen("hostnamectl hostname", "r").read().strip(),
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
    "Resolution: ",
    os.popen("xdpyinfo  | grep -oP 'dimensions:\s+\K\S+'", "r").read(),
    "Theme: ",
    os.popen('cat ~/.config/gtk-3.0/settings.ini | grep "gtk-theme-name"', "r")
    .read()
    .split("=")[-1],
    "bar",
    "",
    "Browser:",
    os.popen(
        "cat /usr/share/applications/chromium.desktop | grep Name= -m 1 | cut -d= -f2-",
        "r",
    ).read(),
    "Packages: ",
    len(os.listdir("/var/lib/pacman/local")) - 1,
    # "Explicit: ",
    # os.popen("pacman -Qe | wc -l", "r").read(),
    "WM: ",
    os.popen(
        "xprop -id `xprop -root -notype _NET_SUPPORTING_WM_CHECK | awk '{print $5}'` | tail -n 1 | awk '{print toupper($4)}' | tr -d '\"'",
        "r",
    ).read(),
    "Shell: ",
    os.popen("echo $SHELL", "r").read().split("/")[-1],
    "Term: ",
    os.popen("xprop -id `xdo id` | grep 'WM_CLASS(STRING)'", "r").read().split('"')[-2],
    "Prompt: ",
    os.popen("fish -c 'echo Pure $pure_version'", "r").read(),
    "bar",
    "",
    "CPU: ",
    get_cpu().replace(" Eight-Core Processor", " "),
    "GPU: ",
    os.popen(
        "echo $(nvidia-smi --query-gpu=name --format=csv,noheader,nounits)",
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
names, func = [data[x] for x in range(0, len(data), 2)], [
    str(data[x]).strip() for x in range(1, len(data), 2)
]

func2 = func
names2 = names
for i in range(len(logo) - len(names)):
    names2.append("")
    func2.append("")
logo = [x + "│" if names2[i] != "bar" else x for i, x in enumerate(logo)]

target = max([len(x) for x in names2])
target2 = max([len(x) for x in func2]) + 1
names, func = names2, func2
names = [
    " " + x + " " * (target - len(x))
    if x != "bar"
    else color1 + "├" + "─" * (target + target2 + 1) + "┤"
    for x in names
]

func = [
    " " * (target2 - len(x) - 1) + x + " " + "\033[1;31m│" if x != "" else ""
    for x in func
]
logo = [
    logo[i] if i < len(logo) else "" for i in range(max(len(data), len(logo)))
]  # making sure that logo and data lengths match by adding in blank lines

names[0] = (
    " " * (int((target + target2) * 0.5) - len(names[0].strip())) + names[0].strip()
)
func[0] = func[0].strip()[:-1]
logo[0] = logo[0][:-1] + "╮"
logo[log_len] = logo[log_len][:-1] + "╯"
for i in range(len(names)):
    if names[i].count("┤") != 0:
        names[i] = names[i].replace("┤", "╮")
        break
for i in range(len(names) - 1, 0, -1):
    if names[i].count("┤") != 0:
        names[i] = names[i].replace("┤", "╯")
        break
for i in range(len(names)):
    print(
        color1,
        logo[i],
        color2,
        names[i],
        color3,
        func[i],
        sep="",
    )

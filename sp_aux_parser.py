from collections import defaultdict
import subprocess
from datetime import datetime
from typing import Any


def run_subprocess()->list:
    result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split('\n')

def parse_processes(lines):
    users_processes = defaultdict(list)
    total_mem = 0.0
    total_cpu = 0.0

    max_mem_command = [0.0,'']
    max_cpu_command = [0.0,'']

    for line in lines[1:]:
        parts = line.split(maxsplit=10)
        if len(parts) < 11:
            continue
        user, _, cpu,mem, *_, command = line.split(maxsplit=10)
        try:
            mem = float(mem)
            cpu = float(cpu)
        except ValueError:
            continue
        users_processes[user].append(command)
        total_mem += mem
        total_cpu += cpu
        if mem > max_mem_command[0]:
            max_mem_command = [mem, command]

        if cpu > max_cpu_command[0]:
            max_cpu_command = [cpu, command]
    return users_processes, len(lines), total_mem, total_cpu, max_mem_command, max_cpu_command

def generate_report(users_processes_: defaultdict[Any, list],
                    total_process_: int,
                    total_mem_: float,
                    total_cpu_: float,
                    max_mem_command_: list,
                    max_cpu_command_: list):
    report = []
    report.append("Отчёт о состоянии системы:")
    report.append(f"Пользователи системы: '{', '.join(users_processes_.keys())}'")
    report.append(f"Процессов запущено: {total_process_}\n")

    report.append("Пользовательских процессов:")
    for user, user_processes in users_processes_.items():
        report.append(f"{user}: {len(user_processes)}")

    report.append(f"\nВсего памяти используется: {total_mem_:.1f} %")
    report.append(f"Всего CPU используется: {total_cpu_:.1f} %")
    report.append(f"Больше всего памяти ({max_mem_command_[0]:.1f} %) использует: {format_command(max_mem_command_[1])}")
    report.append(f"Больше всего CPU ({max_cpu_command_[0]:.1f} %) использует: {format_command(max_cpu_command_[1])}")
    return "\n".join(report)

def format_command(command, max_length=20):
    if len(command) > max_length:
        return command[:max_length] + "..."
    return command

def save_to_file(text):
    filename = datetime.now().strftime("%d-%m-%Y–%H:%M-sp_aux_report.txt")
    with open(filename, "w") as f:
        f.write(text)
    print(f"\nОтчет сохранен в файл: {filename}")

def main():
    lines_ps = run_subprocess()
    users_processes_ps, total_process, total_mem, total_cpu, max_mem_command, max_cpu_command = parse_processes(lines_ps)
    report_ps = generate_report(users_processes_ps, total_process, total_mem, total_cpu, max_mem_command, max_cpu_command)
    print(report_ps)
    save_to_file(report_ps)


if __name__ == "__main__":
    main()

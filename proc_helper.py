import psutil


def main():
    for p in psutil.process_iter():
        if p.pid == 23904:
            print(p.pid, p.name())
            print(p.cmdline(), p.environ())
    return 0


if __name__ == "__main__":
    main()

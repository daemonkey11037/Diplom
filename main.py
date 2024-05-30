import modules.scanner as scanner
import modules.vulncheck as vulncheck
import modules.logs as logs
import sqlite3
from colorama import Fore, Style
from cmd2 import Cmd


class App(Cmd):

    prompt = 'archael > '

    def do_scanner(self, args):

        class Scan(Cmd):
            prompt = 'archael scan() > '

            def do_scan(self, args):
                scanner.main(str(args))

            def do_back(self, args):
                return True
            
        app = Scan()
        app.cmdloop()

    def do_view(self, args):
        vulncheck.main()

    def do_logs(self, args):
        logs.main()

    def do_clean(self, args):
        scanner.clean(args)

    def do_quit(self, args):
        return True

if __name__ == '__main__':
    app = App()
    app.cmdloop()

import modules.scanner as scanner
import modules.vulncheck as vulncheck
import modules.logs as logs
from modules.functions import service_check
from cmd2 import Cmd

if service_check() == True:
    print('Сервис успешно создан!')
else:
    print('Что-то пошло не так!')

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

    def do_vulncheck(self, args):
        vulncheck.main()

    def do_logs(self, args):
        
        class Logs(Cmd):
            prompt = 'archael logs() > '

            def do_host(self, args):
                logs.main(str(args))

        app = Logs()
        app.cmdloop()

    def do_clean(self, args):
        scanner.clean(args)

    def do_quit(self, args):
        return True

if __name__ == '__main__':
    app = App()
    app.cmdloop()

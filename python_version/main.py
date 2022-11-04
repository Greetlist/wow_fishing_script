import window_operation
import argh

def run():
    helper = window_operation.WindowsHelper()
    if not helper.init():
        return
    helper.start()

def test():
    helper = window_operation.WindowsHelper(is_test=True)
    if not helper.init():
        print("Cannot init, Exit")
        return
    helper.test()

if __name__ == "__main__":
    argh.dispatch_commands([run, test])
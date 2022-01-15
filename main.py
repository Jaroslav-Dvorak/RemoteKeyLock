from sim import inst_alarm
from server import Server_thread, Server_inst
from logic import inst_logic


if __name__ == '__main__':
    Server_thread.start()
    inst_logic.start()
    inst_alarm.root.mainloop()
    Server_inst.server_close()

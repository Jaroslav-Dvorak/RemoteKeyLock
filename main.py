from sim import inst_alarm
from server import Server_thread, Server_inst
from logic import inst_logic


def is_rpi():
    try:
        with open('/sys/firmware/devicetree/base/model') as model:
            rpi_model = model.read()
    except FileNotFoundError:
        return False
    else:
        return rpi_model


if __name__ == '__main__':
    Server_thread.start()
    # inst_logic.start()
    # inst_alarm.root.mainloop()
    inst_logic.run()
    Server_inst.server_close()

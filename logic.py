from time import sleep, time
from threading import Thread
from control import Control, Alarm


inst_alarm = Alarm(buzz_pin=22)


class Logic(Thread):
    def __init__(self):
        super().__init__()
        # self.key_locks = {"N2O": Sim("left", "N2O", t_waggle=10, t_autolock=30, t_alarm=60),
        #                   "CO2": Sim("right", "CO2", t_waggle=10, t_autolock=30, t_alarm=60)}
        self.key_locks = {"n2o": Control(coil_pin=6, contact_pin=19, side="left", name="N2O", t_waggle=10, t_autolock=30, t_alarm=60),
                          "co2": Control(coil_pin=5, contact_pin=13, side="right", name="CO2", t_waggle=10, t_autolock=30, t_alarm=60)}

    def msg_decision(self, msg):
        msg = msg.split(",")
        name = "person?"
        if len(msg) == 2:
            msg, name = msg[0], msg[1]
            name = name.strip()
        else:
            msg = msg[0]
        msg = msg.lower()
        try:
            self.key_locks[msg].key_unlock()
        except KeyError:
            print("Uknown command:", msg)
        else:
            print(msg, name, "unlocked!")

    def loop(self, key_lock):
        ok = True
        if key_lock.key_taken:
            if key_lock.key_unlocked:
                if (time() - key_lock.key_taken) > key_lock.t_waggle:
                    key_lock.key_ready_to_return = True
                if (time() - key_lock.key_taken) > key_lock.t_alarm:
                    print(key_lock.name + ": return key timeout")
                    ok = False
            else:
                print(key_lock.name + ": vyrváno!")
                ok = False
        elif not key_lock.key_taken and key_lock.key_ready_to_return:
            key_lock.key_lock()
            key_lock.key_ready_to_return = False
        elif not key_lock.key_taken and key_lock.key_unlocked:
            if (time() - key_lock.key_unlocked) > key_lock.t_autolock:
                key_lock.key_lock()
        return ok

    def run(self):
        while True:
            alarm = False
            for inst in self.key_locks.values():
                if not self.loop(inst):
                    alarm = True
            inst_alarm.command(alarm)
            sleep(1)


inst_logic = Logic()
inst_logic.daemon = True

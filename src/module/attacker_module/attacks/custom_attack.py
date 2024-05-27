
from module.attacker_module.attacks.base_attack import Attack

import time

class CookieAttack(Attack):
    
    def __init__(self, attack_payload) -> None:
        super().__init__(attack_payload)

    def attack(self):
        
        print("🍪💀 Currently attacking :: cookie || [SIM] ~ 15s dly")
        time.sleep(15)
        print("🎊 Cookie attack completed ! 🎊")

class FileFolderDiscoveryAttack(Attack):
    
    def __init__(self, attack_payload) -> None:
        super().__init__(attack_payload)

    def attack(self):

        print("📁💀 Currently attacking :: file folder discovery || [SIM] ~ 20s dly")
        time.sleep(20)
        print("🎊 File folder discovery attack completed ! 🎊")
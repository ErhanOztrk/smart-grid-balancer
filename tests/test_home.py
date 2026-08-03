from home import SmartHome
from appliance import Appliance, Priority

def test_critical_appliance_not_turned_off():
    # 1. ARRANGE: Create a home with ONLY a critical appliance
    my_home = SmartHome("House_001")
    fridge = Appliance("Fridge", 0.8, Priority.CRITICAL)
    fridge.turn_on()
    my_home.add_appliance(fridge)

    # 2. ACT: Force a price spike
    my_home.react_to_price(100.0)
    
    # 3. ASSERT: Prove the fridge is still on!
    assert fridge.is_on is True
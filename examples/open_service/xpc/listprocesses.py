import pprint

import miru

device = miru.get_usb_device()

appservice = device.open_service("xpc:com.apple.coredevice.appservice")
response = appservice.request(
    {
        "CoreDevice.featureIdentifier": "com.apple.coredevice.feature.listprocesses",
        "CoreDevice.action": {},
        "CoreDevice.input": {},
    }
)
pprint.pp(response)

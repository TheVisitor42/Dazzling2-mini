from oled import (
    initialize_oleds,
    test_display
)


print("Starting OLED test")


initialize_oleds()

print("OLEDs initialized")


test_display(0)

print("OLED 0 done")


test_display(1)

print("OLED 1 done")

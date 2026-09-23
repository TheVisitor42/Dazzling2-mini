#change this to main.py in the receiver pico

from oled import initialize_oleds, display_text

print("Starting OLED test...")

initialize_oleds()

display_text(0, "WEATHER", "Fort Worth","TEMP", "100 Degrees F")
display_text(1, "STOCKS", "BRK.B  $510.32","NTDOY $13.67", "NKE $36.39")
display_text(2, "TODO", "1. Test UART","2. Test API","3. Flash/FRAM")
display_text(3, "TIME", "12:34 AM", "DATE", "2026.09.17")

print("OLED test complete.")

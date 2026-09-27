import usocket

HOST = "open-weather13.p.rapidapi.com"

print()
print("================================")
print("DNS TEST")
print("================================")

print("Resolving:")
print(HOST)

try:

    result = usocket.getaddrinfo(
        HOST,
        443
    )

    print()
    print("DNS SUCCESS")
    print(result)

except Exception as error:

    print()
    print("DNS FAILED")
    print("Error:", error)

from tasks.weather_task import WeatherTask


weather_task = WeatherTask()


# ----------------------------------------------------
# TEST 1 — FIRST SUCCESS
# ----------------------------------------------------

print()
print("================================")
print("TEST 1: FIRST SUCCESS")
print("================================")

result = weather_task.run()

print()
print("RESULT:")
print(result)


# ----------------------------------------------------
# TEST 2 — FAILURE
# ----------------------------------------------------

weather_task.simulate_failure = True


print()
print("================================")
print("TEST 2: API FAILURE")
print("================================")

result = weather_task.run()

print()
print("RESULT:")
print(result)

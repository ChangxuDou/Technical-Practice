point = {"x": 1, "y": 2}
# list()
# tuple()
# set()
# dict()

point = dict(x=1, y=2)

point["x"] = 10
point["z"] = 20
if "a" in point:
    print(point["a"])
print(point.get("a", 0))  # 0 is default number
del point["x"]
print(point)

# for key in point:
#     print(key, point[key])


# for x in point.items():
#     print(x)

for key, value in point.items():
    print(key, value)

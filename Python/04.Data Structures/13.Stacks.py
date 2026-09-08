# LIFO
# last in first out

browsing_session = []
browsing_session.append(1)
browsing_session.append(2)
browsing_session.pop()
if not browsing_session:
    print("disable")
else:
    print(browsing_session[-1])

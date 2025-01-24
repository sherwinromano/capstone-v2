item = slice("one", "two", "three")

s, p, o = item.start, item.stop, item.step

if isinstance(item, slice):
    print(s)

armies = int(input())

if armies >= 1000:
    print("legion")
elif armies >= 500:
    print("swarm")
elif armies >= 50:
    print("horde")
elif armies >= 10:
    print("pack")
elif armies >= 1:
    print("few")
else:
    print("no army")

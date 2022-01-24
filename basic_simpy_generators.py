import simpy


def create_generator(env):
    string = ''
    while True:
        string += 'X'
        print(string)
        yield env.timeout(1)


# gen = create_generator()
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))

environment = simpy.Environment()
environment.process(create_generator(environment))
environment.run(5)

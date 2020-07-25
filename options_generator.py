class Choice:

    def __init__(self, name, choices, del_price):
        self.choices = choices
        self.del_price = del_price
        self.name = name

    def __str__(self):
        return str(self.name) + "|" + "|".join([str(c) + ":" + str(p) for c, p in zip(self.choices, self.del_price)])

    def choose(self, choice):
        try:
            return self.choices[choice].del_price
        except IndexError:
            raise IndexError("Choice is not present.")


class Options:

    def __init__(self, options):
        self.options = options

    def __str__(self):
        return "||".join([str(c) for c in self.options])

    def choose(self, choices):

        del_price = 0

        for c, o in zip(choices, self.options):
            del_price += o.choose(c)

        return del_price


h = Options([
    Choice("Stain", ["Natural", "Cherry", "Walnut"], [0, 5, 10]),
    Choice("Size", ["Small", "Medium", "Large"], [0, 10, 20])
])

print(str(h))

"""
out = ""

options = int(input("Number of options: "))

for i in range(options):
    out += input("Name of option: ")
    out += "|"

    choices = int(input("Number of choices: "))

    for j in range(choices):
        out += input("Name of choice: ")
        out += ":"
        out += str(int(input("Amount affected by original price: ")))
        if j + 1 != choices:
            out += "|"

    print()

    if i + 1 != options:
        out += "||"

print(out)
"""
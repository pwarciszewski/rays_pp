import pp_lens

space = pp_lens.lab_space()

space.add_lens(30, -10)
space.add_lens(-40, 20)
space.add_lens(-100, 50)
print(space.get_effl())
space.show()
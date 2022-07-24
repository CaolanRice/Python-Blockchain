#*args returning tuple, **keyword_args returning dictionary, can 
def unlimited_arguments(**keyword_args):
    print(keyword_args)
    for k, argument in keyword_args.items():
        print (k, argument)

unlimited_arguments(name='Caolan', age=29, hehe='Haha', weather='warm')
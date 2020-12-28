#%%
import multiprocessing

def popo():
    print('yup')
    pass

    # p1 = p(target = monk_throws, args=(num,))
    # p2 = p(target = brute_throws, args=(num,))
    # p3 = p(target = feller_throws, args=(num,))
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=popo)
    p2 = multiprocessing.Process(target=popo)
    p3 = multiprocessing.Process(target=popo)

    p1.start()
    p2.start()
    p3.start()


    p1.join()
    p2.join()
    p3.join()

# %%

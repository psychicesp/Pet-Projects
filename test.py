#%%
#print("Ran the whole file")
import multiprocessing
def test():
    print('yup')
    pass


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=test)
    p2 = multiprocessing.Process(target=test)
    p3 = multiprocessing.Process(target=test)

    p1.start()
    p2.start()
    p3.start()


    p1.join()
    p2.join()
    p3.join()

# %%

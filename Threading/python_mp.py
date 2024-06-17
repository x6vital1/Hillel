import multiprocessing as mp
import time

def get_lucky_tickets(ticket):
    ticket_str = str(ticket).zfill(8)
    sum_first_part = sum(int(digit) for digit in ticket_str[:3])
    sum_second_part = sum(int(digit) for digit in ticket_str[3:])
    return sum_first_part == sum_second_part

def get_count(start, end, res):
    count = 0
    for ticket in range(start, end):
        if get_lucky_tickets(ticket):
            count += 1
    res.put(count)

def main():
    start = time.time()
    res1 = mp.Queue()
    res2 = mp.Queue()
    res3 = mp.Queue()
    res4 = mp.Queue()
    p1 = mp.Process(target=get_count, args=(1, 2_500_000, res1))
    p2 = mp.Process(target=get_count, args=(2_500_001, 5_000_000, res2))
    p3 = mp.Process(target=get_count, args=(5_000_001, 7_500_000, res3))
    p4 = mp.Process(target=get_count, args=(7_500_001, 10_000_000, res4))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    total_count = res1.get() + res2.get() + res3.get() + res4.get()
    end = time.time()
    print(f'Total count: {total_count}, time: {end - start}')

if __name__ == '__main__':
    main()
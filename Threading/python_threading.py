import threading as th
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
    res.append(count)

def main():
    start = time.time()
    res1 = []
    res2 = []
    res3 = []
    res4 = []
    th1 = th.Thread(target=get_count, args=(1, 2_500_000, res1))
    th2 = th.Thread(target=get_count, args=(2_500_001, 5_000_000, res2))
    th3 = th.Thread(target=get_count, args=(5_000_001, 7_500_000, res3))
    th4 = th.Thread(target=get_count, args=(7_500_001, 10_000_000, res4))
    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th1.join()
    th2.join()
    th3.join()
    th4.join()
    total_count = sum(res1) + sum(res2) + sum(res3) + sum(res4)
    end = time.time()
    print(f'Total count: {total_count}, time: {end - start}')

if __name__ == '__main__':
    main()
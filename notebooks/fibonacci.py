def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    else:
        list_fib = [0, 1]
        while len(list_fib) < n:
            next_fib = list_fib[-1] + list_fib[-2]
            list_fib.append(next_fib)
        return list_fib

if __name__ == '__main__':
    num_terms = 10  # You can change this number
    fib_sequence = fibonacci(num_terms)
    print(f"Fibonacci sequence up to {num_terms} terms: {fib_sequence}")
def digit_stack(commands):
    stack = [0, [0]]
    for string_command in commands:
        command = string_command.split()
        if command[0] == 'PUSH':
            stack[1] += [int(command[1])]
        elif command[0] == 'PEEK':
            stack[0] += stack[1][-1]
        elif command[0] == 'POP':
            stack[0] += stack[1].pop()
        if len(stack[1]) == 0:
            stack[1].append(0)
    return stack[0]


if __name__ == '__main__':
    print("Example:")
    print(digit_stack(["PUSH 3", "POP", "POP", "PUSH 4", "PEEK",
                       "PUSH 9", "PUSH 0", "PEEK", "POP", "PUSH 1", "PEEK"]))

    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert digit_stack(["PUSH 3", "POP", "POP",
                        "PUSH 4", "PEEK", "PUSH 9",
                        "PUSH 0", "PEEK", "POP",
                        "PUSH 1", "PEEK"]) == 8, "Example"
    assert digit_stack(["POP", "POP"]) == 0, "pop, pop, zero"
    assert digit_stack(["PUSH 9", "PUSH 9", "POP"]) == 9, "Push the button"
    assert digit_stack([]) == 0, "Nothing"
    assert digit_stack(["PUSH 3", "PUSH 3", "PUSH 0",
                        "POP", "PEEK", "PUSH 0",
                        "PUSH 2", "PUSH 5", "PUSH 1"]) == 3, "Extra 1"
    assert digit_stack(["PUSH 0", "PUSH 5", "POP",
                        "PUSH 9", "PUSH 3", "POP",
                        "PUSH 5", "PUSH 6", "PUSH 2",
                        "PUSH 7", "POP", "POP",
                        "PUSH 3", "PUSH 0", "PUSH 9",
                        "POP"]) == 26, "Extra 2"
    assert digit_stack(["POP", "PUSH 1", "POP",
                        "PUSH 8", "PEEK", "POP"]) == 17, "Extra 3"
    assert digit_stack(["POP", "PUSH 6", "PEEK",
                        "POP", "POP", "PUSH 1",
                        "POP", "PUSH 3", "POP",
                        "POP", "POP", "PEEK",
                        "PUSH 5", "PEEK", "PUSH 3",
                        "PEEK", "PEEK", "POP"]) == 30, "Extra 4"
    assert digit_stack(["PUSH 1", "PEEK", "PUSH 2",
                        "PUSH 1", "PEEK", "PUSH 1",
                        "PUSH 9", "PEEK", "PEEK",
                        "PUSH 8"]) == 20, "Extra 5"

    print("Coding complete? Click 'Check' to review your tests and earn cool rewards!");

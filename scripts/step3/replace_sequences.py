
def replace_sequences(input_list):
    my_list = sorted(set(input_list))
    previous = my_list[0]
    segments = []
    current_segment = [previous]
    for current in my_list[1:]:
        if current != previous + 1:
            current_segment.append(previous)
            segments.append(current_segment)
            current_segment = [current]
        previous = current
    current_segment.append(current)
    segments.append(current_segment)

    items = []
    for segment in segments:
        if segment[0] == segment[1]:
            items.append(str(segment[0]))
        elif segment[0] + 1 == segment[1]:
            items.extend(str(_) for _ in segment)
        else:
            items.append(f"{segment[0]}..{segment[1]}")
    index_list = ','.join(items)
    return index_list

foo = [0, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13]

print(foo)
print(replace_sequences(foo))

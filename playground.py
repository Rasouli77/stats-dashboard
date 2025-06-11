# leet 1: Two Sum: easy
def special_sum(nums: list, target: int):
    output = []
    for one in nums:
        for two in nums:
            if one != two and one + two == target:
                index_one = nums.index(one)
                index_two = nums.index(two)
                output.append(index_one)
                output.append(index_two)
    
    items = []
    for item in output:
        items.append(item)
        if item in items:
            output.remove(item)

    export = []
    for n in output:
        export.append(n)
        if len(export) == 2:
            if export[0] > export[1]:
                export[0], export[1] = export[1], export[0]
            print(export)
        if len(export) >= 2:
            export.clear()

special_sum([1, 2, 3, 4], 5)

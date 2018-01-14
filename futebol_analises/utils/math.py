def gini(sample):
    sample = sorted(sample)
    height, area = 0, 0
    for value in sample:
        height += value
        area += height - value / 2.
    total_area = height * len(sample) / 2.
    return (total_area - area) / total_area
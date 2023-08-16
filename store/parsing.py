import csv
from store.gpuItem import GpuItem


def gpuCSV_parser(data):
    gpu_List: list[GpuItem] = []
    for entries in data:
        gpu = GpuItem()
        gpu.image = entries[0]
        gpu.brand = entries[1]
        gpu.link = entries[2]
        gpu.name = entries[3]
        if entries[4] is not None:
            try:
                gpu.current_price = float(entries[4].split("$")[1])
            except:
                gpu.current_price = float(entries[4].split("$")[1].replace(",", ""))
        if entries[5] is not None:
            try:
                gpu.previous_price = float(entries[5].split("$")[1])
            except:
                gpu.previous_price = float(entries[5].split("$")[1].replace(",", ""))
        if entries[6] is not None:
            gpu.savings = int(entries[6].split("%")[0])
        if entries[7] is not None:
            gpu.shipping = entries[7]
        if entries[8] is not None:
            gpu.item_rating = float(entries[8].split()[1])
        if entries[9] is not None:
            try:
                gpu.ratings_num = int(entries[9])
            except:
                gpu.ratings_num = int(entries[9].replace(",", ""))
        if any(x.name == entries[3] for x in gpu_List):
            continue
        else:
            gpu_List.append(gpu)
    return gpu_List


def sort_best_value(data) -> list[GpuItem]:
    item_list = gpuCSV_parser(data)
    bayasian_list: list[GpuItem] = []
    for item in item_list:
        item.bayasian_calc()
        bayasian_list.append(item)
    sorted_bayasian = sorted(
        bayasian_list,
        key=lambda x: (x.bayasian_avg, -x.current_price, x.savings),
        reverse=True,
    )
    result = []
    for item in sorted_bayasian:
        result.append(item.item_to_list())
    return result[:25]

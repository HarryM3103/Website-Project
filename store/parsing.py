import csv
from store.gpuItem import GpuItem


def gpuCSV_parser():
    gpu_List: list[GpuItem] = []
    with open("GPU.csv", "r") as f:
        counter = 0
        reader = csv.reader(f)
        next(reader, None)
        for line in reader:
            if counter != 1:
                counter += 1
                continue
            gpu = GpuItem()
            gpu.image = line[0]
            gpu.brand = line[1]
            gpu.link = line[2]
            gpu.name = line[3]
            if line[4] != "":
                try:
                    gpu.current_price = float(line[4].split("$")[1])
                except:
                    gpu.current_price = float(line[4].split("$")[1].replace(",", ""))
            if line[5] != "":
                try:
                    gpu.previous_price = float(line[5].split("$")[1])
                except:
                    gpu.previous_price = float(line[5].split("$")[1].replace(",", ""))
            if line[6] != "":
                gpu.savings = int(line[6].split("%")[0])
            if line[7] != "":
                gpu.shipping = line[7]
            if line[8] != "":
                gpu.item_rating = float(line[8].split()[1])
            if line[9] != "":
                try:
                    gpu.ratings_num = int(line[9])
                except:
                    gpu.ratings_num = int(line[9].replace(",", ""))
            if any(x.name == line[3] for x in gpu_List):
                continue
            else:
                gpu_List.append(gpu)
    return gpu_List


def sort_best_value() -> list[GpuItem]:
    item_list = gpuCSV_parser()
    bayasian_list: list[GpuItem] = []
    for item in item_list:
        item.bayasian_calc()
        bayasian_list.append(item)
    sorted_bayasian = sorted(
        bayasian_list,
        key=lambda x: (x.bayasian_avg, -x.current_price, x.savings),
        reverse=True,
    )
    return sorted_bayasian[:25]

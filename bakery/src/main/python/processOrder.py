import logging
import json


def readOrder():
    logging.info("Inside readOrder method")
    order = input("Please Enter your order (qty <space> code): ")
    orderList = order.split(" ")
    print("Your order is::::::", orderList)
    qty = int(orderList[0])
    code = str(orderList[1])
    processOrder(qty, code)


def processOrder(qty, code, ordered_dict=None):
    logging.info("Inside processOrder method")
    print("qty:::::::::", qty)
    print("code:::::::", code)

    with open('../../../data/data.json') as f:
        products = json.load(f)

    print("products::::::::", products[code])

    packArr = getPackArray(products, code)

    minPacks = calculateMinPacks(qty, packArr)

    ordered_dict = products[code]
    ordered_price_dict = ordered_dict["packs"]
    printReceipt(code, qty, minPacks, ordered_price_dict)


def getPackArray(products, code):
    logging.info("Inside getPackArray method")
    print("product_Info::::", products[code])
    ordered_item = products[code]
    packs = ordered_item["packs"]
    print("packs:::::::", packs)
    # iterate through packs and retrieve packs and corresponding prices
    packArr = []
    for key in packs:
        packArr.append(key)

    return packArr


def calculateMinPacks(orderQty, packArr):
    logging.info("Inside calculateMinPacks method")
    print("packArr inside calculateMinPacks::", packArr)
    packArr = sorted(packArr, reverse=True)
    print("Sorted Array is::", packArr)
    result = {}
    for pack in packArr:
        if orderQty == pack:
            print("packQty::::::", 1)
            result.__setitem__(str(1), str(pack))
        elif int(orderQty) % int(pack) == 0:
            print("In else::")
            result.__setitem__(str(int(orderQty) // int(pack)), str(pack))
            print("result:::::::", result)
            break
        elif int(orderQty) > int(pack):
            if str(int(orderQty) % int(pack)) not in packArr:
                continue
            else:
                packQty = int(orderQty) // int(pack)
                result.__setitem__(str(packQty), str(pack))
                orderQty = int(orderQty) - (int(pack) * packQty)
                calculateMinPacks(orderQty, packArr)
        else:
            print("Packs Unavailable.")
    print("result:::::::::", result)
    return result


def printReceipt(code, qty, minPacks, ordered_price_dict):
    print("Inside printReceipt:::::")
    print("minPacks inside printReceipt::::", minPacks)
    total_price = 0
    SPACE = " "
    CURRENCY = "$"
    denomination = ""
    for packKey in minPacks:
        print("packkey:::", str(packKey))
        packValue = minPacks[str(packKey)]
        print("packValue:::", str(packValue))
        pack_price = ordered_price_dict[packValue]
        print(pack_price)
        total_price = total_price + int(packKey) * pack_price
        print(round(total_price,2))
        denomination = denomination + "\t"+str(packKey)+SPACE+"X"+SPACE+str(packValue)+SPACE+CURRENCY+str(pack_price)+"\n"

    print(str(qty)+SPACE+code+SPACE+"$"+str(round(total_price,2)))
    print(denomination)


if __name__ == "__main__":
    logging.basicConfig(filename='../../../logs/app.log', format='%(asctime)s - %(message)s', level=logging.INFO)
    readOrder()

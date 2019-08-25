import logging
import json


def readOrder():
    logging.info("Inside readOrder method")
    order=input("Please Enter your order (qty <space> code): ")
    orderList=order.split(" ")
    print("Your order is::::::", orderList)
    qty=int(orderList[0])
    code=str(orderList[1])
    if findProduct(code):
        processOrder(qty, code)


def findProduct(code):
    with open('../../../data/data.json') as f:
        products=json.load(f)

    found=False
    for key in products.keys():
        if key == code:
            found=True
    return found


def processOrder(qty, code, ordered_dict=None):
    logging.info("Inside processOrder method")
    print("qty:::::::::", qty)
    print("code:::::::", code)

    with open('../../../data/data.json') as f:
        products=json.load(f)

    print("products::::::::", products[code])

    packArr=getPackArray(products, code)

    minPacks=calculateMinPacks(qty, packArr)
#    if len(minPacks) > 0:
    ordered_dict=products[code]
    ordered_price_dict=ordered_dict["packs"]
    printReceipt(code, qty, minPacks, ordered_price_dict)
#    else:
#        print("No packs available.  Please choose valid quantity")
#        minPacks=["Invalid quantity. No packs available for given quantity."]
#        return minPacks


def getPackArray(products, code):
    logging.info("Inside getPackArray method")
    print("product_Info::::", products[code])
    ordered_item=products[code]
    packs=ordered_item["packs"]
    print("packs:::::::", packs)
    # iterate through packs and retrieve packs and corresponding prices
    packArr=[]
    for key in packs:
        packArr.append(key)

    return packArr


def calculateMinPacks(orderQty, packArr, result=[]):
    logging.info("Inside calculateMinPacks method")
    print("packArr inside calculateMinPacks::", packArr)
    multiples=[1, 2, 3, 4, 5, 6, 7, 8, 9]
    packArr=sorted(packArr, reverse=True)
    print("Sorted Array is::", packArr)
    for i in range(len(packArr)):
        if int(orderQty > 0):
            packSize=packArr[i]
            if int(orderQty) == int(packSize):
                result.append(str(1) + ":" + str(packSize))
                break
            elif int(orderQty) % int(packSize) == 0:
                packQty=int(orderQty) // int(packSize)
                result.append(str(int(orderQty) // int(packSize)) + ":" + str(packSize))
                break
            elif int(orderQty) > int(packSize):
                for j in range(len(packArr)):
                    packSize=packArr[j]
                    possibleSizeArr=[]
                    if (j + 1) == len(packArr):
                        index=j
                    else:
                        index=j + 1
                    selectedIndex=0
                    for k in range(0, len(multiples)):
                        packMultiples=int(multiples[k]) * int(packSize)
                        if int(orderQty) >= int(packMultiples):
                            if (int(orderQty) - packMultiples) % int(packArr[index]) == 0:
                                selectedIndex = multiples[k]
                                possibleSizeArr.append(str(multiples[k]) + ":" + str(packSize))
                                if (k + 1) == len(multiples):
                                    if len(possibleSizeArr) > 0:
                                        result.append(possibleSizeArr[-1])
                                        orderQty=int(orderQty) - (int(packSize) * int(multiples[k]))
                                        break
                            else:
                                if index < len(packArr) - 1:
                                    index=index + 1
                                    if (int(orderQty) - packMultiples) % int(packArr[index]) == 0:
                                        selectedIndex=multiples[k]
                                        possibleSizeArr.append(str(multiples[k]) + ":" + str(packSize))
                                        if (k + 1) == len(multiples):
                                            if len(possibleSizeArr) > 0:
                                                result.append(possibleSizeArr[-1])
                                                orderQty=int(orderQty) - (int(packSize) * int(multiples[k]))
                                                break
                                continue
                        else:
                            if len(possibleSizeArr) > 0:
                                result.append(possibleSizeArr[-1])
                                orderQty=int(orderQty) - (int(packSize) * int(selectedIndex))
                            break
                    else:
                        break

            elif int(orderQty) < int(packSize):
                continue
            # print("No packs:::")
            else:
                print("Packs Unavailable.")
                break
    print("result:::::::::", result)
#    if len(result) == 0:
#        result.append("Invalid quantity. No packs available for given quantity.")
    return result


def printReceipt(code, qty, minPacks, ordered_price_dict):
    print("Inside printReceipt:::::")
    print("minPacks inside printReceipt::::", minPacks)
    total_price=0
    SPACE=" "
    CURRENCY="$"
    denomination=""
    if len(minPacks)>0:
        for entry in minPacks:
            print("entry:::", str(entry))
            s=str(entry).split(":")
            packKey=s[0]
            packValue=s[1]
            print("packValue:::", str(packValue))
            pack_price=ordered_price_dict[packValue]
            print(pack_price)
            total_price=total_price + int(packKey) * pack_price
            print(round(total_price, 2))
            denomination=denomination + "\t" + str(packKey) + SPACE + "X" + SPACE + str(
            packValue) + SPACE + CURRENCY + str(pack_price) + "\n"
        print("*************Receipt*************")
        print("--------------------------------------------")
        print(str(qty) + SPACE + code + SPACE + CURRENCY + str(round(total_price, 2)))
        print(denomination)
    else:
        print("*************Receipt*************")
        print("--------------------------------------------")
        print("Invalid quantity. No packs available for given quantity.")

if __name__ == "__main__":
    logging.basicConfig(filename='../../../logs/app.log', format='%(asctime)s - %(message)s', level=logging.INFO)
    readOrder()

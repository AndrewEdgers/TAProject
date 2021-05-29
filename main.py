import database


def main():
    print('----------------------------')
    print(
        'Show Depot[1], Show Log[2], Add New Item[3], Add Already Existing Item[4], Delete Item[5], Delete By Bar Code[6], Exit[7]')
    numValue: int = input('Choose action: ')
    if numValue == '1':
        database.showDepot()
        main()
    elif numValue == '2':
        database.showLog()
        main()
    elif numValue == '3':
        database.addItem()
        main()
    elif numValue == '4':
        database.addQuantity()
        main()
    elif numValue == '5':
        database.delQuantity()
        main()
    elif numValue == '6':
        database.delItem()
        main()
    elif numValue == '7':
        pass
    else:
        print('----------------------------')
        print('Couldn\'t resolve command. Please make sure it\'s integer and does not contain any brackets')
        main()


if __name__ == '__main__':
    main()
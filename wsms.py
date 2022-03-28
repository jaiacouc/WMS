# CSC 339-02 Spring 2021
# Program 1
# Name: John Iacoucci
import csv
import os
import atexit

# Welcome message and menu.
print('\nWelcome to wsms please use one of the following commands\n'
      '-wsms.load_stock(pass a csv file)\n'
      '-wsms.check_stock(item number)\n'
      '-wsms.add_stock(item number, quantity to add)\n'
      '-wsms.remove_stock(item_number, quantity to subtract)\n'
      '-wsms.pull_order(pass a csv file)\n'
      '-wsms.fill_order(pass the csv that was created)\n'
      '-wsms.restock_order(pass the csv that was created)\n'
      '-wsms.print_stock()\n')
# Inventory and pull list dictionaries along with the order number counter.
inventory = {}
pull_list = {}
order_counter = 1

def load_stock(filename):
    # Reads filename and adds contents to inventory.
    # Counter for bin number.
    global bin_counter
    global inventory
    # Catching incorrect file format.
    try:
        # open the file and close when finished.
        with open(filename) as f:
            # Cycle through the file and add the contents to the inventory.
            for line in csv.DictReader(f):
                # Creates a nested dictionary starting with the bin number.
                bin = {bin_counter: None}
                # Adds the contents of the file to a dictionary then adds that dictionary to the inventory.
                inventory.update(bin)
                inventory[bin_counter] = {line['item']: line['qty']}
                bin_counter += 1
        print('\nThe stock has been loaded')
    except KeyError:
        print('There is a error in the file stock has not been changed')
        inventory.pop(bin_counter)


def check_stock(item):
    # Returns the in stock quantity of an item.
    if exists(item):
        # Cycles through the inventory to check if the given value is in the inventory.
        for bin in inventory:
            # If the item in the inventory matches the given value then print the stock of that item.
            if str(item) in inventory[bin]:
                print('\nThe stock of widget ' + str(item) + ' is: ' + inventory[bin][str(item)])
                break
    else:
        print('\nThat item is not in the inventory')


def add_stock(item, qty):
    # Adds stock to a certain item by qty
    if exists(item):
        # Cycles through the inventory to see if the given value is in the inventory.
        for bin in inventory:
            # If it is then update the current value to the new value.
            if str(item) in inventory[bin]:
                # taking the current value and incrementing it by the given value.
                new_qty = int(inventory[bin][str(item)])
                new_qty += qty
                # Setting the new value to the item and updating the inventory.
                update_stock = {str(item): str(new_qty)}
                inventory[bin].update(update_stock)
                print('The stock for ' + str(item) + ' is now: ' + str(new_qty))
    else:
        print("\nThat item is not in the inventory")


def remove_stock(item, qty):
    # Decrements the stock of the item by qty
    if exists(item):
        # Cycles through the inventory to see if the given value is in the inventory.
        for bin in inventory:
            # If it is then update the current value to the new value.
            if str(item) in inventory[bin]:
                # taking the current value and incrementing it by the given value.
                new_qty = int(inventory[bin][str(item)])
                new_qty -= qty
                # Setting the new value to the item and updating the inventory.
                update_stock = {str(item): str(new_qty)}
                inventory[bin].update(update_stock)
                print('The stock for ' + str(item) + ' is now: ' + str(new_qty))
    else:
        print("\nThat item is not in the inventory")


def pull_order(filename):
    # Takes CSV of a order and creates a pull list.
    try:
        with open(str(filename)) as order:
            for line in csv.DictReader(order):
                update = {line['item']: line['qty']}
                pull_list.update(update)
    except KeyError:
        print('There is a error in the file has not been changed')
    # Organizes the pull list into bins and creates a csv for the pull list.
    order_conversion(binned_order())
    # Reserves the inventory for that order.
    decrement_inventory()
    # Clears the pull list for the next order.
    pull_list.clear()


def decrement_inventory():
    # Decrements the inventory.
    for bin, item in inventory.items():
        # Searching through the items in that bin
        for key in item:
            # If the item in inventory matches the item in the pull list
            # Take the corresponding bin and assign it to the bin for the ordered pull list
            if key in pull_list:
                new_qty = int(pull_list[key])
                qty = int(inventory[bin][key])
                if new_qty <= qty:
                    qty -= new_qty
                    update_qty = {str(key): str(qty)}
                    inventory[bin].update(update_qty)
                else:
                    print('\nThe order amount is greater than the inventory!')
                break
            else:
                continue
        continue


def binned_order():
    # Take the pull list and assigns it into the bins from the corresponding inventory
    ordered_pull_list = {}
    # Searching through bins in inventory
    for bin, item in inventory.items():
        # searching through the items in that bin
        for key in item:
            # If the item in inventory matches the item in the pull list
            # Take the corresponding bin and assign it to the bin for the ordered pull list
            if key in pull_list:
                # Creating the bin
                bin_num = {bin: None}
                # Adding the pull list item and qty
                ordered_pull_list.update(bin_num)
                ordered_pull_list[bin] = {key: pull_list[key]}
                break
            else:
                continue
        continue
    return ordered_pull_list


def order_conversion(dict):
    # Taking pull list and converting it into a csv file.
    # Creating the csv file.
    global order_counter
    # Name of the file.
    filename = 'pull_list_' + str(order_counter) + '.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Bin', 'Item', 'Qty']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Loop through the dictionary and write to the csv file.
        writer.writeheader()
        for bin, item in dict.items():
            # Writes the values for Bin, Item, Qty into the csv row by row
            for key in item:
                writer.writerow({'Bin': bin, 'Item': key, 'Qty': item[key]})
    # Prints the new file name what take the order counter allowing multiple pull orders to be active at once
    print('\n~Your pull list has been exported as: pull_list_' + str(order_counter) + '.csv.~')
    print('~Please use this filename for fill_order or restock_order.~')
    order_counter += 1


def fill_order(filename):
    # Deletes the specified pull list from the system
    os.remove(filename)
    print('\nThe order has been fulfilled')


def restock_order(filename):
    # Reads the given pull list to reverse the order.
    # Deletes the pull list from the system.
    order = {}
    # Opening the file and reading the data.
    with open(filename) as file:
        for line in csv.DictReader(file):
            data = {line['Item']: line['Qty']}
            order.update(data)
    # Looping through inventory.
    for bin, item in inventory.items():
        for key in item:
            # If the item is in the pull list then add it back to the inventory.
            if key in order:
                new_qty = int(order[key])
                qty = int(inventory[bin][key])
                qty += new_qty
                update_qty = {str(key): str(qty)}
                inventory[bin].update(update_qty)
    # Delete the file.
    os.remove(filename)
    # Confirmation
    print('\nThe order has been restocked')


def print_stock():
    # Prints the stock of each bin.
    # Uses the values of bin and item to determine the number of spaces needed.
    bin_number = 10
    item_number = 5
    # Print the category.
    print('\nBin' + '  ' + 'Item' + '    ' + 'Qty')
    # Loop through inventory
    for bin, item in inventory.items():
        for key in item:
            # If statements for spacing purposes.
            # If the bin is only one character and the item is only 4 characters use this spacing.
            if int(bin) < bin_number and len(key) < item_number:
                print(str(bin) + '    ' + str(key) + '    ' + str(item[key]))
            # If the bin is only one character but more than five characters use this spacing.
            elif int(bin) < bin_number:
                print(str(bin) + '    ' + str(key) + '   ' + str(item[key]))
            # If the item is only 4 characters use this spacing.
            elif len(key) < item_number:
                print(str(bin) + '   ' + str(key) + '    ' + str(item[key]))
            # Any other lengths use this spacing.
            else:
                print(str(bin) + '   ' + str(key) + '   ' + str(item[key]))


def exists(item):
    # Checks if a item is in the inventory and returns true for yes, false for no.
    for bin, items in inventory.items():
        for key in items:
            if str(item) == key:
                return True


def storage():
    # Stores the inventory if the program is exited.
    with open('inventory.csv', 'w', newline='') as csvfile:
        fieldnames = ['Bin','Item', 'Qty']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Writes inventory to a file to be stored.
        for bin, item in inventory.items():
            for key in item:
                writer.writerow({'Bin': bin, 'Item': key, 'Qty': item[key]})


def check_storage():
    # Checks to see if there is a inventory file stored.
    # If there is a file then write it to the Inventory and update the counter to the current bin.
    try:
        with open("inventory.csv") as f:
            for line in csv.DictReader(f):
                bin = {line['Bin']:None}
                inventory.update(bin)
                inventory[line['Bin']] = {line['Item']: line['Qty']}
                counter = int(line['Bin'])
        return counter
    # If there is no file then set the bin to 1.
    except FileNotFoundError:
        counter = 1
        return counter


# Checking for a inventory storage file from the last session and setting the bin accordingly.
bin_counter = check_storage()
# Exit statement
atexit.register(storage)

import datetime
import csv

class ShoppingList:
    def __init__(self, shopping_list, date=datetime.date.today()):
        self.shopping_list = shopping_list.split(', ')
        self.date = date
        self.products = []
        self.cnt = []
        for i in self.shopping_list:
            self.products.append(i.split(' ')[0])
            self.cnt.append(int(i.split(' ')[1]))
        print(self.products)
        print(self.cnt)

    def values_processing(self, val):
        new_values = val.split(', ')
        product_processing = []
        cnt_processing = []
        for i in new_values:
            product_processing.append(i.split(' ')[0])
            cnt_processing.append(int(i.split(' ')[1]))
        return product_processing, cnt_processing

    def add_value(self, val):
        products_add, cnt_add = self.values_processing(val)
        message = ''
        for idx, product in enumerate(products_add):
            if product in self.products:
                product_index = self.products.index(product)
                self.cnt[product_index] += cnt_add[idx]
                message += f'Для продукту {product} кількість збільшена на {cnt_add[idx]}\n'
            else:
                self.products.append(product)
                self.cnt.append(cnt_add[idx])
                message += f'Продукт {product} з кількістю {cnt_add[idx]} додано до Вашого списку\n'
        print(self.products)
        print(self.cnt)
        return message

    def del_value(self, val):
        product_del, cnt_del = self.values_processing(val)
        message = ''
        print(self.products, self.cnt)
        for idx, product in enumerate(product_del):
            if product in self.products:
                product_index = self.products.index(product)
                self.cnt[product_index] -= cnt_del[idx]
                if self.cnt[product_index] <= 0:
                    message += f'Продукт {product} видалено зі списку\n'
                    del self.products[product_index]
                    del self.cnt[product_index]
                elif self.cnt[product_index] > 0:
                    message += f'Кількість продукту {product} зменшена на {cnt_del[idx]}\n'
            else:
                message += f'Продукту {product} немає у списку\n'
            print(self.products, self.cnt)
        return message

    def save_to_csv(self):
        with open('shopping_data.csv', mode='a+', newline='') as file:
            writer = csv.writer(file)

            # Чтение существующих данных
            existing_data = []
            existing_reader = csv.reader(file)
            for row in existing_reader:
                existing_data.append(row)
            for product, count in zip(self.products, self.cnt):
                data_found = False
                for i, row in enumerate(existing_data):
                    date, existing_product, existing_count = row
                    if date == self.date and existing_product == product:
                        if int(existing_count) == count:
                            data_found = True
                            break
                        elif int(existing_count) != count:
                            existing_data[i] = [date, existing_product, count]
                            data_found = True
                            break
                if not data_found:
                    existing_data.append([self.date, product, count])
            file.seek(0)
            file.truncate()
            if len(existing_data) == 0:
                writer.writerow(['date', 'product', 'cnt'])
            writer.writerows(existing_data)

    def read_from_csv(self, date):
        date_for_read = datetime.datetime.strftime(date, '%Y-%m-%d')
        data = []
        message = f'Ось ваш список на дату {date_for_read}'
        with open('shopping_data.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                date_from_file, product, count = row
                if date_from_file == date_for_read:
                    data.append((date, product, count))
                else:
                    return f'На дату {date_for_read} немає списку'
            for i in data:
                message += f'\n {i[1]}, {i[2]}'
        return message

a = ShoppingList('banana 3, apple 1, cherry 2',)
print(a.add_value('kivi 4, pineapple 5, apple 3'))
print(a.del_value('cherry 1, orange 2, banana 3'))
a.save_to_csv()
b = a.read_from_csv(datetime.datetime.today().date())
print(b)

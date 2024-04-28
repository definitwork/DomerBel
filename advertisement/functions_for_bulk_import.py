import openpyxl
from advertisement.models import Advertisement, Category, Region, Field, Spisok, ElementTwo

def check_article(ads):
    '''Функция, проверяющаяя артикул в объявлениях'''
    if 'aртикул' in ads:
        article = ads.get('aртикул')
        if article == None:
            return True
        elif article != None and len(str(article)) < 256:
            return True
        elif article != None and len(str(article)) > 255:
            return 'Количество символов в артикле не должно быть больше 255.'
    else:
        return True
    

def chek_title(ads):
    '''Функция, проверяющая заголовок объявления'''
    if 'заголовок' in ads and len(str(ads.get("заголовок"))) < 256:
        return True
    else:
        return 'поле "Заголовк" обязательное'
    

def chek_price(ads):
    '''Функция, проверящя цену'''
    if 'цена' in ads and ads.get('цена') != None:
        price = str(ads.get('цена'))
        if price.find('.') != -1:
            list_price = price.split('.')
            if len(list_price) == 2 and len(list_price[0])+len(list_price[1]) <=12 and len(list_price[1]) <= 2 and list_price[0].isdigit() and list_price[1].isdigit():
                return True
            else:
                return 'некорретно указана цена'
        else:
            if price.isdigit() and len(price) <= 12:
                return True
            else:
                return 'некорретно указана цена'
    elif ads.get('цена') == None:
        return True
    else:
        return True
    

def chek_category(ads):
    '''Функция, проверяющая категорию объявления'''
    if 'категория' in ads:
        category = ads.get('категория')
        if Category.objects.filter(title__iexact = f'{category}'):
            return True
        else:
            return 'некорректно заполнено поле "Категория"'
    else:
        return 'поле "Категория" обязательное'
    
    
def check_region(ads):
    '''Функция, проверяющаа регион'''
    if 'регион' in ads:
        region = ads.get('регион')
        if Region.objects.filter(area__iexact=f'{region}'):
            return True
        else:
            return 'некорректно заполнено поле "Регион"'
    else:
        return 'поле "Регион" обязательное'

def check_additional_information(ads):
    '''Функция проверяет поля для детальной информации и возвращает JsonFile'''
    j = {}
    error = []
    print(ads)
    if 'категория' in ads:
        category_from_ads = ads.get('категория')
        category = Category.objects.prefetch_related('field_set').get(title=f'{category_from_ads }')
        '''Все поля'''
        fields = category.field_set.all()
        print(1)
        for field_from_excel in ads.keys():
            value = ads.get(field_from_excel)
            field_from_db = fields.filter(title__iexact = field_from_excel)
            print(2)
            if len(field_from_db) != 0:
                print(3)
                for field in field_from_db:
                    if field.error != '':
                        print(4)
                        '''обязательные поля для заполнения'''
                        if field.spisok_id != None:
                            print(5)
                            '''обязательные поля с варинтами для заполнения'''
                            spisok = Spisok.objects.prefetch_related('element_set').get(id=field.spisok_id)
                            elements_from_db = spisok.element_set.all()
                            elements_for_compare = elements_from_db.filter(title__iexact = ads.get(field_from_excel))
                            if len(elements_for_compare) != 0:
                                print(6)
                                '''если значение поля состоит из одной части'''
                                for element in elements_for_compare:
                                    j[field.title] = element.title
                            else:
                                print(7)
                                '''если значение поля стостоит из двух частей или некорректно введено'''
                                elementstwo_for_compate = {}
                                for element in elements_from_db:
                                    elementstwo_from_db = ElementTwo.objects.filter(element_id=element.id)
                                    for element_two in elementstwo_from_db:
                                        elementstwo_for_compate[element.title.lower() + ' ' + element_two.title.lower()] = [element.id,element_two.id]
                                if elementstwo_for_compate.get(str(value).lower()) != None:
                                    element_id = elementstwo_for_compate.get(str(value).lower())
                                    print(8)
                                    ''' ТУТ КОСЯК!!!!!!'''
                                    '''если значение поля состоит из двух частей'''
                                    element_part_one = elements_from_db.filter(id = element_id[0])
                                    element_part_two = elementstwo_from_db.filter(id = element_id[1])
                                    print(element_part_one)
                                    print(element_part_two)
                                    # j[field.title] = element_part_one.title + ' ' + element_part_two.title
                                else:
                                    print(9)
                                    error.append(f'Некорректное значения поля {field_from_excel}')
                        else:
                            print(10)
                            ''' обязательные поля без вариантов для заполнения'''
                            j[field.title] = value
                    else:
                        print(11)
                        '''необязательные полян для заполнения'''
                        j[field.title] = value
            else:
                print('Не все поля относятся к дополнительным . Пределай!', 12)
                error.append(f'Некорректное имя поля {field_from_excel}')
    if len(error) != 0 :
        print('Есть ошибки')
        return error
    else:
        print('Переписать словать в json!!!!')
        print(j)

            
            # for field in fields:
                # if field.error != '':
                #     '''обязательные поля'''

                #     if field_from_excel.lower().replace(' ','') == field.title.lower().replace(' ',''):
                #         if field.spisok_id != None:
                #             '''Список элементов для дополнительного поля'''
                #             spisok = Spisok.objects.prefetch_related('element_set').get(id=field.spisok_id)
                #             '''Значение элементов для дополнительного поля'''
                #             elements = spisok.element_set.all()
                #             str_for_compare = []
                #             for element in elements:
                #                 elementstwo = ElementTwo.objects.filter(element_id=element.id)
                #                 if len(elementstwo) != 0:                                
                #                     for element_two in elementstwo:
                #                         str_for_compare.append(element.title.lower().replace(' ','') + element_two.title.lower().replace(' ',''))
                #                 else:
                #                     str_for_compare.append(element.title)
                #             if ads.get(field_from_excel).lower().replace(' ','') in str_for_compare:
                #                 print('Дзинь-дзинь!', ads.get(field_from_excel))
                #             else:
                #                 print('некорретроное значение поля', ads.get(field_from_excel))
                #         else:
                #             pass
                #     else:
                #         pass
                # else:
                #     '''необязательные поля'''

def save_many_ads_from_excel(uploud_file, user):
    '''Функция сохраняющаяя обявления из экселя'''
    book = openpyxl.open(uploud_file, read_only=True)
    sheet = book.active
    row_in_excel = 2

    list_ads_save = []
    list_ads_error = []
    while row_in_excel <= sheet._max_row:
        ads = {}
        for i in range(0, sheet.max_column):
            if sheet[row_in_excel][i].value != None:
                ads[f'{sheet[1][i].value.lower()}'] = sheet[row_in_excel][i].value
        ''' Проверяются обявления из файла '''
        if len(ads) != 0:
            status_ads = []
            if check_article(ads) != True:
                status_ads.append(check_article(ads))
            if chek_title(ads) != True:
                status_ads.append(chek_title(ads))
            if chek_price(ads) != True:
                status_ads.append(chek_price(ads))
            if chek_category(ads) != True:
                status_ads.append(chek_category(ads))
            check_additional_information(ads)
        #     if check_additional_information(ads) != True:
        #         print('я тут!!!!')
        row_in_excel = row_in_excel + 1
    return True
        
        
        
        

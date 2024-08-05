from celery import shared_task
from advertisement.functions_for_bulk_import import delete_everything_in_folder, save_many_ads_from_excel, \
    save_many_ads_from_zip
from advertisement.models import ErrorFile


@shared_task()
def delete_everything_in_folder_beat():
    '''Таска удаляющая все файлы из папки для "files_for_bulk_import_of_ads"
    Таска отрабатывает раз в сутки в 00.00'''
    delete_everything_in_folder()

@shared_task()
def save_many_ads_from_excel_task(uploud_file,id,first_name,phone_number,email):
    '''Таска сохраняющая объявления из экселя'''
    result = save_many_ads_from_excel(uploud_file,id,first_name,phone_number,email)
    return result

@shared_task()
def save_many_ads_from_zip_task(uploud_zip, id,first_name,phone_number,email):
    '''Таска сохраняющая объявления из zip-архива'''
    result = save_many_ads_from_zip(uploud_zip, id,first_name,phone_number,email)
    return result

@shared_task()
def delete_error_file_beat():
    '''Таска удаляющая все экземпляры модели ErrorFile разы в сутки '''
    files = ErrorFile.objects.all()
    files.delete()



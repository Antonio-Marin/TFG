# import os
# import json
# from datetime import datetime
# import locale

# # Establecer la localización a español
# locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# # Directorio que contiene los archivos JSON
# json_directory = 'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El diario\V1'

# # Diccionario para almacenar las noticias agrupadas por mes y año
# grouped_news = {}

# # Recorrer todos los archivos JSON en el directorio
# for filename in os.listdir(json_directory):
#     if filename.endswith('.json'):
#         with open(os.path.join(json_directory, filename), 'r', encoding='utf-8') as file:
#             news_data = json.load(file)
#             # Procesar cada noticia del archivo JSON
#             for news in news_data:
#                 # Extraer la fecha de la noticia
#                 date_str = news['Fecha']
#                 date_obj = datetime.strptime(date_str, "%d de %B de %Y - %H:%M h")
#                 year_month = date_obj.strftime("%Y-%m")
#                 # Agrupar la noticia por mes y año
#                 if year_month not in grouped_news:
#                     grouped_news[year_month] = []
#                 grouped_news[year_month].append(news)

# # Guardar las noticias agrupadas en archivos separados
# for year_month, news_list in grouped_news.items():
#     output_filename = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El diario\order\datos_{year_month}.json'
#     with open(output_filename, 'w', encoding='utf-8') as output_file:
#         json.dump(news_list, output_file, ensure_ascii=False, indent=4)
#         print(f"Noticias guardadas en {output_filename}")


## COMPROBACIÓN DE CANTIDAD DE NOTICIAS
# import os
# import json

# def count_news_in_directory(directory):
#     total_news = 0
#     for filename in os.listdir(directory):
#         if filename.endswith('.json'):
#             with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
#                 news_data = json.load(file)
#                 total_news += len(news_data)
#     return total_news

# # Directorios que deseas comparar
# directories_to_compare = [
#     'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El diario\V1',
#     'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El diario\order'
# ]

# # Contar las noticias en cada directorio
# news_counts = {}
# for directory in directories_to_compare:
#     news_counts[directory] = count_news_in_directory(directory)

# # Imprimir los recuentos de noticias
# for directory, count in news_counts.items():
#     print(f"Total de noticias en {directory}: {count}")

# # Verificar si la cantidad de noticias es la misma en todos los directorios
# if len(set(news_counts.values())) == 1:
#     print("La cantidad de noticias es la misma en todos los directorios.")
# else:
#     print("La cantidad de noticias difiere entre los directorios.")

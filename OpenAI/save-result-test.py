# OBSOLETO

# import json
# import re

# newscasts = ["ElMundo", "ElPais", "ElDiario", "LibertadDigital"]
# outputAI = "**Fecha de redacción:** 1 de mayo de 2020.\n\n**Sujeto activo de la información:** Delegación del Gobierno, Comunidad de Madrid, portavoces de la oposición de izquierda, Vox, Podemos Comunidad de Madrid.\n\n**Tema principal:** Investigación abierta por vulneración del distanciamiento social en un acto en Ifema, Madrid.\n\n**Tono de la noticia:** Crítico y objetivo, basado en declaraciones de portavoces de la oposición y partidos políticos.\n\n**Resumen:** La Delegación del Gobierno ha abierto una investigación debido a la presunta falta de respeto de medidas de distanciamiento social en un acto en Ifema, Madrid, organizado por la Comunidad de Madrid. Diversos portavoces de la oposición y partidos políticos han denunciado la falta de separación entre los asistentes, incluyendo abrazos y apretones de manos, lo que consideran una acción irresponsable que pone en riesgo la propagación del coronavirus.\n\n**Palabras clave:** Investigación, distanciamiento social, Ifema.\n"
# regex = r"\*\*(.+?)\*\* (.*?)(?=\*\*|$)"

# output_list = []
# fields = re.findall(regex, outputAI, re.DOTALL)

# output_dict = {field[0]: field[1] for field in fields}
# output_list.append(output_dict)
# print(output_list)
# print("----------------------------------")
# outputAI2 = "**Fecha de redacción:** AAAAAAAAAAAAAAA.\n\n**Sujeto activo de la información:** BBBBBBBBBBBBBBBBBBBBBBBBBBB.\n\n**Tema principal:** CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC.\n\n**Tono de la noticia:** DDDDDDDDDDDDDDDDDDDDDDDDDd.\n\n**Resumen:** EEEEEEEEEEEEEEEEEEEEEEEEEEEE.\n\n**Palabras clave:** FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf.\n"
# fields = re.findall(regex, outputAI2, re.DOTALL)

# output_dict = {field[0]: field[1] for field in fields}
# output_list.append(output_dict)
# print(output_list)
# pathJson = f'D:\Carrera\TFG\Pruebas de código\Pruebas OpenAI\SaveTest.json'
# with open(pathJson, 'w', encoding='utf-8') as jsonFile:
#     json.dump(output_list, jsonFile, ensure_ascii=False, indent=4)

# """
# for newscast in newscasts:

#         pathJson = f'PRO-Noticias_{0000}-{00}.json'
#         with open(pathJson, 'w', encoding='utf-8') as jsonFile:
#             json.dump(json_data, jsonFile, ensure_ascii=False, indent=4)
# """


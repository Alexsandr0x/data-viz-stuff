from semeando_educacao.questionarios import PLANILHAS
import pandas as pd

parsed_data = {
    0: [],
    1: [],
    2: []
}

older_columns = ['idade', 'serie', 'cursar_pre',
                                  'cursar_pos', 'pais_superior',
                                  'qual_pais_superior',
                                  'con_ingresso_pre', 'con_ingresso_pos',
                                  'con_aux_pre',
                                  'con_aux_pos']

old_columns = ['idade', 'genero', 'serie', 'cursar_pre',
                                  'cursar_pos', 'pais_superior',
                                  'qual_pais_superior',
                                  'con_ingresso_pre', 'con_ingresso_pos',
                                  'con_aux_pre',
                                  'con_aux_pos']

new_columns = ['idade', 'genero', 'serie', 'cursar_pre',
                'cursar_pos', 'familiar_superior',
                'qual_familiar_superior', 'outro_familiar_superior',
                'palestra_ingresso', 'palestra_aux', 'con_ingresso', 'con_aux']

columns_by_type = {
    0: older_columns,
    1: old_columns,
    2: new_columns
}


def get_questionario_datas():
    for file_name, tipo, escola, cidade in PLANILHAS:
        file = pd.ExcelFile('questionarios/{}'.format(file_name))

        sheet_name = file.sheet_names[0]
        data_file = file.parse(sheet_name)

        table = data_file.values[2:]
        if table.shape[0] > 10 and tipo == 0:
            table = table[:, :10]

        if table.shape[1] > 11 and tipo == 1:
            table = table[:, :11]

        if table.shape[1] > 12 and tipo == 2:
            table = table[:, :12]

        columns = columns_by_type[tipo]
        sheet = pd.DataFrame(table, columns=columns)

        parsed_data[tipo].append(
            {
                'name': escola,
                'city': cidade,
                'data': sheet,
                'version': tipo
            }
        )

    return parsed_data


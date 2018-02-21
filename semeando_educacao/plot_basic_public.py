from collections import OrderedDict

import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from semeando_educacao import get_questionario_datas

"""
Esse modulo tem como objetivo gerar uma serie de graficos usando as informações
mais basicas das planilhas do Projeto Semeando Educação referente ao ano de
2017.
"""

dataset = get_questionario_datas()

age_list = []
gender = OrderedDict({
    'M': 0,
    'F': 0
})
serie = {
    '1': 0,
    '2': 0,
    '3': 0,
    'terminado': 0
}
mudanca_de_opniao = {
    'nn': 0,
    'ny': 0
}

nota_ingresso = {
    'pre': [],
    'pos': []
}

nota_auxilio = {
    'pre': [],
    'pos': []
}

conceito_ingresso = {}

conceito_auxilio = {}

for school in dataset[0] + dataset[1] + dataset[2]:
    sheet = school['data']
    sheet = sheet[sheet.idade.apply(lambda x: isinstance(x, int))]

    # age:
    age_list.extend(
        sheet.idade.values
    )
    if 'genero' in sheet.columns:
        for key_, value_ in dict(sheet.genero.value_counts()).items():
            if key_.upper() in gender:
                gender[key_.upper()] += value_

    if 'serie' in sheet.columns:
        for key_, value_ in dict(sheet.serie.value_counts()).items():
            if str(key_) in serie:
                serie[str(key_)] += value_
            else:
                serie['terminado'] += value_

    if 'cursar_pre' in sheet.columns:
        cursar_pre_pos = zip(
            list(sheet.cursar_pre),
            list(sheet.cursar_pos)
        )
        for pre_r, pos_r in cursar_pre_pos:
            if pre_r == pos_r == 'NÃO':
                mudanca_de_opniao['nn'] += 1

            elif pre_r == 'NÃO' and pos_r == 'SIM':
                mudanca_de_opniao['ny'] += 1

    if 'con_ingresso_pre' in sheet.columns:
        nota_ingresso['pre'] += list(sheet.con_ingresso_pre.values)
        nota_ingresso['pos'] += list(sheet.con_ingresso_pos.values)

    if 'con_aux_pre' in sheet.columns:
        nota_auxilio['pre'] += list(sheet.con_aux_pre.values)
        nota_auxilio['pos'] += list(sheet.con_aux_pos.values)

    if 'palestra_ingresso' in sheet.columns:
        for k, v in dict(sheet.palestra_ingresso.value_counts()).items():
            if k not in conceito_ingresso:
                conceito_ingresso[k] = 0
            conceito_ingresso[k] += v

    if 'palestra_aux' in sheet.columns:
        for k, v in dict(sheet.palestra_aux.value_counts()).items():
            if k not in conceito_auxilio:
                conceito_auxilio[k] = 0
            conceito_auxilio[k] += v

plt.clf()
mpl.rcParams.update(mpl.rcParamsDefault)
plt.title('Idade dos Alunos')
plt.xlabel('Idade')
plt.hist(age_list, 10)
plt.tight_layout()
plt.savefig('idade.png', bbox_inches="tight")
plt.show()

plt.clf()
mpl.rcParams.update(mpl.rcParamsDefault)
plt.title('Sexo dos Alunos')
labels = ['Homem', 'Mulher']
values = [gender['M'], gender['F']]
plt.pie(values, labels=labels)
plt.tight_layout()
plt.savefig('sexo.png', bbox_inches="tight")
plt.show()

plt.clf()
mpl.rcParams.update(mpl.rcParamsDefault)
plt.title('Serie que os alunos cursavam')
labels = ['1° ano', '2° ano', '3° ano', 'terminado']
values = [serie['1'], serie['2'], serie['3'], serie['terminado']]
plt.pie(values, labels=labels)
plt.tight_layout()
plt.savefig('serie.png', bbox_inches="tight")
plt.show()

plt.clf()
mpl.rcParams.update(mpl.rcParamsDefault)
plt.title('Opinião sobre cursar ensino superior')
labels = ['Não e Não \n(sem mudança)', 'Não e Sim \n(mudança positiva)']
values = [mudanca_de_opniao['nn'], mudanca_de_opniao['ny']]
plt.pie(values, labels=labels)
plt.tight_layout()
plt.savefig('mudanca1.png', bbox_inches="tight")
plt.show()

plt.clf()
mpl.rcParams.update(mpl.rcParamsDefault)
plt.title('Auto Avaliação quanto a conhecimento ao ingresso a faculdade')
x = [i for i in nota_ingresso['pre'] if isinstance(i, int)]
y = [i for i in nota_ingresso['pos'] if isinstance(i, int)]
plt.hist(x, alpha=0.5, label='antes da palestra')
plt.hist(y, alpha=0.5, label='após a palestra')
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('ingresso.png', bbox_inches="tight")
plt.show()

plt.clf()
mpl.rcParams.update(mpl.rcParamsDefault)
plt.title('Auto Avaliação quanto a conhecimento ao auxilio na faculdade')
x = [i for i in nota_auxilio['pre'] if isinstance(i, int)]
y = [i for i in nota_auxilio['pos'] if isinstance(i, int)]
plt.hist(x, alpha=0.5, label='antes da palestra')
plt.hist(y, alpha=0.5, label='após a palestra')
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('auxilio.png', bbox_inches="tight")
plt.show()

plt.clf()
mpl.rcParams.update(mpl.rcParamsDefault)
plt.title('Conceito dado pelos alunos quanto a informações '
          '\nsobre ingresso a universidade')
labels = ['BOM', 'REGULAR', 'RUIM', 'INDIFERENTE']
values = [conceito_ingresso[k] for k in labels]
y_pos = np.arange(len(labels))
plt.bar(y_pos, values, align='center', alpha=0.5)
plt.xticks(y_pos, labels)
plt.tight_layout()
plt.savefig('conceito_ingresso.png', bbox_inches="tight")
plt.show()

plt.clf()
mpl.rcParams.update(mpl.rcParamsDefault)
plt.title('Conceito dado pelos alunos quanto a informações '
          '\nsobre auxilios a universidade')
labels = ['BOM', 'REGULAR', 'RUIM', 'INDIFERENTE']
values = [conceito_auxilio[k] for k in labels]
y_pos = np.arange(len(labels))
plt.bar(y_pos, values, align='center', alpha=0.5)
plt.xticks(y_pos, labels)
plt.tight_layout()
plt.savefig('conceito_auxilio.png', bbox_inches="tight")
plt.show()

plt.clf()
mpl.rcParams.update(mpl.rcParamsDefault)
plt.title('Variação de auto avaliação')
x = [i for i in nota_ingresso['pre'] if isinstance(i, int)]
y = [i for i in nota_ingresso['pos'] if isinstance(i, int)]
xy = [y_id - x_id for x_id, y_id in zip(x, y)]
plt.hist(xy, bins=np.arange(-9, 10)-0.5, edgecolor='black', linewidth=1.2)
plt.xticks(range(-10, 10))

plt.tight_layout()
plt.savefig('var_nota_ingresso.png', bbox_inches="tight")
plt.show()
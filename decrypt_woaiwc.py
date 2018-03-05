# encoding: utf-8
"""
File:       decrypt_woaiwc
Author:     twotrees.zf@gmail.com
Date:       2018/2/22 21:24
Desc:
"""

import os
import sys
from os import path
import re
import subprocess


PASSWORDS = {
    'T338801': 'yea951',
    'T338802': 'geru94',
    'T338803': 'h21ear',
    'T338804': '521hhb',
    'T338805': '1187gr',
    'T338806': '987fib',
    'T338807': 'min843',
    'T338808': 'hrr51r',
    'T338809': '32htqa',
    'T338810': '41htat',
    'T338811': '456hgt',
    'T338812': 'yk48w4',
    'T338813': 'jhu157',
    'T338814': 'hhte8q',
    'T338815': 'knyy41',
    'T338816': 'hnyt81',
    'T338817': 'hnytu9',
    'T338818': '66hjqd',
    'T338819': '5jtw3j',
    'T338820': 'gh23ja',
    'T338821': 'khgq18',
    'T338822': '15qh43',
    'T338823': 'hrqw53',
    'T338824': 'hya569',
    'T338825': 'asdh88',
    'T338826': 'aahr26',
    'T338827': '858rhx',
    'T338828': '335hrqdqe257',
    'T338829': 'fht56y5gerqd',
    'T338830': 'qqhyk59gryj4',
    'T338831': 'dhykj5615eah',
    'T338832': '92hrtach63dh',
    'T338833': 'haer53564dhr',
    'T338834': 'adhytuj2242a',
    'T338835': 'dhyfdh3654bf',
    'T338836': 'asdhnt85356a',
    'T338837': 'dhpjtmghe524',
    'T338838': '5547482asdhg',
    'T338839': 'sdr874965dhr',
    'T338840': 'asdhtj235742',
    'T338841': 'dsg8657htjyx',
    'T338842': 'xht985237rae',
    'T338843': 'dhy63574asdh',
    'T338844': 'asdh8753htwa',
    'T338845': 'jkyef82nt4w6',
    'T338846': '5445je42',
    'T338847': '332145fj',
    'T338848': '7892nt22',
    'T338849': 'c6445dw3',
    'T338850': 'f5955546',
    'T338851': 'e3295442',
    'T338852': '32fs3258',
    'T338853': '336984fe',
    'T338854': '36dw9752',
    'T338855': '37954hte',
    'T338856': 'a6524923',
    'T338857': 'de569874',
    'T338858': '698dgrhw',
    'T338859': 'd6547823',
    'T338860': 'sde96874',
    'T338861': 'ja523698',
    'T338862': 'wdg98754',
    'T338863': 'ehs66879',
    'T338864': '68725aea',
    'T338865': '9687gewa',
    'T338866': '963ge789',
    'T338867': '753dge24',
    'T338868': '954gea34',
    'T338869': 'dge85235',
    'T338870': 'pdw35794',
    'T338871': 'xxw99526',
    'T338872': 'hgre9999',
    'T338873': 'xe8822ww',
    'T338874': 'hte57982',
    'T338875': 'kk5533ee',
    'T338876': 'hrww8888',
    'T338877': '88awefff',
    'T338878': '863wrw88',
    'T338879': '99235gew',
    'T338880': 'sdgqq555',
    'T338881': 'wwyhdt2gstqq',
    'T338882': 'jjdhytegdfx28',
    'T338883': 'kldeurycv7652',
    'T338884': 'kajhdgtwx92',
    'T338885': 'pbhjdgegjdj',
    'T338886': 'jdgeu6488wqa',
    'T338887': 'kjyeqx55687a',
    'T338888': 'dgeqw994547d',
    'T338889': 'dgeqaadg6648',
    'T338890': 'adgrrtw88adge',
    'T338891': 'feage687aerqd',
    'T338892': 'pqqdgeqwe5524',
    'T338893': 'ehqei68394dge',
    'T338894': '625adeq55eefx',
    'T338895': 'xx6642qdgeqmx',
    'T338896': 'teixq56362qxf',
    'T338897': '623qdgfqxsge5',
    'T338898': 'dgrrhujid2254',
    'T338899': 'djuimimq36548',
    'T338100': 'utygjqjxytg55',
    'T338101': 'iibe654ewc',
    'T338102': '8524qgjk89',
    'T338103': '56748dgedf',
    'T338104': 'meae998825',
    'T338105': '789465dfeq',
    'T338106': 'mpaq658723',
    'T338107': 'hdf357gqds',
    'T338108': 'erwfg37895',
    'T338109': '59897dfgqd',
    'T338110': '5657dfsgpq',
    'T338111': '23546rgewd',
    'T338112': '98dfg897ew',
    'T338113': 'trhdsf6578',
    'T338114': 'wertfg9878',
    'T338115': 'threrw9875',
    'T338116': 'trwqe98765',
    'T338117': '657werfd87',
    'T338118': 'rtwedshg89',
    'T338119': 'ytree89745',
    'T338120': 'jhkje54678',
    'T338121': 'dg65469getsd',
    'T338122': 'fhdjge66899xz',
    'T338123': '6465hrewqwq89',
    'T338124': '568verhg6wewx',
    'T338125': '568787dgewqwe',
    'T338126': 'd5dg4e5wqwe5d',
    'T338127': 'minewqer987xx',
    'T338128': '88987dgrgjhkx',
    'T338129': '89eyrqwdfga98',
    'T338130': '22787eefdhtqx',
    'T338131': '66u57uerw95fe',
    'T338132': 'er5g5wersddgr',
    'T338133': 'dge45qwer77hr',
    'T338134': '77erh7qweqexr',
    'T338135': '4d54geqwe68rx',
}


def batchProcess(folder):
    for (dir, dirNames, fileNames) in os.walk(folder):
        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            if extName.lower() == '.rar':
                dirName = path.basename(dir)
                matchName = re.findall(r'T\d+', dirName)
                if len(matchName):
                    matchName = matchName[0]
                    password = PASSWORDS[matchName]
                    if len(password):
                        command = 'unar -o {folder} -p {password} {file}'
                        filePath = path.join(dir, fileName)
                        exeCommand = command.format(folder='\'' + dir + '\'', password=password, file='\'' + filePath + '\'')
                        print(exeCommand)
                        ret = subprocess.call(shell=True, args=exeCommand)
                        if ret == 0:
                            print('extract successfull:{file}'.format(file=filePath))
                            os.remove(filePath)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        batchProcess(folder)
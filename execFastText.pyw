# =============================================================================================
#    execFastText : Spawned subprocess from winFastText to execute fasttext command via API.
# =============================================================================================
#   Author:
#     Kiyoshi Hirose, Representative of HIT Business Consulting Firm.
#   Abstract:
#      This program executes every fasttext command and returns results via STDERR.
#      winFastText spawns this process and communicates through subprocess.PIPE method.
#      ft.ini is an input information from winFastText what to do in this program.
#   Github:
#      https://
#   License: MIT License.
#      Find License.txt for more detail.
#   Version history:
#      0.0.1 : 2019-11-xx
# ---
import fasttext as ft
import configparser
import multiprocessing
import sys
import wmi


pcLang = wmi.WMI().Win32_OperatingSystem()[0].OSLanguage  # make sure the language of your Windows PC
winJP = True if pcLang == 1041 else False  # 1041 is the Japanese language code of Windows

config = configparser.ConfigParser()
ft_ini = 'ft.ini'
config.read(ft_ini, encoding='utf-8')
ft_command = config.get('general', 'ft_command')
ft_currentDir = config.get('general', 'ft_currentDir')
section = ft_command

# =============================================
#    $ fasttext supervised/skipgram/cbow ...
# =============================================
if ft_command == 'super' or ft_command == 'skip' or ft_command == 'cbow':
    Ent_input = config.get(section, 'Ent_input').encode('sjis') if winJP else config.get(section, 'Ent_input')
    Ent_output = config.get(section, 'Ent_output')
    if config.get(section, 'Ent_lr') == '':
        Ent_lr = 0.1 if ft_command == 'super' else 0.05
    else:
        Ent_lr = float(config.get(section, 'Ent_lr'))
    Ent_dim = int(config.get(section, 'Ent_dim')) if config.get(section, 'Ent_dim') != '' else 100
    Ent_ws = int(config.get(section, 'Ent_ws')) if config.get(section, 'Ent_ws') != '' else 5
    Ent_epoch = int(config.get(section, 'Ent_epoch')) if config.get(section, 'Ent_epoch') != '' else 5
    if config.get(section, 'Ent_minCount') == '':
        Ent_minCount = 1 if ft_command == 'super' else 5
    else:
        Ent_minCount = int(config.get(section, 'Ent_minCount'))
    if config.get(section, 'Ent_minn') == '':
        Ent_minn = 0 if ft_command == 'super' else 3
    else:
        Ent_minn = int(config.get(section, 'Ent_minn'))
    if config.get(section, 'Ent_maxn') == '':
        Ent_maxn = 0 if ft_command == 'super' else 6
    else:
        Ent_maxn = int(config.get(section, 'Ent_maxn'))
    Ent_neg = int(config.get(section, 'Ent_neg')) if config.get(section, 'Ent_neg') != '' else 5
    Ent_wordNgrams = int(config.get(section, 'Ent_wordNgrams')) if config.get(section, 'Ent_wordNgrams') != '' else 1
    Ent_loss = config.get(section, 'Ent_loss')
    Ent_bucket = int(config.get(section, 'Ent_bucket')) if config.get(section, 'Ent_bucket') != '' else 2000000
    if config.get(section, 'Ent_thread') == '':
        Ent_thread = 12 if ft_command == 'super' else multiprocessing.cpu_count()
    else:
        Ent_thread = int(config.get(section, 'Ent_thread'))
    Ent_lrUpdateRate = int(config.get(section, 'Ent_lrUpdateRate')) if config.get(section, 'Ent_lrUpdateRate') != '' else 100
    Ent_t = float(config.get(section, 'Ent_t')) if config.get(section, 'Ent_t') != '' else 0.0001
    Ent_verbose = int(config.get(section, 'Ent_verbose')) if config.get(section, 'Ent_verbose') != '' else 2
    if ft_command == 'super':
        Ent_minCountLabel = int(config.get(section, 'Ent_minCountLabel')) if config.get(section, 'Ent_minCountLabel') != '' else 0
        Ent_label = config.get(section, 'Ent_label') if config.get(section, 'Ent_label') != '' else '__label__'
        Ent_pretrainedVectors = config.get(section, 'Ent_pretrainedVectors').encode('sjis') if winJP else \
                                config.get(section, 'Ent_pretrainedVectors')

    if ft_command == 'super':
        if Ent_pretrainedVectors != '':
            model = ft.train_supervised(input=Ent_input, lr=Ent_lr, dim=Ent_dim, ws=Ent_ws, epoch=Ent_epoch,
                                        minCount=Ent_minCount, minCountLabel=Ent_minCountLabel, minn=Ent_minn,
                                        maxn=Ent_maxn, neg=Ent_neg, wordNgrams=Ent_wordNgrams, loss=Ent_loss,
                                        bucket=Ent_bucket, thread=Ent_thread, lrUpdateRate=Ent_lrUpdateRate,
                                        t=Ent_t, verbose=Ent_verbose, label=Ent_label,
                                        pretrainedVectors=Ent_pretrainedVectors)
        else:
            model = ft.train_supervised(input=Ent_input, lr=Ent_lr, dim=Ent_dim, ws=Ent_ws, epoch=Ent_epoch,
                                        minCount=Ent_minCount, minCountLabel=Ent_minCountLabel, minn=Ent_minn,
                                        maxn=Ent_maxn, neg=Ent_neg, wordNgrams=Ent_wordNgrams, loss=Ent_loss,
                                        bucket=Ent_bucket, thread=Ent_thread, lrUpdateRate=Ent_lrUpdateRate,
                                        t=Ent_t, verbose=Ent_verbose, label=Ent_label,)
    else:
        mode = 'skipgram' if ft_command == 'skip' else 'cbow'
        model = ft.train_unsupervised(input=Ent_input, model=mode, lr=Ent_lr, dim=Ent_dim, ws=Ent_ws, epoch=Ent_epoch,
                                      minCount=Ent_minCount, minn=Ent_minn, maxn=Ent_maxn, neg=Ent_neg,
                                      wordNgrams=Ent_wordNgrams, loss=Ent_loss, bucket=Ent_bucket, thread=Ent_thread,
                                      lrUpdateRate=Ent_lrUpdateRate, t=Ent_t, verbose=Ent_verbose)

    binFile = ft_currentDir+'/'+Ent_output+'.bin'
    if winJP : binFile = binFile.encode('sjis')  # for Japanese users
    model.save_model(binFile)
    sys.exit(0)

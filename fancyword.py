import sublime
import sublime_plugin
import sys
import os
import re
import json
import subprocess
from collections import OrderedDict
package_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(package_folder, "dependences"))
from nltk.corpus import wordnet as wn
import nltk
nltk.data.path.insert(0, os.path.join(package_folder, 'dependences', 'nltk'))

if sublime.version() < '3000':
    # nltk can't run on Python2.6.9, FancyWord only supports SublimeText 3
    _ST3 = False
else:
    _ST3 = True
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError

# word2vec_api_server process
p = None


def start_subproc(c):
    global p
    p = subprocess.Popen(c, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def plugin_loaded():
    print('FancyWord loaded')
    if not os.path.exists(os.path.join(package_folder, 'Main.sublime-menu')):
        template_file = os.path.join(
            package_folder, 'templates', 'Main.sublime-menu.tpl'
        )
        with open(template_file, 'r', encoding='utf8') as tplfile:
            template = Template(tplfile.read())

        menu_file = os.path.join(package_folder, 'Main.sublime-menu')
        with open(menu_file, 'w', encoding='utf8') as menu:
            menu.write(template.safe_substitute({
                'package_folder': os.path.basename(package_folder)
            }))


def plugin_unloaded():
    if p and not p.poll():
        p.terminate()


def word2vec_topn_outproc(word2vec_port, w, n):
    url = "http://127.0.0.1:{}/word2vec/most_similar?positive={}&topn={}".format(word2vec_port,
        w, n)
    req = Request(url, None)
    try:
        page = urlopen(req)
        html = page.read().decode()
        page.close()
        words_distances = json.loads(html)
        words = list(map(lambda x: x[0], words_distances))
        return words
    except HTTPError:
        return []
    except URLError:
        raise


def wordnet_topn(w, n, lang):
    rst = []
    a = [ss for ss in wn.synsets(w, lang=lang)]
    for ai in a:
        name = ai.name().split('.')[0]
        if name not in rst:
            rst.append(name)
    b = [sim for ai in a for sim in ai.similar_tos()]
    for bi in b:
        name = bi.name().split('.')[0]
        if name not in rst:
            rst.append(name)
    if w in rst:
        rst.remove(w)
    return rst[:n]

def is_word2vec_api_server_running():
    import psutil
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
        except psutil.NoSuchProcess:
            pass
        else:
            if 'python' in p.name().lower() and len(p.cmdline()) > 1 and "dependences/word2vec-api.py" in p.cmdline()[1]:
                return True
    return False


class FancyWordCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        s = sublime.load_settings("FancyWord.sublime-settings")
        self.topn = int(s.get('topn', 10))
        self.lang = s.get('language', 'eng')
        self.word2vec_setting = s.get('word2vec', {})
        self.word2vec_enabled = self.word2vec_setting.get('enabled', False)
        self.word2vec_python_path = self.word2vec_setting.get(
            'python_path', 'python')
        self.word2vec_model = self.word2vec_setting.get(
            'pretrained_word2vec_model', '')
        self.word2vec_port = self.word2vec_setting.get('port', 5000)
        self.wordnet_enabled = s.get('wordnet', {}).get('enabled', True)
        # when word2vec-api server is dead, restart it
        if self.word2vec_enabled and not is_word2vec_api_server_running():
            # ['/usr/local/bin/python', '/Users/easton/Downloads/word2vec-api/word2vec-api.py', '--model', '~/Downloads/deps.words.bin', '--binary', 'true']
            print('FancyWord: word2vec-api server is starting')
            word2vec_api_file_path = os.path.join(
                package_folder, 'dependences/word2vec-api.py')
            self.word2vec_api_command = [self.word2vec_python_path, word2vec_api_file_path,
                                         '--model', self.word2vec_model,
                                         '--binary', 'true',
                                         '--port', str(self.word2vec_port)]
            print(' '.join(self.word2vec_api_command))
            start_subproc(self.word2vec_api_command)

    def run(self, edit):
        self.selection = self.view.sel()
        self.pos = self.view.sel()[0]
        if self.view.sel()[0].a == self.view.sel()[0].b:
            self.view.run_command("expand_selection", {"to": "word"})

        phrase = self.view.substr(self.selection[0]).lower()
        if not phrase:
            return  # nothing selected

        try:
            word2vec_rst = word2vec_topn_outproc(self.word2vec_port, phrase, self.topn)
        except URLError:
            print('FancyWord: word2vec-api server is not reachable')
            print('FancyWord: Will start word2vec-api server')
            word2vec_rst = []

        wordnet_rst = wordnet_topn(phrase, self.topn, self.lang)
        self.suggestions = []
        self.index_suggestions = []
        if word2vec_rst:
            self.index_suggestions += ['{}: {}'.format(idx + 1, sug) + (''.join(
                [' ' * 4, '=' * 4, ' Word2Vec results:']) if idx == 0 else '') for idx, sug in enumerate(word2vec_rst)]
            self.suggestions += word2vec_rst
        len_word2vec_sug = len(word2vec_rst)
        if wordnet_rst:
            self.index_suggestions += ['{}: {}'.format(idx + len_word2vec_sug + 1, sug) + (''.join(
                [' ' * 4, '=' * 4, ' Wordnet results:']) if idx == 0 else '') for idx, sug in enumerate(wordnet_rst)]
            self.suggestions += wordnet_rst
        if self.suggestions:
            self.view.window().show_quick_panel(self.index_suggestions,
                                                self.on_done,
                                                sublime.MONOSPACE_FONT)
        else:
            sublime.status_message(
                "FancyWord: can't find similar words for {}!".format(phrase))
            self.on_done(-1)

    def on_done(self, index):
        if (index == -1):
            self.view.sel().clear()
            if not _ST3:
                self.view.sel().add(sublime.Region(long(self.pos.a), long(self.pos.b)))
            else:
                self.view.sel().add(sublime.Region(self.pos.a, self.pos.b))
            return
        self.view.run_command("insert_my_text", {"args": {'text': self.suggestions[index],
                                                          'posa': self.pos.a, 'posb': self.pos.b}})


class LookUpWordCommand(sublime_plugin.TextCommand):
    # def __init__(self, view):
    #     sublime_plugin.TextCommand.__init__(self, view)

    def run(self, edit):
        self.selection = self.view.sel()
        self.pos = self.view.sel()[0]
        if self.view.sel()[0].a == self.view.sel()[0].b:
            self.view.run_command("expand_selection", {"to": "word"})

        phrase = self.view.substr(self.selection[0]).lower()
        self.view.sel().clear()
        if not _ST3:
            self.view.sel().add(sublime.Region(long(self.pos.a), long(self.pos.b)))
        else:
            self.view.sel().add(sublime.Region(self.pos.a, self.pos.b))

        if not phrase:
            return  # nothing selected
        s = sublime.load_settings("FancyWord.sublime-settings") or {}
        lang = s.get('language', 'eng')
        def_exmp = OrderedDict()
        for w in wn.synsets(phrase, lang=lang):
            def_exmp[w.name()] = {'def': w.definition(), 'exmp': w.examples()}
        if not def_exmp:
            sublime.status_message(
                "FancyWord: can't find definition words for {}!".format(phrase))
            return
        self.def_exmp = []
        for w, de in def_exmp.items():
            self.def_exmp.append('<u>' + w + '</u>: ' + de['def'])
            for e in de['exmp']:
                self.def_exmp.append('- <i>' + e + '</i>')
        self.def_exmp = '<br>'.join(self.def_exmp)
        if int(sublime.version()) >= 3070:
            self.view.show_popup(self.def_exmp)
        else:
            self.print_doc(edit)

    def print_doc(self, edit):
        """Print the documentation string into a Sublime Text panel
        """

        doc_panel = self.view.window().create_output_panel(
            'fancyword_defexmp'
        )

        doc_panel.set_read_only(False)
        region = sublime.Region(0, doc_panel.size())
        doc_panel.erase(edit, region)
        doc_panel.insert(edit, 0, self.def_exmp)
        self.def_exmp = None
        doc_panel.set_read_only(True)
        doc_panel.show(0)
        self.view.window().run_command(
            'show_panel', {'panel': 'output.fancyword_defexmp'}
        )


class InsertMyText(sublime_plugin.TextCommand):
    def run(self, edit, args):
        self.view.replace(edit, self.view.sel()[0], args['text'])

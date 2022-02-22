#!/bin/bash

# Making sure data folder gets right rights.
sudo chown vscode data

# Workarount to try to mitigate SSL verification issue.
# Poetry SSL issue: https://stackoverflow.com/questions/48391750/disable-python-requests-ssl-validation-for-an-imported-module

poetry install
ret=$?
if [ $ret -ne 0 ]; then
        export  CURL_CA_BUNDLE=""
        poetry install
else
        echo "Install sucess!!"
fi


poetry run jupyter notebook --generate-config
echo 'c.NotebookApp.contents_manager_class = "jupytext.TextFileContentsManager"' >> /home/vscode/.jupyter/jupyter_notebook_config.py
poetry run jupyter nbextension install --py jupytext --user
poetry run jupyter nbextension enable jupytext --user --py
poetry run pre-commit install

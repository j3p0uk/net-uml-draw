#!/bin/bash -xeu

export PATH=${PATH}:~/.local/bin
pip install -q --user -r test-requirements.txt

$HOME/.local/bin/tox --workdir /tmp "${@}"


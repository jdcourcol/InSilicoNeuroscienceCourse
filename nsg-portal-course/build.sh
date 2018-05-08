#!/usr/bin/env bash

tar -cvf ./initial_ncx_data.tar.gz ./model/
pushd ./utils/nsg-bluepyopt-job/
python setup.py sdist
popd

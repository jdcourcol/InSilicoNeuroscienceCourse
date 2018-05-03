#!/usr/bin/env bash
tar -cvf ./model/initial_data.tar.gz ./model/hippo-ca1

tar -cvf ./model/initial_ncx_data.tar.gz ./model/neoctx-L5PC
pushd ./utils/nsg-bluepyopt-job/
python setup.py sdist
popd

#!/usr/bin/env bash
tar -cvf ./model/initial_data.tar.gz ./model/hippo-ca1
pushd ./utils/nsg-bluepyopt-job/
python setup.py sdist
popd

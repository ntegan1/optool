#!/bin/bash

whereami="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)"
bin_dir="${whereami}/bin"
thirdparty_dir="${whereami}/thirdparty"
node_dir="${thirdparty_dir}/node-v19.2.0-linux-arm64"
if echo "$PATH" | grep -q "${bin_dir}"; then
  echo optool bin_dir already on PATH
else
  echo adding optool bin_dir to PATH
  export PATH="${PATH}":"${bin_dir}"
fi

if test -d "${node_dir}"; then
  if echo "$PATH" | grep -q "${node_dir}/bin"; then
    echo nodejs bin_dir already on PATH
  else
    echo nodejs bin_dir to PATH
    export PATH="${PATH}":"${node_dir}/bin"
  fi
fi

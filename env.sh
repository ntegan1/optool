#!/bin/bash

whereami="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)"
bin_dir="${whereami}/bin"
thirdparty_dir="${whereami}/thirdparty"
node_dir="${thirdparty_dir}/node-v19.2.0-linux-arm64"
socat_dir="${thirdparty_dir}/socat-1.7.4.4"

if echo "$PATH" | grep -q "${bin_dir}"; then
  echo optool bin_dir already on PATH
else
  echo adding optool bin_dir to PATH
  export PATH="${PATH}":"${bin_dir}"
fi

if test -d "${socat_dir}"; then
  if echo "$PATH" | grep -q "${socat_dir}/bin"; then
    echo socat bin_dir already on PATH
  else
    echo socat bin_dir to PATH
    export PATH="${PATH}":"${socat_dir}/bin"
  fi
fi

if test -d "${node_dir}"; then
  if echo "$PATH" | grep -q "${node_dir}/bin"; then
    echo nodejs bin_dir already on PATH
  else
    echo nodejs bin_dir to PATH
    export PATH="${PATH}":"${node_dir}/bin"
    export npm_config_cache=/data/media/.npm
    mkdir -p ${npm_config_cache}
  fi
fi

#!/bin/bash

whereami="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)"
bin_dir="${whereami}/bin"
if echo "$PATH" | grep -q "${bin_dir}"; then
  echo optool bin_dir already on PATH
else
  echo adding optool bin_dir to PATH
  export PATH="${PATH}":"${bin_dir}"
fi

#!/usr/bin/env bash
script_dir="${BASH_SOURCE%/*}/"
analysis_tarfile=".__Analysis_Submission.tar.gz"
if [ -f "${analysis_tarfile}" ]; then
    rm ${analysis_tarfile}
fi
echo "creating the tarfile for analysis"
${script_dir}/make_p1_tar.sh ${analysis_tarfile} || exit -1
echo "submitting for analysis"
~cs3214/bin/analysis-submit.sh ${analysis_tarfile} || exit -1

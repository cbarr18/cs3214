#!/usr/bin/env bash
script_dir="${BASH_SOURCE%/*}/"
consent_file="$HOME/._analysis_project_consent"
consent_information=$(cat "${script_dir}/consent_information.txt")
if [ ! -f "${consent_file}" ]; then
    read -p "${consent_information}" yn
    case $yn in
        [Yy]* ) touch ${consent_file};;
        [Nn]* ) echo "No consent was given";;
        * ) echo "Please answer y or n.";;
    esac
fi
analysis_tarfile=".__Analysis_Submission.tar.gz"
if [ -f "${analysis_tarfile}" ]; then
    rm ${analysis_tarfile}
fi
echo "creating the tarfile for analysis"
${script_dir}/make_p1_tar.sh ${analysis_tarfile} || exit -1
echo "submitting for analysis"
~cs3214/bin/analysis-submit.sh ${analysis_tarfile} || exit -1

#!/usr/bin/env bash
script_dir="${BASH_SOURCE%/*}/"
consent_file="~/._analysis_project_consent"
if [ ! -f "${consent_file}" ]; then
    read -p "The anonymized results of this analysis may be used for research purposes. Do you consent to allowing your anonymized results to be used to research purposes?" yn
    case $yn in
        [Yy]* ) touch ${consent_file}; break;;
        [Nn]* ) echo "Aborting submission"; exit 4;;
        * ) echo "Please answer yes or no.";;
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

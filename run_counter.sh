#!/bin/bash

start=$(date +%s)

if [ $# != 2 ]; then
  echo "USAGE: sh run.sh input output"
  echo "input: directory or file"
  echo "output: directory or file"
  exit 1
fi


INPUT=$1
OUTPUT=$2

UPGRADE_MDL="api_upgrade_src"
# UPGRADE_FILE="parallel_executor_api_upgrade_run.py"
UPGRADE_FILE="upgrade_api_counter_run.py"


CUR_FOLDER=$(dirname $(readlink -f "$0"))
COUNTER_OUTPUT_PATH_ORI="${CUR_FOLDER}/api_upgrade_src/dict/new_counter_output.dict"
echo "curent folder : ${COUNTER_OUTPUT_PATH_ORI}"

cp "${CUR_FOLDER}/api_upgrade_src/dict/new_counter.dict" "${CUR_FOLDER}/api_upgrade_src/dict/new_counter_output.dict"

if [ -d ${INPUT} ]
then
  if [ ! -d ${UPGRADE_MDL} ]; then
    echo "api_upgrade_src module does not exist, please clone the code"
    exit 1
  fi

  if [ ! -f ${UPGRADE_FILE} ]; then
    echo "upgrade_models_api_run.py does not exist, please clone the code"
    exit 1
  fi

  if [ ! -d "${INPUT}/${UPGRADE_MDL}" ]; then
    # cp -r ${UPGRADE_MDL} ${INPUT}
    rsync -av --progress ${UPGRADE_MDL} ${INPUT} --exclude="*/tests/*"
  fi

  if [ ! -f "${INPUT}/${UPGRADE_FILE}" ]; then
    # cp ${UPGRADE_FILE} ${INPUT}
    rsync -av --progress ${UPGRADE_FILE} ${INPUT} --exclude="*/tests/*"
  fi

  cd ${INPUT}
  output_fir="${CUR_FOLDER}/${OUTPUT}"
  config_file="./api_upgrade_src/conf/upgrade.conf"
  sed -i "1c input_path=${INPUT}" ${config_file}
  sed -i "2c output_path=${output_fir}" ${config_file}
  sed -i "3c counter_path=${COUNTER_OUTPUT_PATH_ORI}" ${config_file}

  python3 ${UPGRADE_FILE}

  if [ -d "${UPGRADE_MDL}" ]; then
    rm -r ${UPGRADE_MDL}
  fi

  if [ -f "${UPGRADE_FILE}" ]; then
    rm ${UPGRADE_FILE}
  fi

  cd ${CUR_FOLDER}
elif [ -f ${INPUT} ]
then
  prefix="./"
  INPUT=${INPUT#$prefix}
  ls -l | grep "${INPUT}"
  cur_stat=$?
  filename=${INPUT}
  if [ ${cur_stat} == 1 ]; then
      dir_name=$(dirname ${INPUT})
      filename=${INPUT##*/}
      
      if [ ! -d " ${dir_name}/${UPGRADE_MDL}" ]; then
        # cp -r ${UPGRADE_MDL} ${dir_name}
        rsync -av --progress ${UPGRADE_MDL} ${dir_name} --exclude="*/tests/*"
      fi
      
      if [ ! -f " ${dir_name}/${UPGRADE_FILE}" ]; then
        # cp ${UPGRADE_FILE} ${dir_name}
        rsync -av --progress ${UPGRADE_FILE} ${dir_name} --exclude="*/tests/*"
      fi
      
      cd ${dir_name}
  fi
  output_fir="${CUR_FOLDER}/${OUTPUT}"
  config_file="./api_upgrade_src/conf/upgrade.conf"
  sed -i "1c input_path=${filename}" ${config_file}
  sed -i "2c output_path=${output_fir}" ${config_file}
  python3 ${UPGRADE_FILE}
  if [ ${cur_stat} == 1 ]; then
      if [ -d "${UPGRADE_MDL}" ]; then
        rm -r ${UPGRADE_MDL}
      fi
      
      if [ -f "${UPGRADE_FILE}" ]; then
        rm ${UPGRADE_FILE}
      fi
      
      cd ${CUR_FOLDER}
  fi

fi

end=$(date +%s)
take=$(( end - start ))
echo Time taken to execute commands is ${take} seconds.
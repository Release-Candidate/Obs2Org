#!/bin/bash
#
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Tzolkin
# File:     get_changelog.sh
#
################################################################################

# Returns the newest part of the changelog `CHANGELOG.md`.
# For use with automatic releases.

# Path to the changelog to parse
CHANGELOG_PATH="../CHANGELOG.md"


LINE_NUMS=$(grep '##' ${CHANGELOG_PATH} -n| head -2|cut -f1 -d":"|paste -s -d' ')

LINE_NUM_ARRAY=(${LINE_NUMS})

if [ "${#LINE_NUM_ARRAY[@]}" -lt "1" ]
then
    echo ""
elif [ "${#LINE_NUM_ARRAY[@]}" -lt "2" ]
then
    tail +${LINE_NUM_ARRAY[0]} ${CHANGELOG_PATH}
else
    head -$((${LINE_NUM_ARRAY[1]} - 1)) ${CHANGELOG_PATH} | tail +${LINE_NUM_ARRAY[0]}
fi

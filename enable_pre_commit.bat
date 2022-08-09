@REM ###########################################################################  #
@REM Baker Hughes Energy Technology UK Limited Confidential                       #
@REM [Unpublished] Copyright 2022.  Baker Hughes Energy Technology UK Limited.    #
@REM NOTICE:  All information contained herein is, and remains the property of    #
@REM Baker Hughes Energy Technology UK Limited, its suppliers, and affiliates, if #
@REM any.                                                                         #
@REM The intellectual and technical concepts contained herein are proprietary to  #
@REM Baker Hughes Energy Technology UK Limited and its suppliers and affiliates   #
@REM and may be covered by U.S. and Foreign Patents, patents in process, and are  #
@REM protected by trade secret and copyright law.                                 #
@REM Dissemination of this information or reproduction of this material is        #
@REM strictly forbidden unless prior written permission is obtained from Baker    #
@REM Hughes Energy Technology UK Limited.                                         #
@REM ###########################################################################  #

@REM This batch file will enable the use of pre-commit on the current checkout if run
@REM in the root of the checkout.
@REM Pre-commit is included as a part of the BH_Utils package but requires the existance
@REM of .pre-commit-config.yaml in the root of the checkout and will run a number of
@REM tests prior to allowing the commit. It will also fix up #nnn format strings to
@REM reference the tracker defined in .ticket_master.txt and check that the issue
@REM exists and is open for you.

pre-commit install -tpre-commit -tcommit-msg

@REM You should now have pre-commit working on your repository.

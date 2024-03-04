# Qradar-Security-Solutions


## Introduction

With IBM QRadar, administrators can invoke a custom script and pass data to a script that is
based on a rule response.

This document describes sample custom action script for Pure Storage FlashArray which can be used with QRadar. 
It provides details on script's available action, inputs required for the script to run, and the configuration file to be created.

## Create the Configuration File
The configuration file needs to be created under “/opt/qradar/bin/ca_jail/pure.conf” with following parameters on the QRadar SIEM server:

Click [here](https://support.purestorage.com/FlashArray/PurityFA/FlashArray_Admin_and_CLI_Reference_Guides) and refer to the section Creating API Tokens for details on how to create an api_token.  

Config file has one entry per FlashArray.
To incorporate new Volumes or Protection Groups, users can perform an in-place edit on the corresponding array line within the file. 
The plugins will automatically detect these changes for subsequent executions.
When adding a new array, users should append a new line to the file, as illustrated below, and provide the required details accordingly.

| Name                  | Type        | Description                                 | Required |
| --------------------- | ----------- | ------------------------------------------- | -------- |
| Array controller name | String      | Name of the FlashArray                      | Yes      |
| API Token             | String      | API token access the array                  | Yes      |
| volume list           | List        | List of volumes to creare snapshot          | Yes      |
| Protection group list | List        | List of protection group to creare snapshot | Yes      |


Sample configuration file

```
pure-array-1:xxxxx-fffff-xccccc-ccceeee:aa_test_vol,testvol1:ps_1,pg_2
pure-array-2:xxxxx-fffff-xccccc-ccceeee:test_vol,pp_vol:pg_3,pgroup-auto
```

## Confuguring custom action script on QRadar

The custom script must be uploaded into IBM QRadar by using the Define Actions icon in
the Admin tab of the IBM QRadar GUI. Download the python script and
saved to the location on the local drive that is used to access IBM QRadar before uploading it
onto IBM QRadar.




### Creating a custom action script
This section explains how to create custom action scripts that can be associated with QRadar
events.
Complete the following steps:
1. Download the python script.
2. In the IBM QRadar GUI, open **Admin settings**.
3. Click the navigation menu, and then click **Admin** to open the **Admin** tab.
4. Under **Custom Actions**, click **Define Actions**.
5. To upload your scripts, click **Add**.
6. Under **Basic Information**, type a name for the custom action.
7. Scroll down to **Script configuration** and select **Interpreter: Bash, python, perl**.
8. Click **Browse** and find the file that you created in step 1.
9. Scroll to the bottom of the Define Custom Action window and click **Save**.
10.Click **Deploy Changes**.

### Script configuration for different actions

Scripts parameters can be fixed property or network event property which is extacted from the event. 

The python script supports following actions. 

1. Create single volume snapshot (action = vol_snapshot )

![alt text](images/image1.png)

2. Create multiple volume snapshot action = multivol_snapshot).

![alt text](images/image4.png)

3. Create protection group snapshot (action = pg_snapshot).

![alt text](images/image3.png)

4. Remove user (action = remove_user). 

![alt text](images/image2.png)

### Testing the custom action script
Verify that the test file is created or updated either by using the **Test Execution** function in the
Define Actions window or by confirming that the Custom Rule has been triggered.

To test the script by using the Test Execution, complete the following steps:

1. Open the **Admin settings**, and in the IBM QRadar GUI, click the navigation menu, and
then click **Admin** to open the **Admin** tab.
2. Scroll down to **Custom Actions**.
3. Click **Define Actions**.
4. Highlight the test script.
5. Click **Test Execution → Execute**.
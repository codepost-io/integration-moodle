# Integrating with Moodle

This repository contains short utility scripts that make it easy to connect codePost with Moodle.

A typical lead instructor will usually do something like the following every week:

- Import student submissions into codePost from Moodle
- Grade and review student submissions in codePost
- Export grades from codePost back to Moodle in a csv

# Import submissions into codePost from Moodle

First, we’ll download assignment submissions from Moodle to our local machine.

Next, we’ll run `moodle_to_codepost_manual` script, which will create a folder called `codepost_upload` which you can drag-and-drop into codePost. Any errors will show up in the `errors` folder.

The process will only take a minute, start to finish.

> Need help? Email us at team@codepost.io

## 0. Downloading Submissions from Moodle

If you are using MNet, go to the Assignment then click `Grading Action -> Download All Submissions`.

You'll notice that the submissions are organized in folders for each student, which is the structure we need for codePost. So all we will do now is change the name of each folder to be the student email instead of their full name.

Name this downloaded folder `submissions`.

## 1. Download the roster

If you are using MNet, go to the Course Participants then click `Select All -> With selected users... -> Download Table Data as Comma separated values (.csv)`.

Name this download `roster.csv`.

## 2. Setting up the script

Clone this repository or copy the python script `moodle_to_codepost_manual.py` to your local machine in the same folder as `submissions` and `roster.csv`.

Move the script, `roster.csv` and `submissions` into the same directory.

## 3. Run the script

Make sure that you have Python3 installed and run

`python3 moodle_to_codepost_manual.py submissions roster.csv`

You should now see a folder called `codepost_upload`, whose subfolders correspond to students. Any problem files will show up in the `errors` folder.

> Optional flag '--simulate' will run the script without copying any files
> `python3 moodle_to_codepost_manual.py submissions roster.csv --simulate`

## 4. Upload to codePost

Navigate to [codepost.io](https://codepost.io), log in, and click `Assignments -> Actions -> Upload Submissions -> Multiple Submissions`. Drag `codepost_upload` into codePost and voila.

If you prefer to have more control over the upload process, check out our [Python SDK](https://github.com/codepost-io/codepost-python).

## Special Case A: Partners

Many assignments will have students submit together in groups of 2 or more.

If you want codePost to recognize group submissions, you can require your students to submit an extra file in their submission called `partners.txt` which contains the email address of each group member on a newline.

Like this:

```
partner1@school.edu
partner2@school.edu
partner3@school.edu
```

The `moodle_to_codepost_manual` script will read this file from Moodle and do the work necessary to make sure the students are recorded as partners on codePost.

# Exporting grades from codePost to Moodle

Once all submissions for an assignment are graded on codePost, go to `codepost.io/admin -> Assignments -> Download Grades`.

Format the csv as necessary and upload to Moodle by going to your Moodle Instance -> Grades -> Import -> CSV file.

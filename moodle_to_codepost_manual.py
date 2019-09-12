# =============================================================================
# codePost – Moodle Utility
#
# Takes submissions downloaded from Moodle and transforms the file
# structure into a structure that codePost will recognize.
#
# =============================================================================

# Python stdlib imports
import os
import argparse
import csv
import shutil
import re

# =============================================================================

parser = argparse.ArgumentParser(description='Moodle to codePost!')
parser.add_argument(
    'submissions', help='The directory of submissions downloaded from Moodle')
parser.add_argument(
    'roster', help='The course roster of students that includes first name, last name, and email')
parser.add_argument('-s', '--simulate', action='store_true')
args = parser.parse_args()

# =============================================================================
# Constants

OUTPUT_DIRECTORY = 'codepost_upload'
ERROR_DIRECTORY = 'errors'

_cwd = os.getcwd()
_upload_dir = os.path.join(_cwd, OUTPUT_DIRECTORY)
_error_dir = os.path.join(_cwd, ERROR_DIRECTORY)

# =============================================================================
# Helpers


def normalize(string):
  return string.lower().strip()


def delete_directory(path):
  if os.path.exists(path):
    shutil.rmtree(path)


def validate_csv(row):
  for key in row.keys():
    if 'first name' in normalize(key):
      first_name = key
    if 'last name' in normalize(key):
      last_name = key
    elif 'email' in normalize(key):
      email = key

  if first_name == None or last_name == None or email == None:
    if first_name == None:
      print("Missing header: First name")
    if last_name == None:
      print("Missing header: Last name")
    if email == None:
      print("Missing header: email")

    raise RuntimeError(
        "Malformatted roster. Please fix the headers and try again.")

    return (first_name, last_name, email)
  else:
    return (first_name, last_name, email)


def moodle_name_to_email(roster):
  with open(roster, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    first_name, last_name, email = (None, None, None)
    moodle_name_to_email = {}
    for row in csv_reader:
      if line_count == 0:
        (first_name, last_name, email) = validate_csv(row)
        line_count += 1

      # Moodle convention: map {First Name} {Last Name} to {codePost email}
      moodle_name_to_email["{} {}".format(
          normalize(row[first_name]), normalize(row[last_name]))] = normalize(row[email])
      line_count += 1
    return moodle_name_to_email


def check_for_partners(moodle_folder, file_name):
  filepath = os.path.join(os.path.join(
      args.submissions, moodle_folder), file_name)
  emails = [line.rstrip('\n') for line in open(filepath, 'r')]
  EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
  filtered_emails = [x for x in emails if re.match(EMAIL_REGEX, x)]

  return filtered_emails

# =============================================================================

if (args.simulate):
  print('\n~~~~~~~~~~~ START SIMULATION ~~~~~~~~~~~')

print('\nSetting up directories...')

# Overwrite the directories if they exist already
if not args.simulate:
  delete_directory(_upload_dir)
  delete_directory(_error_dir)

  os.makedirs(_upload_dir)
  os.makedirs(_error_dir)

print('\t/{}'.format(OUTPUT_DIRECTORY))
print('\t/{}'.format(ERROR_DIRECTORY))

print('\nReading and validating roster...')
moodle_name_to_email = moodle_name_to_email(args.roster)
print('\tVALID')

print('\nChecking submissions for partners...')

moodle_folders = os.listdir(args.submissions)
folders = []
for moodle_folder in moodle_folders:
  if os.path.isdir(os.path.join(args.submissions, moodle_folder)):
    files = os.listdir(os.path.join(args.submissions, moodle_folder))
    for file in files:
      if 'partners' in file:
        partners = check_for_partners(moodle_folder, file)
        folders.append(partners)

print('\t{}'.format(folders))

print('\nCreating student folders...')
for student in moodle_name_to_email:
  found = False
  for folder in folders:
    if moodle_name_to_email[student] in folder:
      found = True
      break

  if not found:
    folders.append([moodle_name_to_email[student]])

print('\nMapping and copying files...')
for moodle_folder in moodle_folders:
  if os.path.isdir(os.path.join(args.submissions, moodle_folder)):
    full_name = moodle_folder.split('_')[0]

    if normalize(full_name) in moodle_name_to_email:
      email = moodle_name_to_email[normalize(full_name)]
      found = False
      for folder in folders:
        if email in folder:
          folder_name = ",".join(folder)
          found = True
          if not args.simulate:
            shutil.copytree(os.path.join(args.submissions, moodle_folder),
                            os.path.join(_upload_dir, folder_name))
          print("\t{}".format(os.path.join(_upload_dir, folder_name)))

      if not found:
        if not args.simulate:
          shutil.copytree(os.path.join(args.submissions, moodle_folder),
                          os.path.join(_error_dir, moodle_folder))
        print('\tERROR: {}'.format(os.path.join(_error_dir, moodle_folder)))
    else:
      if not args.simulate:
        shutil.copyfile(os.path.join(args.submissions, moodle_folder),
                        os.path.join(_error_dir, moodle_folder))
      print('\tERROR: {}'.format(os.path.join(_error_dir, moodle_folder)))

if args.simulate:
  print('\n~~~~~~~~~~~ END SIMULATION ~~~~~~~~~~~\n')

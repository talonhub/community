# Adding new entries

All of the json entries should be `-` separated, and formatted in a way that can
be interpreted as a spoken command in talon. This is because talon will
automatically interpret all of the keys into spoken commands that correlate to
the entry, an that entry is used to look up the corresponding value in the
json file. For example the phone number entry is `phone-number` in the
corresponding talon command is "phone number".

# Avoid private information leaking

It is very important that when you add personal changes to the
personal_info.json file, that you update your git repository to stop tracking
the file, to ensure that your information is not accidentally pushed into a
public repo. this can be done with the following command:

```
git update-index --assume-unchanged <path to personal_info.json>
```

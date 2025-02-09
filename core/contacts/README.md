# Contacts

This directory provides a versatile `<user.prose_contact>` capture that can be
used to insert names and email addresses using a suffix. This functionality is
exposed through other captures such as `<user.text>` and `<user.prose>`, not
directly as commands. The contact list may be provided in the private directory
via the `contacts.json` file, the `contacts.csv` file, or both.

Here is an example contacts.json:

```json
[
  {
    "email": "john.doe@example.com",
    "full_name": "Jonathan Doh: Jonathan Doe",
    "nicknames": ["Jon", "Jah Nee: Jonny"]
  }
]
```

Note that for either full_name or nicknames, pronunciation can be provided via
the standard Talon list format of "[pronunciation]: [name]". Pronunciation for
the first name is automatically extracted from pronunciation for the full name,
if there are the same number of name parts in each. Pronunciation can be
overridden for the first name by adding a nickname with matching written form.

To refer to this contact, you could say:

- Jonathan Doh email -> john.doe@example.com
- Jonathan email -> john.doe@example.com
- Jah Nee email -> john.doe@example.com
- Jah Nee name -> Jonny
- Jonathan Doh name -> Jonathan Doe
- Jon last name -> Doe
- Jon full name -> Jonathan Doe
- Jon names -> Jon's
- Jon full names -> Jonathan Doe's

The CSV format provides only email and full name functionality:

```csv
Name,Email
John Doe,jon.doe@example.com
Jane Doe,jane.doe@example.com
```

The advantage of the CSV format is that it is easily exported. If both the CSV
and JSON are present, they will be merged based on email addresses. This makes
it easy to use an exported CSV and maintain nicknames in the JSON. For example,
to export from Gmail, go to https://contacts.google.com/, then click "Frequently
contacted", then "Export". Then run:

```bash
cat contacts.csv | python -c "import csv; import sys; w=csv.writer(sys.stdout); [w.writerow([row['First Name'] + ' ' + row['Last Name'], row['E-mail 1 - Value']]) for row in csv.DictReader(sys.stdin)]"
```

In case of name conflicts (e.g. two people named John), the first instance will
be preferred, with all JSON contacts taking precedence over CSV. If you wish to
refer to both, use the pronunciation to differentiate, using a nickname to
override the first name pronunciation if desired. For example, you might add
"John S: John" and "John D: John" as nicknames to the two different Johns. This
is also an effective way to handle name homophones such as John and Jon, which
would otherwise be resolved arbitrarily by the speech engine.

# Attendance Marker

Welcome to My Application! This application helps you with marking attendance automatically every day.

## Configuration

To start using this application, you need to add a `config.yaml` file in the root directory. The structure should be exactly the same as below:

### `config.yaml`

```yaml
url:
  base_url: https://example-base-url.com/

email:
  from_email: example.from@example.com
  from_password: examplepassword

org:
  your_name:
    emailId: example.email@example.com
    password: examplepassword
    to_email: example.to@example.com
```


## Explanation of config.yaml

base_url: This is the base URL for the application.

from_email: The email address from which the notifications will be sent.

from_password: The password for the from_email account.

to_email: The email address to which the notifications will be sent.


emailId: The email ID for the organization account.

password: The password for the organization account.

## Note
Please replace the example values with your actual data, but do not share the original values publicly.

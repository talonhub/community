# Powershell

By default the windows powershell does not display the current address in the title. To fix this add a prompt function to the powershell profile file. If the powershell profile file doesn't exist then create it.

To find the profile file run `$profile` in windows powershell.

The prompt function to add:

```
function prompt {
  $Host.UI.RawUI.WindowTitle = 'Windows PowerShell: ' +  $(get-location)
  "$pwd" + '> '
}
```

Then you can set the setting `user.powershell_always_refresh_title` to false.

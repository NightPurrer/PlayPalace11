# Sharing server profiles from client to client
The server manager stores a lot of information for each server. This includes:
*server info like name, address, and port.
*User accounts to log into the server.
*Options profile (migrated from v10).

## Goal of system
The goal is to build a flexible system that will allow for easily sharing only specific details from one client to another. This is necessary because the identities.json file has sensitive information that should not be shared around, and doing so would also completely overwrite a client's previous data.
Therefore, both the user exporting the data and the user importing data, should have full control over what gets shared, overwritten, or added.

## Method
To accomplish this flexible system, we only need one screen, an import / export config screen. As well as tracking the mode "import" or "export".
Both modes will have almost identical controls, however there will be slight differences. Importing data will have more options since it is more complex and has the potential to merge with existing data.
To import or export data, the main server manager screen will have a button for each operation.

## Updated server manager main layout
After the add server button, ad the "import server profiles" and "export server profiles" buttons.

## Config Sharing Dialog layout
These controls are present regardless of the mode.

*Details (grouping)
*available servers (checklistbox): the list of available servers to manage data from. When enabled, includes the general information for the focused server along with optional content.
*add options profile (checkbox): determines if the options profile for the focused server should be included in the operation. This means the checkbox should save and refresh state for each server.
*add user accounts (checkbox): determines if the list of user accounts for the focused server should be included in the operation. This means the checkbox should save and refresh state for each server.

*helpers (grouping): this section is collapsable, and is collapsed by default.
*select all servers (button): enables the checkbox for every server in the available servers list.
*deselect all servers (button): disables the checkbox for every server in the available servers list.
*select all option profiles (button): enables the checkbox for every server's options profile.
*deselect all option profiles (button): disables the checkbox for every server's options profile.
*select all user accounts (button): enables the checkbox for every server's user accounts.
*deselect all user accounts (button): disables the checkbox for every server's user accounts.

*operation (grouping)
*start import/export (button): confirms and starts the operation
*cancel (button): aborts the operation.

## Exporting data
This is the simpler operation. It uses the current data from "identities.json" to populate the list of available servers. The data is already loaded into the config manager, so no reading from disc required.
When exporting server info, do not include the trust certificate.
When exporting user accounts, do not include the last connected user id.
After the user has confirmed and started the operation, ask a confirmation warning if user accounts from any servers are included. As user data is sensitive info.
Save the export file as "identities-export.json' in the current working directory.
When saving, ask for a name for this export, and add the unix timestamp when it occurred.

### Exported json File Example
{
 "description": "zarvox's export",
 "timestamp": 11112121111,
 "servers": [] # Copied data
}

### Export Warnings
user accounts (for any server):

"User accounts are included in this export. Are you sure you want to proceed?
Some servers will ban you (the account owner) and anyone who attempts to access the same account."

## Importing data

### Updated config sharing dialog layout

### Import Warnings
user accounts (for any server):

"User accounts are included in this import. Are you sure you want to proceed?
Some servers will ban the account owner and you or anyone else who attempts to access the same account."

option profiles (for any server):
"Option profiles will overwrite your  existing settings. Do you want to proceed?"
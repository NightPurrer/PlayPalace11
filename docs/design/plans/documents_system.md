# Documents System for Play Palace
Documents are a collection of articles that the user can view to get help or information. Each document has categories and locale support.

Since Play Palace is open source, contributors can edit document .md files directly in the repo. The in-app editor is a nice-to-have for those who do not wish to download the source, or if the file format changes in the future. The in-app editor is not critical to the system.

# Roles
Server admins have full control over document organization and contents. However if only admins had access to the documents system, it would make locale support very difficult.
To account for this, admins can approve people to be transcribers. The transcriber role allows for existing documents to support new translations. Transcribers can not manage documents, or create new ones. They can only create and edit translations.
Transcribers will be assigned a list of languages. They can only modify translations for the languages they are assigned. For example, a transcriber with Spanish and French would not be allowed to create or edit translations of an English version.

## Storing transcriber data
The user table has a fluent_languages column, which is a list of lang codes (e.g. ["en", "es"]). This tracks what languages a user knows and can be used for purposes beyond translation in the future.

Transcriber assignments are stored separately, in a transcriber_assignments table (user_id, lang_code). A user may be fluent in a language without being approved as a transcriber for it. This separation also makes queries like "who are the French transcribers?" trivial without parsing JSON arrays.

**Database status: implemented.** The `fluent_languages` column (JSON text on `users`) and `transcriber_assignments` table are in `server/persistence/database.py` with full CRUD methods and migration support. See `server/tests/test_database.py` for coverage.

# Backend folder structure
server/documents/ folder contains each document folder and a "_metadata.json" file.

## Document system metadata file
In the root of the documents folder is a "_metadata.json" file. This file contains:
- Categories dictionary: maps human-readable category slugs to their settings, including a sort order and localized display names.

The slug is the internal identifier, set once at creation, and never shown to users. Renaming a category only changes the display name for a specific locale, not the slug. If a locale translation is missing, the system falls back to English, or the slug itself as a last resort.

### Example
```json
{
    "categories": {
        "news": {
            "sort": "alphabetical",
            "name": {
                "en": "News and Updates",
                "es": "Noticias y Actualizaciones"
            }
        },
        "game_rules": {
            "sort": "alphabetical",
            "name": {
                "en": "Game Rules"
            }
        }
    }
}
```

## Document specific folder
Each document has its own folder, for example "uno_rules".
The folder name IS the document's identity. There is no separate id field in the metadata.
A document's folder contains:
- The content in each locale, e.g. "en.md", "fr.md"
- A "_metadata.json" file

## Document metadata file
Contains the following:
- categories: the list of category slugs this document belongs to.
- source_locale: the original language this document was written in (defaults to "en"). Transcribers use this to detect staleness -- if the source locale's modified_contents is newer than their translation's, they know an update is needed.
- locales: a dictionary of locale codes and settings for each one.

### Locale settings:
- created: the timestamp this locale was created.
- modified_contents: the timestamp for when the document contents of this locale was last modified. This does not include changes to locale settings.
- title: the display title of the document for this locale. Stored in metadata (not in the .md file) so document lists can be displayed without parsing every .md file.
- public: a boolean flag indicating if this locale is visible to normal users. If not, only transcribers and admins can see it.
    - Transcribers of other languages still have viewing access. For example a French transcriber can see the English version even when it is private. This is so the French transcriber knows what changes they need to update before either version is publicly available.
    - A transcriber can only change the visibility for languages they are assigned. For example, a French transcriber can not make an English translation public.

### Example
```json
{
    "categories": ["game_rules"],
    "source_locale": "en",
    "locales": {
        "en": {
            "created": "2026-01-15T10:00:00Z",
            "modified_contents": "2026-02-20T14:30:00Z",
            "title": "Uno Rules",
            "public": true
        },
        "es": {
            "created": "2026-02-01T09:00:00Z",
            "modified_contents": "2026-02-05T11:00:00Z",
            "title": "Reglas de Uno",
            "public": false
        }
    }
}
```

# Loading and data management
Timestamps (created, modified_contents) are stored in metadata JSON, not read from filesystem file attributes. File attributes are unreliable for an open source project -- git does not preserve creation time, and mtime is reset on clone, checkout, and rebase. Contributors editing .md files directly should also update the corresponding _metadata.json. A helper script or pre-commit hook can automate this if it becomes a pain point.

## Startup loading
On server startup, the documents system loads once:
1. Load the root _metadata.json (categories) into memory.
2. Scan each subfolder in server/documents/ and load its _metadata.json into memory.
3. Do NOT load .md content into memory. Document content is loaded on demand when a user views or edits a document.

After startup, all listing, searching, filtering, and title display is served from the in-memory metadata. This keeps memory usage low and startup fast since only small JSON files are read, not every document's full content.

## Writes
When metadata is changed (via the in-app UI or a server command), update both:
- The in-memory state (so changes are reflected immediately)
- The _metadata.json file on disk (so changes persist across restarts)

When document content (.md) is changed via the in-app editor, write directly to disk. There is no in-memory cache for content.

## Edit locks
When someone opens a translation for editing, the server records (user_id, document, locale) as an active edit session. If a second person tries to edit the same translation, they receive a message: "This translation is currently being edited by [username]. You cannot edit it right now." The lock is released when the editor saves or cancels. A timeout (e.g., 30 minutes of inactivity) auto-releases stale locks in case someone disconnects without saving. Admins have a "force unlock" option if a lock gets stuck.

## Version history
When a translation is saved, the previous version is copied to a `_history/` subfolder inside the document folder (e.g., `uno_rules/_history/en_2026-02-28T14-30-00Z.md`). A maximum of 5 versions per locale are kept; the oldest is deleted when the cap is reached. No UI is needed initially — this is a safety net. An admin "view history" menu item can be added later.

# Frontend UI structure

## Documents system UI
Add a "Documents" action in the main menu. The documents menu has the following items:
- Category x: display the category name for each category as its own item. Add an "all documents" item at the top, and an "uncategorized documents" item at the bottom.
- New document (admin): create a new document not found in the system.
- New category (admin): create a new category not found in the system.
- View transcribers by language
- View transcribers by user

## Documents in category menu
- Search documents: the user types a query and confirms before the search runs. The search loads .md files on demand, scoped to the user's current locale and the selected category. No content is preloaded or indexed at startup.
- document x: the document title for each document in this category.
- Rename category (transcriber): allows for changing the user friendly name for the user's current locale.
- add documents to category (admin): add 1 or more documents not associated with this category via a boolean list.
- Remove documents from category (admin): remove 1 or more documents associated with this category via a boolean list.
- Category settings (admin): edit the settings for this category such as sort method. Available sort options: alphabetical, date created, date modified.
- Delete category (admin): deletes this category. Documents associated with this category should remove the category slug from the metadata.

Admin actions remain in this menu to ensure everything is accessible without relying on the context menu.

## Fallback categoies
The system will have two dynamic categories that are not real categories: "all documents" and "uncategorized documents".
Even if the system has 0 categoies or a document has 0 categoies associated, it will still show up in both of these fallback categoies.
Since these are not user generated or real categories, the labels should be apart of the fluent locale bundle data.

## New document
- Choose categories. Selecting no categoies is acceptable.
- Use the "add translation" flow to create the initial translation. Pass the new document folder name and the current user's locale so it knows what document is being created and can skip choosing a locale.

The folder name is auto-generated from the initial title (slugified). If the slug already exists, the user is warned and asked to choose a different title. The folder can be manually renamed on the filesystem if needed, but this is not exposed in the UI.

## New Category
Write a slug and a user friendly name for the user's current locale.

## View transcribers by language
Shows the standard language menu. Append each item with the number of users assigned to that language.
For example, "English (4 users)"
When clicking on a language, displays the list of users in a menu. If an admin, clicking on a user asks if you want to remove them.
If admin, at the bottom is an "add users" item.
When clicked, shows a list of users who do not have this assigned language, with on/off status.

## View transcribers by user
This is the exact inverse of view transcribers by language.
Shows the list of transcribers as a menu. Append each item with the number of languages assigned to that user.
For example, "Zarvox (4 languages)"
When clicking on a user, displays the list of assigned languages in a menu. If an admin, clicking on a language asks if you want to remove it.
If admin, at the bottom is an "add languages" item.
When clicked, shows the standard language menu for the user's fluent languages excluding the already assigned languages, with on/off status.

## Document actions
When clicking on a document:
- Normal users: automatically view the document (no action menu).
- Transcribers and admins: show a short action menu:
    - View document contents
    - Edit document contents
    - Document settings...

"Document settings" opens a submenu with:
- Change title (with language selection)
- Manage visibility (x/x languages public)
- Modify category list (admin): changes the list of categories this document is associated with via a boolean list.
- Add translation
- Remove this translation (admin): removes the translation for the user's current locale. This is only available for admins. The source translation can not be removed. Requires confirmation.
- Delete document (admin): deletes this document completely including the metadata. Requires confirmation, include the number of translations in the prompt. Recovery is not possible.

## Viewing a document
The document content is displayed in a read-only text field as plain text. No markdown rendering.

## Editing a document
The editor is a multiline text field for writing plain text. If the translation being edited is not the source language, a second read-only multiline text field displays the source language translation for side-by-side comparison.
Include save and cancel buttons. Both require confirmation. Pressing escape acts as cancel. If the document has no changes, the save button does nothing.

Note: The platform does not currently support F2 for inline editing or the context menu key on lists. These would be ideal shortcuts (F2 to jump straight to editing, context key for the settings submenu) and are worth considering as platform features in the future. For now, the three-item action menu keeps things simple and discoverable.

## Language selection menu
After clicking an item that requires language selection, display the list of languages the document has been translated into. Append the created and last modified dates.
Focus the user's current language by default. If their locale is not available for this document, focus on the source locale.
If a transcriber selects edit or change title, only their assigned languages are shown.

## Changing title
Brings up a text field for renaming the document title for the selected locale. This modifies the value in _metadata.json. This does not rename the folder on the backend.

## Manage visibility
Show a list of the document's languages with on/off toggles for public visibility.

## Add translation
Select from the language menu -- only languages the document has NOT been translated into are shown. If a transcriber, further filtered to their assigned languages. If no languages are available, inform them.
Brings up a text field for the title, then a multiline text field for the contents. New translations are private when first created.

## Modifying category list
Shows a menu with each category name and its current status (included / excluded). Pressing enter on an item toggles the status.

# Options menu addition: Fluent languages
The options menu gains a "Fluent languages" item, below the active language item. This opens the standard language menu with on/off toggles for each language. The user's active locale is always included and cannot be toggled off. This setting is stored in the `fluent_languages` column on the user table.

Fluent languages live in the options menu because they are a personal profile setting — they describe the user, not a document. Admins use this data when assigning transcribers: only users who have marked a language as fluent can be assigned as transcribers for that language.

# Future plans and considerations
The following are not part of the initial implementation but are worth adding later:

- **Staleness indication for transcribers**: Append "(needs update)" or similar to translations in the language selection menu when the source locale's `modified_contents` is newer than the translation's. Helps transcribers identify what needs attention without manually comparing timestamps.
- **Notification system**: Notify transcribers when a source document they are responsible for has been updated. Could be an in-app notification or a simple "pending updates" list.
- **Version history UI**: An admin "view history" menu item to browse and restore previous versions from the `_history/` folder.
- **Client-side draft persistence**: If the connection drops mid-edit, the client should hold the draft in memory and allow retrying the save on reconnect. If the client crashes entirely, the draft is lost, which is acceptable given the low frequency of editing.
- **F2 and context menu key support**: Platform-level shortcuts for inline editing (F2) and settings access (context menu key) on list items.
